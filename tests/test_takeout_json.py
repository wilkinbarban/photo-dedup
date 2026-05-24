import json
import tempfile
import unittest
from pathlib import Path

from PIL import Image

from src.modules.services.models import PhotoInfo
from src.modules.services.takeout import enrich_image_with_json, find_takeout_json, organize_takeout_photos


class TakeoutJsonTests(unittest.TestCase):
    def test_finds_google_takeout_supplemental_metadata_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            image_path = root / "photo.jpg"
            json_path = root / "photo.jpg.supplemental-metadata.json"
            image_path.write_bytes(b"fake image bytes")
            json_path.write_text("{}", encoding="utf-8")

            self.assertEqual(find_takeout_json(str(image_path)), str(json_path))

    def test_organizes_photo_and_json_when_supplemental_metadata_is_present(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            image_path = root / "photo.jpg"
            json_path = root / "photo.jpg.supplemental-metadata.json"
            image_path.write_bytes(b"fake image bytes")
            json_path.write_text(
                json.dumps({"photoTakenTime": {"timestamp": "1704067200"}}),
                encoding="utf-8",
            )

            photo = PhotoInfo(path=str(image_path), exif_date="2024:01:01 00:00:00")
            photos, videos_count, json_count = organize_takeout_photos([photo], str(root), {})

            moved_photo = root / "2024" / "01" / "2024-01-01_00-00-00.jpg"
            moved_json = root / "Json" / "photo.jpg.supplemental-metadata.json"

            self.assertEqual(videos_count, 0)
            self.assertEqual(json_count, 1)
            self.assertEqual(photos[0].path, str(moved_photo))
            self.assertTrue(moved_photo.exists())
            self.assertTrue(moved_json.exists())
            self.assertFalse(image_path.exists())
            self.assertFalse(json_path.exists())

    def test_skips_heic_exif_write_without_error_log(self):
        try:
            import pillow_heif
        except ImportError:
            self.skipTest("pillow-heif is not installed")

        pillow_heif.register_heif_opener()

        with tempfile.TemporaryDirectory() as tmp:
            image_path = Path(tmp) / "photo.HEIC"
            Image.new("RGB", (32, 24), color=(80, 120, 160)).save(image_path, format="HEIF")

            with self.assertNoLogs(level="ERROR"):
                enriched = enrich_image_with_json(
                    str(image_path),
                    {
                        "exif_date": "2024:01:01 00:00:00",
                        "geo_data": {"latitude": 18.5, "longitude": -69.9, "altitude": 12.0},
                        "description": "heic metadata",
                    },
                )

            self.assertFalse(enriched)


if __name__ == "__main__":
    unittest.main()
