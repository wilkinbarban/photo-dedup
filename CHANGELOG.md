# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- _No changes yet._

### Changed
- _No changes yet._

### Fixed
- _No changes yet._

### Documentation
- _No changes yet._

## [1.0.10] - 2026-04-12

### Fixed
- **Dual-release CI reliability**: Prevented cleanup lock failures between `full` and `lite` builds by running `-Clean` only for the first variant in `scripts/build_variants.ps1`.
- **Smoke-test stability**: Added retry logic in `scripts/build_windows.ps1` when the executable exits early on first launch (transient onefile startup behavior in CI).
- **Cleanup robustness**: Added retry loop for removing `dist` during clean builds to avoid transient file-handle errors on Windows runners.

## [1.0.9] - 2026-04-12

### Added
- **Dual build automation**: Added `scripts/build_variants.ps1` to generate `full` and `lite` Windows builds in one command, run smoke tests, and write a comparison report in JSON.

### Changed
- **Release artifacts (dual assets)**: Release pipeline now publishes both variants (`PhotoDedup-full.exe` / `PhotoDedup-lite.exe`) and their ZIP packages.
- **Build script telemetry**: `scripts/build_windows.ps1` now supports integrated smoke testing and writes build metrics JSON files.
- **Packaging flavors**: `PhotoDedup.spec` now supports `full` and `lite` modes using `PHOTO_DEDUP_BUILD_FLAVOR`.

### Fixed
- **Lite runtime resilience**: Added fallback to hash-only detection when AI dependencies are unavailable in lite builds.

## [1.0.8] - 2026-04-12

### Fixed
- **Application startup invocation**: Restored explicit `main()` execution guard in `src/main/photo_dedup.py` (`if __name__ == "__main__": main()`), preventing silent exit on launch.

## [1.0.7] - 2026-04-12

### Fixed
- **Runtime import bootstrap**: Added startup path bootstrap in `src/main/photo_dedup.py` to guarantee `src.*` imports resolve correctly when launching the entrypoint directly and in frozen runtime.

### Changed
- **Release reliability**: Updated CI triggers so release build and smoke-test workflows run from tag-based publication flow without GitHub token event-chaining issues.

## [1.0.6] - 2026-04-12

### Added
- **Canonical src architecture**: Introduced `src/main`, `src/modules`, and `src/interfaces` as the final runtime structure, with `src/main/photo_dedup.py` as the canonical app entrypoint.
- **Maintenance script namespace**: Moved maintenance utilities to `scripts/maintenance/` (`update_analyzer.py`, `update_texts.py`) to keep the project root clean.

### Changed
- **Packaging and CI path alignment**: Updated `PhotoDedup.spec`, `scripts/build_windows.ps1`, and `.github/workflows/publish-release-from-tag.yml` to resolve version/build entrypoint from `src/main/photo_dedup.py`.
- **Installer/runtime commands**: Updated installer and release docs to launch the app via `python src/main/photo_dedup.py`.

### Fixed
- **Legacy module removal**: Removed compatibility wrappers and deleted deprecated `core/` and `ui/` trees after migration validation.

### Documentation
- Updated `README.md`, `CONTRIBUTING.md`, `RELEASE.md`, and `RELEASE.template.md` to reflect the final `src/`-based structure and commands.

## [1.0.5] - 2026-04-12

### Changed
- **Release asset policy**: `install_secure.ps1` is no longer attached as a GitHub Release asset; release uploads now include only `PhotoDedup.exe` and `PhotoDedup-vX.Y.Z-windows.zip`.
- **README secure installer source**: Updated secure install commands (ES/EN/PT) to fetch `install_secure.ps1` from the repository source (`raw.githubusercontent.com`) instead of release assets.

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
