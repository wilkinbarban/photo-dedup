# PhotoDedup

PhotoDedup is an intelligent duplicate photo finder and automated media organizer. Built with Python and PyQt6, it not only detects exact and similar duplicate images but also integrates deeply with Google Takeout JSON files to restore lost EXIF metadata and organize your photo and video library automatically.

## 🚀 Features

*   **Intelligent Duplicate Detection**:
    *   Find exact duplicates based on file size and content.
    *   Find visually similar images using perceptual hashing (`imagehash`).
    *   Advanced AI-powered similarity checks using `MobileNetV2` for extreme accuracy.
*   **Google Takeout Integration**:
    *   Automatically associates `*.json` or `*.supplemen.json` files with your photos and videos.
    *   Restores essential metadata: `photoTakenTime` (DateTimeOriginal), `geoData` (GPS coordinates), and descriptions directly into the image's EXIF data.
*   **Real-Time Log Viewer**:
    *   Monitor the analysis progress, background tasks, and errors in real-time directly from the application's UI with a dedicated log console.
*   **Final Summary & Dynamic Controls**:
    *   After analysis, a detailed summary panel displays the total images and videos processed, duplicates found, and whether JSON files were generated.
    *   Dynamic context-aware buttons guide you smoothly (e.g., "Continue" if duplicates are found, or "Back" if none exist).
*   **Automatic Media Organizer**:
    *   If Google Takeout JSON files are detected, PhotoDedup will automatically rename your files to a standard format (`YYYY-MM-DD_HH-MM-SS.ext`).
    *   Moves organized photos and videos into structured directories: `/YYYY/MM/`.
    *   Safely moves processed JSON files to a dedicated `/Json/` folder to clean up the workspace.
*   **Safe Deletion**:
    *   Duplicates are moved to the system's Recycle Bin/Trash, preventing accidental permanent loss.
*   **Multilingual Interface**:
    *   Available in English, Spanish (Español), and Brazilian Portuguese (Português - Brasil). The language is selected at application startup.
*   **High Performance**:
    *   Utilizes multiple CPU cores via `ProcessPoolExecutor` to analyze thousands of images rapidly.
    *   Includes built-in caching (`cache.json` and `embeddings.pkl`) to speed up subsequent scans.

## 📦 Installation

### Requirements

*   Python 3.8 or higher.

### Steps

1.  Clone this repository:
    ```bash
    git clone https://github.com/wilkinbarban/photo-dedup
    cd photo-dedup
    ```

2.  Install dependencies:
    *   **On Windows**: You can simply run `install_dependencies.bat`.
    *   **Manual installation**:
        ```bash
        pip install -r requirements.txt
        ```
    *   *Dependencies include:* `PyQt6`, `Pillow`, `imagehash`, `opencv-python`, `numpy`, `pillow-heif`, `send2trash`, `piexif`, `torch`, `torchvision`.

## 💻 Usage

1.  Run the application:
    ```bash
    python photo_dedup.py
    ```
2.  Select your preferred language at startup.
3.  Select the root folder containing your images, videos, and (optionally) Google Takeout JSON files.
4.  Choose your settings:
    *   **Mode**: Exact or Similar.
    *   **Threshold**: How strict the similarity match should be.
    *   **AI Level**: Use Deep Learning models to refine results (Fast, Balanced, Deep).
5.  Click **"Start"**.

### 🛠 How the System Works

*   **JSON Processing & EXIF**: When analyzing a photo (e.g., `IMG_1234.jpg`), the system searches for a matching JSON file (like `IMG_1234.jpg.json` or `IMG_1234.supplemen.json`). If found, it parses the Google Takeout metadata and embeds it securely back into the image using `piexif`.
*   **File Organization**: After restoring metadata, files are evaluated for their creation date. They are then renamed and safely moved to an intuitive `/Year/Month/` folder structure. Any processed JSON is archived away so you are left with a perfectly clean media folder.
*   **Duplicate Detection**: Hashing algorithms (Average Hash, Perceptual Hash, Difference Hash) compute differences. For ambiguous cases, a deep learning model (`MobileNetV2`) extracts feature embeddings to calculate high-dimensional similarity, ensuring incredibly accurate deduplication.

## ☕ Support the Project

This project is completely free and open-source. However, if you find it useful and it has saved you time or recovered precious memories, you can voluntarily support its development! 

In the application's main screen, you'll find a **"Buy me a coffee"** button. Clicking it will display a PayPal QR code that you can scan to make a voluntary donation. Your support is greatly appreciated and helps keep the project alive!

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!
Feel free to check [issues page](https://github.com/wilkinbarban/photo-dedup/issues).

## 📝 License

This project is licensed under the **GNU General Public License v3.0 (GPLv3)**.

You are free to use, modify, and distribute this software, provided that any derivative work is also distributed under the same GPLv3 license. See the [LICENSE](LICENSE) file for more details.

---

*Disclaimer: While this software includes safeguards like moving files to the trash instead of permanently deleting them, always make sure you have a backup of your precious photos before running automated deduplication or organization tools.*