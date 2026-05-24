import json
import logging
import re
import shutil
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple

try:
    import piexif
    from piexif import InvalidImageDataError
except ImportError:
    piexif = None

SUPPORTED_VIDEO_FORMATS = {'.mp4', '.mov', '.mkv', '.3gp', '.avi', '.m4v', '.webm'}
PIEXIF_WRITABLE_FORMATS = {'.jpg', '.jpeg'}
FILENAME_DATE_PATTERNS = [
    re.compile(
        r"(?P<year>20\d{2}|19\d{2})[_-](?P<month>\d{2})[_-](?P<day>\d{2})"
        r"[_\s-](?P<hour>\d{2})[_-](?P<minute>\d{2})(?:[_-](?P<second>\d{2}))?"
    ),
    re.compile(
        r"(?P<year>20\d{2}|19\d{2})(?P<month>\d{2})(?P<day>\d{2})"
        r"[_-]?(?P<hour>\d{2})(?P<minute>\d{2})(?P<second>\d{2})"
    ),
]


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
        f"{base_name}..json",
        f"{stem}.json",
        f"{base_name}.supplemental-metadata.json",
        f"{stem}.supplemental-metadata.json",
        f"{base_name}.supplemen.json",
        f"{stem}.supplemen.json",
    ]

    numbered_match = re.match(r"^(?P<name>.+?)\s*\((?P<num>\d+)\)$", stem)
    if numbered_match:
        orig_name = numbered_match.group("name")
        num = numbered_match.group("num")
        candidates.append(f"{orig_name}{path.suffix}({num}).json")
        candidates.append(f"{orig_name}({num}){path.suffix}.json")
        candidates.append(f"{orig_name}{path.suffix}({num}).supplemental-metadata.json")
        candidates.append(f"{orig_name}({num}){path.suffix}.supplemental-metadata.json")
        candidates.append(f"{orig_name}{path.suffix}.supplemental-metadata({num}).json")
        candidates.append(f"{orig_name}{path.suffix}({num}).supplemen.json")
        candidates.append(f"{orig_name}({num}){path.suffix}.supplemen.json")
        candidates.append(f"{orig_name}{path.suffix}.supplemen({num}).json")

    for candidate in candidates:
        json_path = dir_name / candidate
        if json_path.exists():
            return str(json_path)

    base_lower = base_name.lower()
    stem_lower = stem.lower()
    numbered_num = numbered_match.group("num") if numbered_match else None
    orig_base_lower = None
    if numbered_match:
        orig_base_lower = f"{numbered_match.group('name')}{path.suffix}".lower()

    search_dirs = [dir_name]
    json_dir = dir_name / "Json"
    if json_dir.exists():
        search_dirs.append(json_dir)

    for search_dir in search_dirs:
        for json_path in search_dir.glob("*.json"):
            json_name = json_path.name.lower()
            json_stem = json_path.stem.lower()
            if json_name in {f"{base_lower}.json", f"{base_lower}..json", f"{stem_lower}.json"}:
                return str(json_path)

            if base_lower.startswith(json_stem) and len(json_stem) >= 20:
                return str(json_path)

            if json_name.startswith(f"{base_lower}.supp"):
                return str(json_path)

            if json_name.startswith(f"{stem_lower}.") and ".supp" in json_name:
                return str(json_path)

            if orig_base_lower and numbered_num:
                number_token = f"({numbered_num})"
                orig_name_lower = numbered_match.group('name').lower()
                if json_name.startswith(f"{orig_base_lower}.supp") and number_token in json_name:
                    return str(json_path)
                if json_name.startswith(f"{orig_base_lower}{number_token}.supp"):
                    return str(json_path)
                if json_name.startswith(f"{orig_base_lower}{number_token}.json"):
                    return str(json_path)
                if json_name.startswith(f"{orig_name_lower}.") and ".supp" in json_name and number_token in json_name:
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


def is_takeout_metadata_json(json_path: Path) -> bool:
    """Returns True when a JSON file looks like Google Takeout photo metadata."""
    try:
        with open(json_path, 'r', encoding='utf-8') as file_handle:
            data = json.load(file_handle)
    except Exception:
        return False

    if not isinstance(data, dict):
        return False

    takeout_keys = {'photoTakenTime', 'creationTime', 'geoData', 'googlePhotosOrigin', 'imageViews'}
    return bool(takeout_keys.intersection(data.keys())) and 'title' in data


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

    suffix = Path(image_path).suffix.lower()
    if suffix not in PIEXIF_WRITABLE_FORMATS:
        logging.info("Skipping EXIF write for unsupported format %s: %s", suffix, image_path)
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


