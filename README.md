# Live AreaTranslator (macOS)

A real-time screen translation app for macOS. Select any area on your screen, and it will continuously capture, OCR, and translate the text — displaying results in a floating overlay.

## Download

**No Python installation required.** Download the pre-built app, unzip, and double-click to launch.

👉 **[Download Latest Release](https://github.com/rryunosuke0055-wq/Live-AreaTranslator2/releases/latest)**

> After downloading, if macOS shows "app can't be opened", right-click the app → Open → Open.

> 🪟 Looking for the **Windows version**? → [Live AreaTranslator for Windows](https://github.com/rryunosuke0055-wq/Live-AreaTranslator-Windows)

## Features

- **Drag-to-Select** — Draw a rectangle over any region of your screen to start live translation.
- **Real-Time Updates** — Continuously captures the selected area, detects text changes via image diffing, and re-translates only when content changes.
- **Native macOS OCR** — Uses Apple's Vision framework for fast and accurate text recognition. No external OCR engine required.
- **10 Languages Supported** — Japanese, English, Korean, Chinese, Spanish, French, German, Italian, Portuguese, and Russian, with auto-detection for the source language.
- **Floating Overlay** — Translated text appears in a semi-transparent, always-on-top overlay that you can freely drag and resize.
- **Customizable Settings** — Adjust font size, toggle light/dark theme, and control capture speed (1–30 FPS).
- **Multi-Monitor Support** — Works across multiple displays.

## How It Works

1. Launch the app and choose source/target languages (or leave source as "Auto Detect").
2. Click **"📷 Drag to Select Area & Start Live Translation"**.
3. Draw a rectangle around the text you want to translate.
4. The translated text appears in a floating overlay just below the selected area.
5. Close the overlay with the **✖** button to return to the home screen and select a new area.

## Tech Stack

| Layer | Technology |
|---|---|
| GUI | PySide6 (Qt for Python) |
| Screen Capture | mss + OpenCV |
| OCR | Apple Vision Framework (macOS native) |
| Translation | Google Translate via deep-translator |
| Language | Python 3.10+ |

## For Developers

### Requirements

- macOS 10.15 (Catalina) or later
- Python 3.10+

### Run from Source

```bash
git clone https://github.com/rryunosuke0055-wq/Live-AreaTranslator2.git
cd Live-AreaTranslator2

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

python main.py
```

### Build the .app Yourself

```bash
pip install pyinstaller
pyinstaller build_mac.spec --noconfirm

# Sign the app
xattr -cr "dist/Live AreaTranslator.app"
codesign --force --deep --sign - "dist/Live AreaTranslator.app"
```

The built app will be in `dist/Live AreaTranslator.app`.

## Project Structure

```
├── main.py                  # Entry point
├── build_mac.spec           # PyInstaller build config
├── capture/
│   └── screen_capture.py    # Screen capture & image diffing (mss + OpenCV)
├── ocr/
│   └── text_extractor.py    # OCR (Vision framework) & translation
├── worker/
│   └── capture_worker.py    # Background thread: capture → OCR → translate loop
├── ui/
│   ├── home_window.py       # Main home screen UI
│   ├── selection_window.py  # Full-screen drag-to-select overlay
│   ├── translation_overlay.py  # Floating translation result overlay
│   ├── overlay_manager.py   # Coordinates selection, overlay, and worker lifecycle
│   └── settings_modal.py    # Settings dialog (font size, theme, FPS)
└── requirements.txt
```

## License

MIT
