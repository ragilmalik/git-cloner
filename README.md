# 🚀 RagilmalikGitCloner

> **"I got 99 problems but manually cloning Git repos ain't one."**

![Status](https://img.shields.io/badge/Status-Gold_Master-FFD700?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge&logo=windows)
![Vibe](https://img.shields.io/badge/Vibe-Immaculate-ff69b4?style=for-the-badge)

---

## 🧐 The Origin Story

Picture this: I'm sitting there, staring at a spreadsheet containing 50 different GitHub URLs. My project manager wants the code. My hands want to *not* type `git clone` 50 times.

I realized I had two choices:
1.  Succumb to the repetitive stress injury and lose my mind.
2.  Build a tool so over-engineered and beautiful that it solves the problem forever.

I made **one**. It's not just a script; it's a statement. It's a portable, dark-mode, batch-processing beast that carries its own Git engine in its pocket.

---

## ✨ Features That Slap

*   **Portable Engine**: It bundles `MinGit`. It doesn't care if you have Git installed. It brings its own party.
*   **Batch Operations**: Feed it `.txt`, `.csv`, `.xlsx` files, or just copy-paste a mess of URLs. It devours them.
*   **Anti-Crash Logic**: Duplicate folder? We don't crash. We rename it (`repo_updated_DATE`). We adapt. We overcome.
*   **The "Boss Report"**: Generates a fully styled, dark-themed Excel report. Bold headers. Borders. Professionalism.
*   **UI That Purrs**: Cyan/Black aesthetics. Focus-aware scrolling. Progress bars that shift color like a mood ring (Red -> Green).

---

## 📂 The Anatomy (Source Tree)

For the curious developers who want to peek under the hood. Here is how I structured this masterpiece:

```text
RagilmalikGitCloner/
├── src/
│   ├── main_gui.py           # The Brain. Handles the UI, threading, and event loop.
│   ├── git_operations.py     # The Muscle. Talks to the git binary and moves files.
│   ├── report_generator.py   # The Accountant. Stylizes that sweet Excel report.
│   ├── url_parser.py         # The Detective. Hunts down URLs in messy text files.
│   ├── git_config.py         # The Navigator. Finds where we hid the portable git.
│   └── error_handler.py      # The Diplomat. Tells you what went wrong nicely.
├── assets/                   # Icons and pretty things.
├── git_portable/             # The secret weapon. A mini Git installation (MinGit).
├── build.bat                 # The "Make it work" button (Build script).
├── build_exe.spec            # The PyInstaller recipe.
└── download_mingit.py        # Fetches the engine if you lost it.
```

---

## 🧠 How It Works (The Logic)

You might think, "It's just a wrapper for git clone." **Wrong.** It's a symphony of logic.

1.  **Input Parsing**: When you load a file, `url_parser.py` uses Regex to scrape legitimate GitHub URLs, ignoring your grocery list that you accidentally pasted in the text file.
2.  **The Engine Swap**: `git_config.py` performs a runtime check. "Is Git installed?" No? "Is the portable folder here?" Yes. It effectively hot-swaps the system PATH variable for the sub-process so the app uses *our* Git, not yours.
3.  **Non-Blocking UI**: The cloning happens in a daemon thread (`main_gui.py`). This means while the app is doing heavy lifting, the window remains responsive. You can scroll, minimize, or just admire the progress bar.
4.  **Smart Reporting**: We don't just dump text. `report_generator.py` uses `pandas` and `openpyxl` to craft a native `.xlsx` file with cell formatting, color themes, and auto-adjusted column widths.

---

## 🎮 The Manual (For Humans)

### 1. Installation
You don't install it. You **unleash** it.
1.  Download the release zip.
2.  **Extract it**. (Do not run from inside the zip, or I will judge you).
3.  Keep the `git_portable` folder next to the executable. They are soulmates.
4.  Double-click `RagilmalikGitCloner.exe`.

### 2. Usage
*   **Choose File**: Pick a list. We support almost anything text-based.
*   **Manual Input**: Paste links directly. One per line.
*   **Destination**: Tell it where the code goes.
*   **Settings**: Adjust the delay slider if you don't want GitHub to think you're a DDoS attack (5 seconds is safe).
*   **Execute**: Click **Start**. Watch the magic.

---

## 🛠️ Developer Guide (Build it yourself)

So you want to modify perfection? Bold. Here is how you do it.

**Prerequisites**: Python 3.10+. That's it.

### Step 1: The Setup
Get the code and the engine.
```bash
pip install -r requirements.txt
python download_mingit.py  # This grabs the portable git binary for you
```

### Step 2: Run from Source
```bash
python src/main_gui.py
```

### Step 3: The Build
I wrote a script so you don't have to remember PyInstaller flags.
```bash
build.bat
```
This runs the spec file, bundles the assets, bundles the Git environment, and spits out a standalone `.exe` in the `dist` folder.

---

## 🚑 Troubleshooting

**Q: "It says Permission Denied!"**
A: You have the Excel report open. Close it. The code is powerful, but it cannot fight Windows file locks.

**Q: "It says Git Not Found!"**
A: You moved the `.exe` away from the `git_portable` folder. Put them back together. They need to be in the same folder.

**Q: "Why is this app so cool?"**
A: Because I made it.

---

## 📜 License

Open source. Use it. Clone it.
Just remember who saved you from typing `git clone` 500 times.

**Ragilmalik**
*Automating the boring stuff with style.*
