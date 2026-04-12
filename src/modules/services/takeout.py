import json
import logging
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Tuple

try:
    import piexif
    from piexif import InvalidImageDataError
except ImportError:
    piexif = None

SUPPORTED_VIDEO_FORMATS = {'.mp4', '.mov', '.mkv', '.3gp', '.avi', '.m4v', '.webm'}


def find_takeout_json(image_path: str) -> Optional[str]:
    """
    Finds the associated Google Takeout JSON file for a given image.
    Handles common naming conventions like:
    - image.jpg.json
    - image.json
    - image.jpg.supplemen.json
    - image (1).jpg.json -> image.jpg(1).json
    """
    path = Path(image_path)
    dir_name = path.parent
    base_name = path.name
    stem = path.stem

    candidates = [
        f"{base_name}.json",
        f"{stem}.json",
        f"{base_name}.supplemen.json",
        f"{stem}.supplemen.json",
    ]

    if " (" in stem and stem.endswith(")"):
        parts = stem.rsplit(" (", 1)
        if len(parts) == 2:
            orig_name = parts[0]
            num = parts[1][:-1]
            candidates.append(f"{orig_name}{path.suffix}({num}).json")
            candidates.append(f"{orig_name}({num}){path.suffix}.json")
            candidates.append(f"{orig_name}{path.suffix}({num}).supplemen.json")
            candidates.append(f"{orig_name}({num}){path.suffix}.supplemen.json")

    for candidate in candidates:
        json_path = dir_name / candidate
        if json_path.exists():
            return str(json_path)

    return None


def parse_takeout_json(json_path: str) -> Optional[dict]:
    """
    Reads and parses a Google Takeout JSON file.
    Extracts relevant metadata like photoTakenTime, geoData, title, description.
    """
    try:
        with open(json_path, 'r', encoding='utf-8') as file_handle:
            data = json.load(file_handle)

        result = {}

        if 'photoTakenTime' in data and 'timestamp' in data['photoTakenTime']:
            timestamp = int(data['photoTakenTime']['timestamp'])
            from datetime import timezone
            dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
            result['exif_date'] = dt.strftime('%Y:%m:%d %H:%M:%S')

        if 'geoData' in data:
            geo = data['geoData']
            lat = geo.get('latitude', 0.0)
            lon = geo.get('longitude', 0.0)
            alt = geo.get('altitude', 0.0)
            if lat != 0.0 or lon != 0.0:
                result['geo_data'] = {'latitude': lat, 'longitude': lon, 'altitude': alt}

        if 'title' in data:
            result['title'] = data['title']
        if 'description' in data:
            result['description'] = data['description']

        return result
    except Exception as error:
        logging.error(f"Error parsing Takeout JSON {json_path}: {error}")
        return None


def float_to_rational(value: float) -> Tuple[int, int]:
    """Converts a float to a rational number format used by EXIF."""
    return (int(value * 10000), 10000)


def convert_to_degrees(value: float) -> Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int]]:
    """Converts a decimal degree to degrees, minutes, seconds for EXIF."""
    degrees = int(value)
    minutes = int((value - degrees) * 60)
    seconds = (value - degrees - minutes / 60) * 3600.0
    return ((degrees, 1), (minutes, 1), (int(seconds * 10000), 10000))


def enrich_image_with_json(image_path: str, json_data: dict) -> bool:
    """
    Writes data from Takeout JSON into the image's EXIF if the image lacks it.
    Returns True if the image was modified.
    """
    if not piexif:
        logging.warning("piexif library is missing, skipping EXIF write.")
        return False

    try:
        modified = False
        try:
            exif_dict = piexif.load(image_path)
        except Exception:
            exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}, "thumbnail": None}

        has_exif_date = piexif.ExifIFD.DateTimeOriginal in exif_dict.get('Exif', {})
        if not has_exif_date and 'exif_date' in json_data:
            date_str = json_data['exif_date'].encode('utf-8')
            exif_dict.setdefault('Exif', {})[piexif.ExifIFD.DateTimeOriginal] = date_str
            exif_dict.setdefault('0th', {})[piexif.ImageIFD.DateTime] = date_str
            modified = True

        has_gps = piexif.GPSIFD.GPSLatitude in exif_dict.get('GPS', {})
        if not has_gps and 'geo_data' in json_data:
            lat = json_data['geo_data']['latitude']
            lon = json_data['geo_data']['longitude']
            alt = json_data['geo_data'].get('altitude', 0.0)

            lat_ref = b'N' if lat >= 0 else b'S'
            lon_ref = b'E' if lon >= 0 else b'W'

            gps_ifd = exif_dict.setdefault('GPS', {})
            gps_ifd[piexif.GPSIFD.GPSLatitudeRef] = lat_ref
            gps_ifd[piexif.GPSIFD.GPSLatitude] = convert_to_degrees(abs(lat))
            gps_ifd[piexif.GPSIFD.GPSLongitudeRef] = lon_ref
            gps_ifd[piexif.GPSIFD.GPSLongitude] = convert_to_degrees(abs(lon))
            gps_ifd[piexif.GPSIFD.GPSAltitudeRef] = 0 if alt >= 0 else 1
            gps_ifd[piexif.GPSIFD.GPSAltitude] = float_to_rational(abs(alt))
            modified = True

        has_desc = piexif.ImageIFD.ImageDescription in exif_dict.get('0th', {})
        if 'description' in json_data and not has_desc and json_data['description']:
            exif_dict.setdefault('0th', {})[piexif.ImageIFD.ImageDescription] = json_data['description'].encode('utf-8')
            modified = True

        if modified:
            try:
                exif_bytes = piexif.dump(exif_dict)
                piexif.insert(exif_bytes, image_path)
                logging.info(f"Successfully enriched EXIF for {image_path} with Takeout JSON")
                return True
            except Exception as error:
                logging.error(f"Error saving EXIF for {image_path}: {error}")
                return False
    except Exception as error:
        logging.error(f"Error checking/updating EXIF for {image_path}: {error}")

    return False