def get_safe_filename(target_dir: Path, base_name: str, ext: str, source_path: Optional[Path] = None) -> Path:
    """Returns a non-colliding file path by appending a counter if needed."""
    counter = 1
    new_path = target_dir / f"{base_name}{ext}"
    while new_path.exists():
        if source_path and str(new_path.resolve()) == str(source_path.resolve()):
            return new_path
        new_path = target_dir / f"{base_name}_{counter}{ext}"
        counter += 1
    return new_path


def parse_date_from_filename(path: Path) -> Optional[str]:
    """Extracts common camera/export timestamps embedded in filenames."""
    for pattern in FILENAME_DATE_PATTERNS:
        match = pattern.search(path.stem)
        if not match:
            continue

        second = match.groupdict().get("second") or "00"
        return (
            f"{match.group('year')}:{match.group('month')}:{match.group('day')} "
            f"{match.group('hour')}:{match.group('minute')}:{second}"
        )

    return None


def build_target_from_date(root_path: Path, source_path: Path, exif_date: Optional[str]) -> Tuple[Path, str]:
    if exif_date:
        try:
            date_part, time_part = exif_date.split(' ')
            year, month, day = date_part.split(':')
            hh, mm, ss = time_part.split(':')
            return root_path / year / month, f"{year}-{month}-{day}_{hh}-{mm}-{ss}"
        except Exception as error:
            logging.warning(f"Error parsing date {exif_date} for {source_path}: {error}")

    return root_path / "Sin_fecha", source_path.stem


def move_file(source_path: Path, target_path: Path) -> bool:
    """Moves a file without keeping the original path behind."""
    if str(target_path.resolve()) == str(source_path.resolve()):
        return True

    try:
        target_path.parent.mkdir(parents=True, exist_ok=True)
        original_size = source_path.stat().st_size
        shutil.move(str(source_path), str(target_path))
        if target_path.exists() and target_path.stat().st_size == original_size and not source_path.exists():
            return True

        logging.error(f"Failed to verify move for {target_path}")
    except Exception as error:
        logging.error(f"Error moving {source_path} to {target_path}: {error}")

    return False


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
        json_data = None
        if json_path_str:
            processed_jsons.add(json_path_str)
            json_data = parse_takeout_json(json_path_str)

        photo_path = Path(photo.path)
        exif_date = photo.exif_date or (json_data or {}).get('exif_date') or parse_date_from_filename(photo_path)
        target_dir, base_name = build_target_from_date(root_path, photo_path, exif_date)

        ext = photo_path.suffix
        new_path = get_safe_filename(target_dir, base_name, ext, photo_path)

        old_path = photo.path
        if move_file(photo_path, new_path):
            if old_path in cache:
                cache[str(new_path)] = cache.pop(old_path)
            photo.path = str(new_path)

    if update_cb:
        update_cb("Organizando videos por fecha (JSON detectado)...")

    video_paths = [
        path for path in root_path.rglob("*")
        if path.is_file() and path.suffix.lower() in SUPPORTED_VIDEO_FORMATS
    ]

    for video_path in video_paths:
        if not video_path.exists():
            continue

        json_path_str = find_takeout_json(str(video_path))
        json_data = None
        if json_path_str:
            processed_jsons.add(json_path_str)
            json_data = parse_takeout_json(json_path_str)

        videos_count += 1
        exif_date = (json_data or {}).get('exif_date') or parse_date_from_filename(video_path)
        target_dir, base_name = build_target_from_date(root_path, video_path, exif_date)
        new_path = get_safe_filename(target_dir, base_name, video_path.suffix, video_path)

        move_file(video_path, new_path)

    json_dir = root_path / "Json"
    for json_path in root_path.rglob("*.json"):
        try:
            if json_dir in json_path.parents:
                continue
            if str(json_path) not in processed_jsons and is_takeout_metadata_json(json_path):
                processed_jsons.add(str(json_path))
        except Exception as error:
            logging.error(f"Error checking orphan JSON {json_path}: {error}")

    if processed_jsons:
        json_dir.mkdir(parents=True, exist_ok=True)
        for json_path in processed_jsons:
            try:
                json_file = Path(json_path)
                if json_file.exists():
                    if json_dir in json_file.parents:
                        continue
                    new_json_path = get_safe_filename(json_dir, json_file.stem, json_file.suffix, json_file)
                    shutil.move(str(json_file), str(new_json_path))
            except Exception as error:
                logging.error(f"Error moving JSON {json_path}: {error}")

    return photos, videos_count, len(processed_jsons)
