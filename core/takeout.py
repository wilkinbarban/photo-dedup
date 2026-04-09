import os
import json
import logging
import shutil
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Tuple

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

    # Potential JSON names
    candidates = [
        f"{base_name}.json",             # e.g., IMG_1234.jpg.json
        f"{stem}.json",                  # e.g., IMG_1234.json
        f"{base_name}.supplemen.json",   # e.g., IMG_1234.jpg.supplemen.json
        f"{stem}.supplemen.json",        # e.g., IMG_1234.supplemen.json
    ]
    
    # Handle duplicates like IMG_1234 (1).jpg -> IMG_1234.jpg(1).json
    if " (" in stem and stem.endswith(")"):
        # e.g. stem = "IMG_1234 (1)", suffix = ".jpg"
        parts = stem.rsplit(" (", 1)
        if len(parts) == 2:
            orig_name = parts[0]
            num = parts[1][:-1] # remove the ')'
            candidates.append(f"{orig_name}{path.suffix}({num}).json")
            candidates.append(f"{orig_name}({num}){path.suffix}.json")
            candidates.append(f"{orig_name}{path.suffix}({num}).supplemen.json")
            candidates.append(f"{orig_name}({num}){path.suffix}.supplemen.json")

    for cand in candidates:
        json_path = dir_name / cand
        if json_path.exists():
            return str(json_path)
            
    return None

def parse_takeout_json(json_path: str) -> Optional[dict]:
    """
    Reads and parses a Google Takeout JSON file.
    Extracts relevant metadata like photoTakenTime, geoData, title, description.
    """
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        result = {}
        
        # Extract timestamp
        if 'photoTakenTime' in data and 'timestamp' in data['photoTakenTime']:
            timestamp = int(data['photoTakenTime']['timestamp'])
            # Convert to EXIF format: YYYY:MM:DD HH:MM:SS
            from datetime import timezone
            dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
            result['exif_date'] = dt.strftime('%Y:%m:%d %H:%M:%S')
            
        # Extract Geo Data
        if 'geoData' in data:
            geo = data['geoData']
            lat = geo.get('latitude', 0.0)
            lon = geo.get('longitude', 0.0)
            alt = geo.get('altitude', 0.0)
            if lat != 0.0 or lon != 0.0:
                result['geo_data'] = {'latitude': lat, 'longitude': lon, 'altitude': alt}
                
        # Extract title and description
        if 'title' in data:
            result['title'] = data['title']
        if 'description' in data:
            result['description'] = data['description']
            
        return result
    except Exception as e:
        logging.error(f"Error parsing Takeout JSON {json_path}: {e}")
        return None

def float_to_rational(value: float) -> Tuple[int, int]:
    """Converts a float to a rational number format used by EXIF."""
    return (int(value * 10000), 10000)