def get_safe_filename(target_dir: Path, base_name: str, ext: str) -> Path:
    """Returns a non-colliding file path by appending a counter if needed."""
    counter = 1
    new_path = target_dir / f"{base_name}{ext}"
    while new_path.exists():
        new_path = target_dir / f"{base_name}_{counter}{ext}"
        counter += 1
    return new_path


def organize_takeout_photos(photos: list, root_folder: str, cache: dict, update_cb=None) -> Tuple[list, int, int]:
    """
    Intelligently organizes photos if Takeout JSON files are detected in the root folder.
    Renames photos by EXIF date, moves them to YYYY/MM/ folders, and moves processed JSONs to /Json/.
    Returns a tuple: (photos list, number of videos processed, number of JSONs processed).
    """
    root_path = Path(root_folder)

    has_jsons = any(root_path.rglob("*.json"))
    if not has_jsons:
        return photos, 0, 0

    logging.info("Takeout JSON files detected. Starting intelligent organization...")

    if update_cb:
        update_cb("Organizando archivos por fecha (JSON detectado)...")

    processed_jsons = set()
    videos_count = 0

    for photo in photos:
        json_path_str = find_takeout_json(photo.path)
        if not json_path_str:
            continue

        processed_jsons.add(json_path_str)

        if photo.exif_date:
            try:
                date_part, time_part = photo.exif_date.split(' ')
                year, month, day = date_part.split(':')
                hh, mm, ss = time_part.split(':')
                target_dir = root_path / year / month
                base_name = f"{year}-{month}-{day}_{hh}-{mm}-{ss}"
            except Exception as error:
                logging.warning(f"Error parsing date {photo.exif_date} for {photo.path}: {error}")
                target_dir = root_path / "Sin_fecha"
                base_name = Path(photo.path).stem
        else:
            target_dir = root_path / "Sin_fecha"
            base_name = Path(photo.path).stem

        target_dir.mkdir(parents=True, exist_ok=True)
        ext = Path(photo.path).suffix
        new_path = get_safe_filename(target_dir, base_name, ext)

        if str(new_path.resolve()) != str(Path(photo.path).resolve()):
            try:
                shutil.copy2(photo.path, new_path)
                if new_path.exists() and new_path.stat().st_size == Path(photo.path).stat().st_size:
                    os.remove(photo.path)
                    if photo.path in cache:
                        cache[str(new_path)] = cache.pop(photo.path)
                    photo.path = str(new_path)
                else:
                    logging.error(f"Failed to verify copy for {new_path}")
            except Exception as error:
                logging.error(f"Error moving {photo.path} to {new_path}: {error}")

    if update_cb:
        update_cb("Organizando videos por fecha (JSON detectado)...")

    for root, _, files in os.walk(root_path):
        for file_name in files:
            video_path = Path(root) / file_name
            if video_path.suffix.lower() not in SUPPORTED_VIDEO_FORMATS:
                continue

            json_path_str = find_takeout_json(str(video_path))
            if not json_path_str:
                continue

            videos_count += 1
            processed_jsons.add(json_path_str)
            json_data = parse_takeout_json(json_path_str)

            if json_data and 'exif_date' in json_data:
                try:
                    date_part, time_part = json_data['exif_date'].split(' ')
                    year, month, day = date_part.split(':')
                    hh, mm, ss = time_part.split(':')
                    target_dir = root_path / year / month
                    base_name = f"{year}-{month}-{day}_{hh}-{mm}-{ss}"
                except Exception as error:
                    logging.warning(f"Error parsing date {json_data['exif_date']} for {video_path}: {error}")
                    target_dir = root_path / "Sin_fecha"
                    base_name = video_path.stem
            else:
                target_dir = root_path / "Sin_fecha"
                base_name = video_path.stem

            target_dir.mkdir(parents=True, exist_ok=True)
            new_path = get_safe_filename(target_dir, base_name, video_path.suffix)

            if str(new_path.resolve()) != str(video_path.resolve()):
                try:
                    shutil.copy2(str(video_path), new_path)
                    if new_path.exists() and new_path.stat().st_size == video_path.stat().st_size:
                        os.remove(str(video_path))
                    else:
                        logging.error(f"Failed to verify copy for {new_path}")
                except Exception as error:
                    logging.error(f"Error moving {video_path} to {new_path}: {error}")

    if processed_jsons:
        json_dir = root_path / "Json"
        json_dir.mkdir(parents=True, exist_ok=True)
        for json_path in processed_jsons:
            try:
                json_file = Path(json_path)
                if json_file.exists():
                    new_json_path = get_safe_filename(json_dir, json_file.stem, json_file.suffix)
                    shutil.move(str(json_file), str(new_json_path))
            except Exception as error:
                logging.error(f"Error moving JSON {json_path}: {error}")

    return photos, videos_count, len(processed_jsons)
