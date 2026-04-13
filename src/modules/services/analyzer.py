import functools
import logging
import multiprocessing
import os
import threading
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from pathlib import Path
from typing import Optional

import cv2
import imagehash
import numpy as np
from PIL import Image
from PyQt6.QtCore import QThread, pyqtSignal

from src.modules.config.i18n import get_text
from src.modules.config.state import (
    load_cache,
    load_embeddings_cache,
    save_cache,
    save_embeddings_cache,
)
from src.modules.services.models import DuplicateGroup, PhotoInfo, Statistics
from src.modules.services.takeout import (
    enrich_image_with_json,
    find_takeout_json,
    organize_takeout_photos,
    parse_takeout_json,
)

SUPPORTED_FORMATS = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', '.webp', '.heic', '.heif'}


def compute_score(info: PhotoInfo) -> float:
    """
    Computes a quality score for the photo based on megapixels, sharpness, size, and EXIF presence.

    Args:
        info (PhotoInfo): The photo information object.

    Returns:
        float: The calculated quality score.
    """
    score = 0.0
    score += min(info.megapixels * 10, 40)
    score += min(info.sharpness / 100, 30)
    score += min(info.size_mb * 5, 20)
    score += 10 if info.has_exif else 0
    return score


def analyze_photo_task(path: str, cached: Optional[dict] = None) -> tuple:
    """
    Standalone function to analyze a single photo. Designed to run in a separate process
    to avoid blocking the main thread and to bypass the Python GIL.

    Args:
        path (str): The file path of the photo.
        cached (dict, optional): Cached information about the photo, if available.

    Returns:
        tuple: (path (str), info (Optional[PhotoInfo]), new_cache_entry (Optional[dict]))
    """
    try:
        json_path = find_takeout_json(path)
        json_data = None
        if json_path:
            json_data = parse_takeout_json(json_path)
            if json_data:
                enrich_image_with_json(path, json_data)

        if cached is not None:
            try:
                if os.path.getmtime(path) == cached.get('mtime'):
                    info = PhotoInfo(path=path)
                    info.size = cached.get('size', 0)
                    info.width = cached.get('width', 0)
                    info.height = cached.get('height', 0)
                    info.sharpness = cached.get('sharpness', 0.0)
                    info.has_exif = cached.get('has_exif', False)
                    info.exif_date = cached.get('exif_date')
                    info.score = cached.get('score', 0.0)

                    if json_data:
                        info.geo_data = json_data.get('geo_data')
                        info.title = json_data.get('title')
                        info.description = json_data.get('description')
                        if not info.exif_date and 'exif_date' in json_data:
                            info.exif_date = json_data['exif_date']

                    return (path, info, None)
            except Exception:
                pass

        info = PhotoInfo(path=path)

        if json_data:
            info.geo_data = json_data.get('geo_data')
            info.title = json_data.get('title')
            info.description = json_data.get('description')
            if 'exif_date' in json_data:
                info.exif_date = json_data['exif_date']

        info.size = os.path.getsize(path)
        mtime = os.path.getmtime(path)

        with open(path, 'rb') as file_handle:
            raw_bytes = file_handle.read()

        img_rgb = None
        rotation_angle = 0

        try:
            import io
            with Image.open(io.BytesIO(raw_bytes)) as img:
                info.width, info.height = img.size
                img_rgb = img.convert('RGB')
                img_rgb = img_rgb.copy()

                try:
                    exif = img._getexif()
                    info.has_exif = exif is not None and len(exif) > 0
                    if exif:
                        from PIL.ExifTags import TAGS
                        for tag, value in exif.items():
                            tag_name = TAGS.get(tag)
                            if tag_name == 'DateTimeOriginal':
                                info.exif_date = str(value)
                            elif tag_name == 'Orientation':
                                rotation_angle = value
                except Exception:
                    info.has_exif = False

        except Exception:
            try:
                img_bytes_arr = np.frombuffer(raw_bytes, dtype=np.uint8)
                img_cv_color = cv2.imdecode(img_bytes_arr, cv2.IMREAD_COLOR)
                if img_cv_color is not None:
                    img_cv_rgb = cv2.cvtColor(img_cv_color, cv2.COLOR_BGR2RGB)
                    height, width = img_cv_rgb.shape[:2]
                    info.width, info.height = width, height
                    img_rgb = Image.fromarray(img_cv_rgb)
                else:
                    return (path, None, None)
            except Exception:
                return (path, None, None)

        if img_rgb is None:
            return (path, None, None)

        if rotation_angle in [3, 4, 5, 6, 7, 8]:
            try:
                if rotation_angle == 3:
                    img_rgb = img_rgb.rotate(180)
                elif rotation_angle == 6:
                    img_rgb = img_rgb.rotate(270)
                elif rotation_angle == 8:
                    img_rgb = img_rgb.rotate(90)
            except Exception:
                pass

        info.phash = imagehash.phash(img_rgb, hash_size=16)
        info.dhash = imagehash.dhash(img_rgb, hash_size=16)
        info.ahash = imagehash.average_hash(img_rgb, hash_size=16)

        thumb = img_rgb.resize((64, 64), Image.LANCZOS).convert('L')
        info.img_small = np.array(thumb, dtype=np.float32)

        try:
            img_bytes_arr = np.frombuffer(raw_bytes, dtype=np.uint8)
            img_cv = cv2.imdecode(img_bytes_arr, cv2.IMREAD_GRAYSCALE)
            if img_cv is not None:
                info.sharpness = cv2.Laplacian(img_cv, cv2.CV_64F).var()
            else:
                gray = np.array(img_rgb.convert('L'), dtype=np.float64)
                info.sharpness = cv2.Laplacian(gray, cv2.CV_64F).var()
        except Exception:
            info.sharpness = 0.0

        info.score = compute_score(info)

        new_cache_entry = {
            'mtime': mtime,
            'size': info.size,
            'width': info.width,
            'height': info.height,
            'sharpness': info.sharpness,
            'has_exif': info.has_exif,
            'exif_date': info.exif_date,
            'score': info.score,
        }

        return (path, info, new_cache_entry)

    except Exception as error:
        logging.error(f"Error analyzing {path}: {error}")
        return (path, None, None)


