# iOS Nonogram.com Solver

A macOS-based tool to automate the solving of nonogram puzzles, specifically designed for puzzles on the **Nonogram.com** app. Utilizing the iPhone Mirroring feature introduced in macOS Sequoia (2024) and iOS 18, this project captures clues from the mirrored display, interprets them, and fills in the solution directly on your iPhone.

## Demo

![Project Demo](docs/project_demo.gif)

## Features

- **Integrated iPhone Mirroring**: Utilizes macOS Sequoia’s iPhone Mirroring feature to allow direct interaction with puzzles displayed on your iPhone.
- **Supports Nonogram.com App**: Currently designed specifically for the **Nonogram.com** app, leveraging unique app characteristics for accurate interpretation.
- **Automated Puzzle Solving**: Captures and interprets clues from screenshots and automatically fills in the solution.
  
### Example Output

> **Note:** Below is a sample output showing the detected clues and the final puzzle solution format.

```plaintext
Screenshot taken.
Top Clues: [[3], [3], [3, 3], [1, 1, 1, 1], [4, 2], [1, 1, 3], [8, 1], [1, 1, 3], [4, 1, 1], [1, 1, 3]]
Side Clues: [[1], [7], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 5], [1, 1, 1, 1], [2, 1], [9], [2, 2, 1, 1], [2, 5]]
                1             
                1   1   1 4 1 
              3 1 4 1 8 1 1 1 
          3 3 3 1 2 3 1 3 1 3 
        ┌────────────────────
      1 │ ⨯ ⨯ ⨯ ⨯ ⨯ ⨯ ■ ⨯ ⨯ ⨯ 
      7 │ ⨯ ⨯ ⨯ ■ ■ ■ ■ ■ ■ ■ 
1 1 1 1 │ ⨯ ⨯ ■ ⨯ ■ ⨯ ■ ⨯ ■ ⨯ 
1 1 1 1 │ ⨯ ⨯ ■ ⨯ ■ ⨯ ■ ⨯ ■ ⨯ 
  1 1 5 │ ■ ⨯ ■ ⨯ ■ ■ ■ ■ ■ ⨯ 
1 1 1 1 │ ■ ⨯ ⨯ ■ ⨯ ⨯ ■ ⨯ ⨯ ■ 
    2 1 │ ■ ■ ⨯ ⨯ ⨯ ⨯ ■ ⨯ ⨯ ⨯ 
      9 │ ⨯ ■ ■ ■ ■ ■ ■ ■ ■ ■ 
2 2 1 1 │ ⨯ ■ ■ ⨯ ■ ■ ⨯ ■ ⨯ ■ 
    2 5 │ ⨯ ⨯ ■ ■ ⨯ ■ ■ ■ ■ ■ 
Puzzle solved successfully!
```


## Getting Started

### Prerequisites

- **macOS Sequoia** (2024) or later and **iOS 18** or later
- **Nonogram.com** app installed on your iPhone
- **Python 3.8+**
- **Tesseract OCR**
- **CMake** (for building C++ extensions)

### Setup

1. Clone the repository:

```bash
git clone https://github.com/matteo-psnt/ios-nonogramcom-solver.git
cd ios-nonogramcom-solver
```

2. Run the setup script:

```bash
chmod +x setup.sh
./setup.sh
```

3. Activate the virtual environment (if not already activated):

```bash
source .venv/bin/activate
```

## Usage

1. Ensure your iPhone is mirrored to your macOS display with the Nonogram.com app open.

2. Run the solver:

```bash
python main.py
```

## Technical Overview

This tool combines several techniques:

- **Tesseract OCR**: Detects and extracts puzzle clues from screenshots.
- **Computer Vision (OpenCV)** Identifies color blocks and interprets the clues visually.
- **C++ Extension:** Implements optimized line-solving logic in C++ via Pybind11 for efficient puzzle solving.

### Known Issues and Limitations

- Tool fails to detect clues for Expert-level puzzles.
- Detection may fail with very small puzzle grids or high clue densities.
- Puzzle-solving logic is currently tailored to puzzles with integer clues; symbol-based or color-based nonograms are unsupported.

## Troubleshooting

1. **Tesseract OCR Not Installed**: Install Tesseract and add it to your PATH:

      ```bash
      brew install tesseract
      ```

2. **cmake is not installed**: If missing, install CMake with:

      ```bash
      brew install cmake
      ```

3. **C++ Extension Build Fails**: Delete the build directory, then retry the build. You may need to install Xcode Command Line Tools:

     ```bash
     xcode-select --install
     ```

4. **Screen Detection Issues**: Ensure the iPhone screen is set as the primary display, visible, and unobstructed.

5. **Clue Detection Issues**: Try increase iPhone screen size using:  `⌘ +` to improve clue detection.
