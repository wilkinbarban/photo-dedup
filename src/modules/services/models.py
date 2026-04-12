import os
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class PhotoInfo:
    """
    Data class representing information about a photo.

    Attributes:
        path (str): The absolute file path of the photo.
        size (int): File size in bytes.
        width (int): Image width in pixels.
        height (int): Image height in pixels.
        sharpness (float): Computed sharpness score of the image.
        phash (Optional[object]): Perceptual hash of the image.
        dhash (Optional[object]): Difference hash of the image.
        ahash (Optional[object]): Average hash of the image.
        img_small (Optional[object]): Downscaled, grayscale version of the image for SSIM comparison.
        has_exif (bool): Indicates if the image contains EXIF metadata.
        exif_date (Optional[str]): The original date extracted from EXIF metadata.
        score (float): A calculated quality score used to determine the best photo in a duplicate group.
    """
    path: str
    size: int = 0
    width: int = 0
    height: int = 0
    sharpness: float = 0.0
    phash: Optional[object] = None
    dhash: Optional[object] = None
    ahash: Optional[object] = None
    img_small: Optional[object] = None
    has_exif: bool = False
    exif_date: Optional[str] = None
    score: float = 0.0
    geo_data: Optional[dict] = None
    title: Optional[str] = None
    description: Optional[str] = None

    @property
    def megapixels(self) -> float:
        """
        Calculates the image resolution in megapixels.

        Returns:
            float: Megapixels of the image.
        """
        return (self.width * self.height) / 1_000_000

    @property
    def filename(self) -> str:
        """
        Gets the base filename from the image path.

        Returns:
            str: The base filename.
        """
        return os.path.basename(self.path)

    @property
    def size_mb(self) -> float:
        """
        Calculates the file size in megabytes.

        Returns:
            float: File size in MB.
        """
        return self.size / (1024 * 1024)


@dataclass
class DuplicateGroup:
    """
    Data class representing a group of duplicate or similar photos.

    Attributes:
        photos (list): List of PhotoInfo objects in this group.
        similarity (float): The average similarity score percentage of the group.
        best_index (int): Index of the photo in the `photos` list with the highest quality score.
        root_folder (str): The root folder where the search was performed.
    """
    photos: list = field(default_factory=list)
    similarity: float = 0.0
    best_index: int = 0
    root_folder: str = ""
    match_type: str = "similar (hash)"


@dataclass
class Statistics:
    """
    Data class to hold statistics about the duplicate analysis process.

    Attributes:
        total_photos (int): Total number of photos analyzed.
        total_groups (int): Total number of duplicate groups found.
        total_size_mb (float): Total size of all photos in megabytes.
        duplicate_size_mb (float): Total size of all photos within duplicate groups in megabytes.
        recoverable_mb (float): Amount of space in megabytes that could be recovered by deleting duplicates.
        avg_similarity (float): Average similarity score across all groups.
        by_format (dict): Dictionary storing statistics grouped by file format.
        total_videos (int): Total number of videos analyzed.
        json_generated (bool): Indicates if JSON files were processed/generated.
    """
    total_photos: int = 0
    total_groups: int = 0
    total_size_mb: float = 0.0
    duplicate_size_mb: float = 0.0
    recoverable_mb: float = 0.0
    avg_similarity: float = 0.0
    by_format: dict = field(default_factory=dict)
    total_videos: int = 0
    json_generated: bool = False