def convert_to_degrees(value: float) -> Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int]]:
    """Converts a decimal degree to degrees, minutes, seconds for EXIF."""
    d = int(value)
    m = int((value - d) * 60)
    s = (value - d - m / 60) * 3600.0
    return ((d, 1), (m, 1), (int(s * 10000), 10000))

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
            # File is not supported by piexif or has no EXIF
            exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}, "thumbnail": None}
            
        # 1. Write DateTimeOriginal if missing
        has_exif_date = piexif.ExifIFD.DateTimeOriginal in exif_dict.get('Exif', {})
        if not has_exif_date and 'exif_date' in json_data:
            date_str = json_data['exif_date'].encode('utf-8')
            exif_dict.setdefault('Exif', {})[piexif.ExifIFD.DateTimeOriginal] = date_str
            exif_dict.setdefault('0th', {})[piexif.ImageIFD.DateTime] = date_str
            modified = True
            
        # 2. Write GPS Data if missing and available in JSON
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
            
        # Optional: Write Description if missing
        has_desc = piexif.ImageIFD.ImageDescription in exif_dict.get('0th', {})
        if 'description' in json_data and not has_desc:
            if json_data['description']:
                exif_dict.setdefault('0th', {})[piexif.ImageIFD.ImageDescription] = json_data['description'].encode('utf-8')
                modified = True
                
        if modified:
            try:
                exif_bytes = piexif.dump(exif_dict)
                piexif.insert(exif_bytes, image_path)
                logging.info(f"Successfully enriched EXIF for {image_path} with Takeout JSON")
                return True
            except Exception as e:
                logging.error(f"Error saving EXIF for {image_path}: {e}")
                return False
                
    except Exception as e:
        logging.error(f"Error checking/updating EXIF for {image_path}: {e}")
        
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
    
    # Check if ANY JSON file exists in the directory tree
    has_jsons = any(root_path.rglob("*.json"))
    if not has_jsons:
        return photos, 0, 0

    logging.info("Takeout JSON files detected. Starting intelligent organization...")
    
    if update_cb:
        update_cb("Organizando archivos por fecha (JSON detectado)...")

    processed_jsons = set()
    videos_count = 0
    
    for i, p in enumerate(photos):
        json_path_str = find_takeout_json(p.path)
        if json_path_str:
            processed_jsons.add(json_path_str)
            
            # Determine target folder and base name based on EXIF date
            if p.exif_date:
                try:
                    # Expected format: 'YYYY:MM:DD HH:MM:SS'
                    date_part, time_part = p.exif_date.split(' ')
                    year, month, day = date_part.split(':')
                    hh, mm, ss = time_part.split(':')
                    
                    target_dir = root_path / year / month
                    base_name = f"{year}-{month}-{day}_{hh}-{mm}-{ss}"
                except Exception as e:
                    logging.warning(f"Error parsing date {p.exif_date} for {p.path}: {e}")
                    target_dir = root_path / "Sin_fecha"
                    base_name = Path(p.path).stem
            else:
                target_dir = root_path / "Sin_fecha"
                base_name = Path(p.path).stem
                
            target_dir.mkdir(parents=True, exist_ok=True)
            ext = Path(p.path).suffix
            new_path = get_safe_filename(target_dir, base_name, ext)
            
            # Only move if the path is actually different
            if str(new_path.resolve()) != str(Path(p.path).resolve()):
                try:
                    # Safe move: copy2, verify, remove original
                    shutil.copy2(p.path, new_path)
                    if new_path.exists() and new_path.stat().st_size == Path(p.path).stat().st_size:
                        os.remove(p.path)
                        
                        # Update cache keys
                        if p.path in cache:
                            cache[str(new_path)] = cache.pop(p.path)
                            
                        # Update PhotoInfo path
                        p.path = str(new_path)
                    else:
                        logging.error(f"Failed to verify copy for {new_path}")
                except Exception as e:
                    logging.error(f"Error moving {p.path} to {new_path}: {e}")
                    
    # Process videos (similar logic but they aren't part of the photos list)
    if update_cb:
        update_cb("Organizando videos por fecha (JSON detectado)...")
        
    for root, _, files in os.walk(root_path):
        # Skip internal organized folders if you want, but it's okay since we check for json
        for f in files:
            vp = Path(root) / f
            if vp.suffix.lower() in SUPPORTED_VIDEO_FORMATS:
                json_path_str = find_takeout_json(str(vp))
                if json_path_str:
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
                        except Exception as e:
                            logging.warning(f"Error parsing date {json_data['exif_date']} for {vp}: {e}")
                            target_dir = root_path / "Sin_fecha"
                            base_name = vp.stem
                    else:
                        target_dir = root_path / "Sin_fecha"
                        base_name = vp.stem
                        
                    target_dir.mkdir(parents=True, exist_ok=True)
                    new_path = get_safe_filename(target_dir, base_name, vp.suffix)
                    
                    if str(new_path.resolve()) != str(vp.resolve()):
                        try:
                            shutil.copy2(str(vp), new_path)
                            if new_path.exists() and new_path.stat().st_size == vp.stat().st_size:
                                os.remove(str(vp))
                            else:
                                logging.error(f"Failed to verify copy for {new_path}")
                        except Exception as e:
                            logging.error(f"Error moving {vp} to {new_path}: {e}")

    # Move all processed JSONs to /Json/ folder
    if processed_jsons:
        json_dir = root_path / "Json"
        json_dir.mkdir(parents=True, exist_ok=True)
        for jp in processed_jsons:
            try:
                jp_path = Path(jp)
                if jp_path.exists():
                    new_jp = get_safe_filename(json_dir, jp_path.stem, jp_path.suffix)
                    shutil.move(str(jp_path), str(new_jp))
            except Exception as e:
                logging.error(f"Error moving JSON {jp}: {e}")
                
    return photos, videos_count, len(processed_jsons)
