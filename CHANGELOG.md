# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- _No changes yet._

### Changed
- **Release asset policy**: `install_secure.ps1` is no longer attached as a GitHub Release asset; release uploads now include only `PhotoDedup.exe` and `PhotoDedup-vX.Y.Z-windows.zip`.
- **README secure installer source**: Updated secure install commands (ES/EN/PT) to fetch `install_secure.ps1` from the repository source (`raw.githubusercontent.com`) instead of release assets.

### Fixed
- _No changes yet._

### Documentation
- _No changes yet._

## [1.0.4] - 2026-04-12

### Added
- **Standalone EXE release asset**: The release workflow now uploads `PhotoDedup.exe` directly for non-technical users.

### Changed
- **PyInstaller packaging mode**: Switched from folder-based (`onedir`) output to single-file (`onefile`) output so the app is distributed as one executable with bundled runtime dependencies.
- **Build and smoke-test paths**: Updated build scripts and smoke-test workflow to validate `dist/PhotoDedup.exe`.

### Documentation
- Updated README (ES/EN/PT) to mention direct `PhotoDedup.exe` download option.

## [1.0.3] - 2026-04-11

### Added
- **Windows EXE smoke test workflow**: Added `.github/workflows/smoke-test-exe.yml` to verify executable startup and controlled shutdown on Windows runners.
- **Stable secure installer channel**: Release pipeline now publishes `install_secure.ps1` as a release asset in addition to the Windows ZIP.

### Changed
- **README secure installer commands**: Switched to the stable release channel URL (`releases/latest/download/install_secure.ps1`) in English, Portuguese, and Spanish sections.

### Documentation
- **Windows EXE download guidance**: Added multilingual “Download Windows EXE” sections with direct link to latest GitHub release assets.

## [1.0.2] - 2026-04-10

### Added
- **Windows build automation**: Added `scripts/build_windows.ps1` to compile and package `PhotoDedup.exe` into a release ZIP artifact.
- **PyInstaller project spec**: Added `PhotoDedup.spec` for reproducible Windows GUI builds.
- **Release CI workflow**: Added `.github/workflows/build-release-exe.yml` to build and upload Windows ZIP assets automatically on published releases.

### Documentation
- Added multilingual **Download Windows EXE** sections in README linking directly to latest GitHub Releases for non-technical users.
- Updated secure installer guidance to use the known-good pinned installer URL in README.

## [1.0.1] - 2026-04-10

### Added
- **One-liner installer (`install.ps1`)**: Allows downloading and running the project setup directly from PowerShell without requiring Git.
- **Secure installer (`install_secure.ps1`)**: Adds safer setup flow with host checks, connectivity validation, download retry logic, ZIP header validation, SHA-256 calculation, optional hash enforcement, and temp cleanup.
- **Versioned release support in PowerShell installers**: Both `install.ps1` and `install_secure.ps1` now support custom release ZIP URLs and custom install folder names (`RepoZipUrl`, `InstallFolderName`).

### Changed
- **Installer UX language**: `install_dependencies.bat` messages were translated to English for consistent onboarding.
- **Post-install behavior**: `install_dependencies.bat` now launches `photo_dedup.py` automatically after successful dependency installation.
- **Desktop path handling**: PowerShell installers now resolve the actual Windows Desktop directory (including redirected folders such as OneDrive Desktop).

### Fixed
- **Python detection flow in batch installer**: Improved Python bootstrap and PATH session handling in `install_dependencies.bat`.
- **Security prompt compatibility**: README one-liner commands now include `-UseBasicParsing` to avoid legacy web parser prompts.
- **In-memory execution compatibility**: `install_secure.ps1` now handles execution via `iwr ... | iex` without failing signature checks when no local script path exists.

### Documentation
- Added multilingual **Quick Install** sections (English, Portuguese, Spanish) to README.
- Documented secure installation in both quick and standard installation sections.
- Added practical secure examples with versioned release ZIP and expected SHA-256.
- Pinned secure installer documentation to a known-good commit to reduce cache-related issues.

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
