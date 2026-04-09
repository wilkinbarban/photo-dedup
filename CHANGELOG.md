# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-04-09

### Added
- **Intelligent Duplicate Detection**: Find exact duplicates based on file size and content.
- **Visual Similarity Search**: Perceptual hashing (`imagehash`) support.
- **AI-Powered Analysis**: Deep learning similarity checks using `MobileNetV2` for extreme accuracy.
- **Google Takeout Integration**: Automatic metadata restoration (`photoTakenTime`, `geoData`, descriptions) via JSON parsing and `piexif`.
- **Media Organizer**: Automatic renaming (`YYYY-MM-DD_HH-MM-SS.ext`) and structuring into `/YYYY/MM/` directories.
- **Multilingual Support**: Fully translated interface in English, Spanish (Español), and Brazilian Portuguese (Português - Brasil).
- **Safe Deletion**: Duplicates are moved to the system's Recycle Bin/Trash instead of permanent deletion.
- **Real-Time Log Viewer**: Monitor progress, background tasks, and errors from the UI.
- **Summary & Controls**: Detailed summary panel post-analysis and dynamic navigation.
- **High Performance Processing**: Multiprocessing via `ProcessPoolExecutor` and cache system (`cache.json`, `embeddings.pkl`).

### Changed
- Initial release of the software as open-source under GPLv3.