class AnalysisWorker(QThread):
    """
    Worker thread responsible for analyzing photos and finding duplicates.
    It runs in the background to avoid freezing the main UI.

    Signals:
        progress (int, str): Emits the current progress percentage and a status message.
        finished (list, dict): Emits the list of DuplicateGroup objects found and extra statistics.
        error (str): Emits an error message if an exception occurs.
    """

    progress = pyqtSignal(int, str)
    finished = pyqtSignal(list, dict)
    error = pyqtSignal(str)

    def __init__(self, folder: str, threshold: int = 10, duplicate_mode: str = "similar", use_ai: bool = False, ai_level: str = "balanced"):
        """
        Initializes the analysis worker.

        Args:
            folder (str): The root folder path to scan for photos.
            threshold (int, optional): The similarity threshold (lower is stricter). Defaults to 10.
            duplicate_mode (str, optional): The search mode ("exact" or "similar"). Defaults to "similar".
            use_ai (bool): Whether to use AI for duplicate detection.
            ai_level (str): The AI strictness level ("fast", "balanced", "deep").
        """
        super().__init__()
        self.folder = folder
        self.threshold = threshold
        self.duplicate_mode = duplicate_mode
        self.use_ai = use_ai
        self.ai_level = ai_level
        self._stop = False
        self._paused = False
        self.paused_lock = threading.Lock()
        self.embeddings_cache = {}
        self.ai_model = None

    def stop(self) -> None:
        """Flags the worker to stop the analysis process."""
        self._stop = True

    def pause(self) -> None:
        """Flags the worker to pause the analysis process."""
        self._paused = True

    def resume(self) -> None:
        """Resumes the analysis process."""
        self._paused = False

    def _wait_if_paused(self) -> None:
        """Blocks execution while the worker is paused and not stopped."""
        while self._paused and not self._stop:
            time.sleep(0.1)

    def run(self) -> None:
        """
        Main execution method for the thread. Performs finding, analyzing,
        and grouping duplicate photos.
        """
        try:
            logging.info(f"Starting analysis in '{self.folder}' with mode '{self.duplicate_mode}' and threshold {self.threshold}.")
            cache = load_cache()
            self.embeddings_cache = load_embeddings_cache()

            if self.use_ai:
                self.progress.emit(0, get_text("msg_load_ai"))
                try:
                    from src.modules.services.ai_model import PhotoAIAnalyzer
                    self.ai_model = PhotoAIAnalyzer.get_instance()
                except Exception as error:
                    logging.warning(f"AI unavailable, falling back to hash-only mode: {error}")
                    self.use_ai = False
                    self.ai_model = None

            self.progress.emit(0, get_text("msg_search_img"))
            all_files = []
            for root, _, files in os.walk(self.folder):
                for file_name in files:
                    if Path(file_name).suffix.lower() in SUPPORTED_FORMATS:
                        all_files.append(os.path.join(root, file_name))

            total = len(all_files)
            if total == 0:
                logging.warning("No images found in the selected folder.")
                self.error.emit("No images found in the selected folder.")
                return

            logging.info(f"Found {total} supported images to analyze.")
            self.progress.emit(5, get_text("msg_analyzing").format(total=total))

            start_time = time.time()
            caches = [cache.get(file_path) for file_path in all_files]

            with ProcessPoolExecutor(max_workers=min(multiprocessing.cpu_count(), 8)) as executor:
                results = list(executor.map(analyze_photo_task, all_files, caches))

            photos = []
            for path, info, new_cache_entry in results:
                if info:
                    photos.append(info)
                if new_cache_entry:
                    cache[path] = new_cache_entry

            save_cache(cache)

            analyze_time = time.time() - start_time
            logging.info(f"Successfully analyzed {len(photos)} images in {analyze_time:.2f} seconds using multiple cores.")
            self.progress.emit(60, get_text("msg_analyzed").format(n=len(photos)))

            def update_org_progress(msg: str):
                self.progress.emit(60, msg)

            photos, videos_count, jsons_count = organize_takeout_photos(photos, self.folder, cache, update_cb=update_org_progress)
            save_cache(cache)

            self.progress.emit(60, get_text("msg_comparing"))
            groups = self._find_duplicates(photos)

            if self.use_ai:
                save_embeddings_cache(self.embeddings_cache)

            logging.info(f"Analysis complete. Found {len(groups)} duplicate groups.")
            self.progress.emit(95, get_text("msg_found_groups").format(n=len(groups)))
            self.finished.emit(groups, {"videos": videos_count, "jsons": jsons_count > 0, "total_photos": len(photos)})

        except Exception as error:
            logging.error(f"Analysis error: {error}", exc_info=True)
            self.error.emit(str(error))

    def _are_duplicates(self, a: PhotoInfo, b: PhotoInfo) -> tuple[bool, float, str]:
        """
        Determines if two photos are duplicates based on the selected mode and threshold.

        Args:
            a (PhotoInfo): The first photo.
            b (PhotoInfo): The second photo.

        Returns:
            tuple[bool, float, str]: A boolean indicating if they are duplicates, their similarity percentage, and match type.
        """
        if self.duplicate_mode == "exact":
            if a.size == b.size:
                try:
                    if (a.phash - b.phash) == 0:
                        return True, 100.0, "exacta"
                except Exception:
                    pass
            return False, 0.0, ""

        threshold = self.threshold * 2

        phash_diff = float('inf')
        dhash_diff = float('inf')
        ahash_diff = float('inf')

        votes = 0
        try:
            phash_diff = a.phash - b.phash
            if phash_diff <= threshold:
                votes += 1
        except Exception:
            pass
        try:
            dhash_diff = a.dhash - b.dhash
            if dhash_diff <= threshold:
                votes += 1
        except Exception:
            pass
        try:
            ahash_diff = a.ahash - b.ahash
            if ahash_diff <= threshold:
                votes += 1
        except Exception:
            pass

        use_ai_check = False
        is_dup_hash = False
        sim_hash = 0.0

        if votes >= 2:
            is_dup_hash = True

        if a.img_small is not None and b.img_small is not None and is_dup_hash:
            try:
                array_a = a.img_small / 255.0
                array_b = b.img_small / 255.0
                mu_a = array_a.mean()
                mu_b = array_b.mean()
                sig_a = array_a.std()
                sig_b = array_b.std()
                sig_ab = ((array_a - mu_a) * (array_b - mu_b)).mean()
                c1, c2 = 0.01**2, 0.03**2
                ssim = ((2 * mu_a * mu_b + c1) * (2 * sig_ab + c2)) / ((mu_a**2 + mu_b**2 + c1) * (sig_a**2 + sig_b**2 + c2))
                ssim = float(ssim)

                ssim_min = 0.85 - (self.threshold - 2) * (0.25 / 18)

                if ssim < ssim_min:
                    is_dup_hash = False
                else:
                    sim_hash = round(ssim * 100, 1)
            except Exception:
                sim_hash = float(votes) / 3.0 * 100
        elif is_dup_hash:
            sim_hash = float(votes) / 3.0 * 100

        if a.exif_date and b.exif_date and a.exif_date == b.exif_date:
            sim_hash = min(sim_hash + 10, 100)

        if self.use_ai and self.ai_model:
            if self.ai_level == "deep" and votes >= 1 and not is_dup_hash:
                use_ai_check = True
            elif is_dup_hash and sim_hash < 95.0:
                use_ai_check = True

        if use_ai_check:
            emb_a = self.embeddings_cache.get(a.path)
            if emb_a is None:
                emb_a = self.ai_model.get_embedding(a.path)
                if emb_a is None:
                    emb_a = np.zeros(1280)
                self.embeddings_cache[a.path] = emb_a

            emb_b = self.embeddings_cache.get(b.path)
            if emb_b is None:
                emb_b = self.ai_model.get_embedding(b.path)
                if emb_b is None:
                    emb_b = np.zeros(1280)
                self.embeddings_cache[b.path] = emb_b

            ai_sim = self.ai_model.compute_similarity(emb_a, emb_b)
            ai_sim_pct = round(ai_sim * 100, 1)

            if ai_sim_pct >= 90.0:
                return True, max(sim_hash, ai_sim_pct), "similar (IA)"
            elif ai_sim_pct < 80.0 and is_dup_hash:
                if self.ai_level == "deep":
                    return False, 0.0, ""

        if is_dup_hash:
            return True, sim_hash, "similar (hash)"

        return False, 0.0, ""

    def _find_duplicates(self, photos: list[PhotoInfo]) -> list[DuplicateGroup]:
        """
        Finds groups of duplicate photos from a list of analyzed photos.

        Args:
            photos (list[PhotoInfo]): The list of analyzed photos.

        Returns:
            list[DuplicateGroup]: A list of groups, where each group contains duplicate photos.
        """
        groups = []
        if not photos:
            return groups

        if self.duplicate_mode == "exact":
            from collections import defaultdict
            exact_groups = defaultdict(list)

            for photo in photos:
                hash_key = str(photo.phash) if photo.phash is not None else "no_hash"
                key = (photo.size, hash_key)
                exact_groups[key].append(photo)

            for _, group_photos in exact_groups.items():
                if self._stop:
                    return groups
                self._wait_if_paused()

                if len(group_photos) > 1:
                    best_idx = max(range(len(group_photos)), key=lambda index: group_photos[index].score)
                    group = DuplicateGroup(
                        photos=group_photos,
                        similarity=100.0,
                        best_index=best_idx,
                        root_folder=self.folder,
                        match_type="exacta",
                    )
                    groups.append(group)

            return groups

        for photo in photos:
            try:
                photo._ahash_int = int(str(photo.ahash), 16)
            except Exception:
                photo._ahash_int = None

        total_photos = len(photos)
        visited = set()
        max_diff = self.threshold * 4

        for index in range(total_photos):
            if self._stop:
                return groups
            self._wait_if_paused()

            if index in visited:
                continue

            pct = 60 + int((index / total_photos) * 35)
            self.progress.emit(pct, get_text("msg_comparing_n").format(i=index + 1, n=total_photos))

            group_members = [index]
            group_similarities = [100.0]
            group_match_types = []
            photo_i = photos[index]

            for other_index in range(index + 1, total_photos):
                if other_index in visited:
                    continue

                photo_j = photos[other_index]

                if photo_i._ahash_int is not None and photo_j._ahash_int is not None:
                    try:
                        diff = (photo_i._ahash_int ^ photo_j._ahash_int).bit_count()
                    except AttributeError:
                        diff = bin(photo_i._ahash_int ^ photo_j._ahash_int).count('1')

                    local_max_diff = max_diff + 10 if (self.use_ai and self.ai_level == "deep") else max_diff
                    if diff > local_max_diff:
                        continue

                is_dup, sim, match_type = self._are_duplicates(photo_i, photo_j)
                if is_dup:
                    group_members.append(other_index)
                    group_similarities.append(sim)
                    group_match_types.append(match_type)
                    visited.add(other_index)

            if len(group_members) > 1:
                visited.add(index)
                group_photos = [photos[group_index] for group_index in group_members]
                avg_sim = sum(group_similarities) / len(group_similarities)
                best_idx = max(range(len(group_photos)), key=lambda group_index: group_photos[group_index].score)

                final_match_type = "similar (hash)"
                if "similar (IA)" in group_match_types:
                    final_match_type = "similar (IA)"

                group = DuplicateGroup(
                    photos=group_photos,
                    similarity=avg_sim,
                    best_index=best_idx,
                    root_folder=self.folder,
                    match_type=final_match_type,
                )
                groups.append(group)

        return groups
