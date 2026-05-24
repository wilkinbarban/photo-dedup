# Security Policy

## Scope

PhotoDedup is an educational Windows desktop project for local photo-library analysis. It is not a cloud service and does not require accounts, remote storage, or external scanning APIs.

## Supported Versions

Use the latest GitHub Release unless you are intentionally testing development builds:

https://github.com/wilkinbarban/photo-dedup/releases/latest

## Reporting a Security Issue

If you find a vulnerability or a behavior that could cause data loss, please open a private report or contact:

- Author: Wilkin Barban Rosabal
- Email: wilkin.barban@gmail.com

Please include:

- affected version or commit,
- operating system,
- exact steps to reproduce,
- expected behavior,
- observed behavior,
- whether real files were moved, deleted, or modified.

## Local Data Handling

PhotoDedup works on files selected by the user. The app may create local cache, config, history, and embeddings files under the user application-data directory. These files are used to speed up analysis and keep an audit trail of duplicate-resolution actions.

## File Safety

- Duplicate actions are review-first: users choose which files to keep.
- The UI supports moving duplicates to a `duplicados` folder.
- Delete actions prefer the system recycle bin through `send2trash` when available.
- Some file operations can partially succeed; the UI reports per-file failures when possible.

## Windows SmartScreen

Current release executables are not code-signed. Windows may report them as unknown publisher apps. Always download from the official GitHub Releases page and avoid binaries redistributed by third parties.

## Educational Purpose

This project demonstrates PyQt6 desktop development, local image analysis, packaging, release automation, and resilient error handling. Use it only with photo libraries you own or are authorized to manage.
