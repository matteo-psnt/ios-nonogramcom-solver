#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <vector>
#include <algorithm>  // Include for std::equal

using Line = std::vector<int>;
using Clues = std::vector<int>;

Line fillInLine(const Clues& clues, const Line& existingLine) {
    Line currentLine(existingLine.size(), 0);
    Line consistentLine;
    consistentLine.reserve(existingLine.size());

    std::function<void(size_t, size_t)> findConsistentLine = [&](size_t clueIndex, size_t position) {
        if (clueIndex == clues.size()) {
            for (size_t i = 0; i < currentLine.size(); ++i) {
                if (currentLine[i] == 0) {
                    currentLine[i] = -1;
                }
            }

            // Improved matching logic using std::equal
            bool isMatch = std::equal(
                currentLine.begin(), currentLine.end(), existingLine.begin(),
                [](int current, int existing) {
                    return existing == 0 || existing == current;
                }
            );

            if (isMatch) {
                if (consistentLine.empty()) {
                    consistentLine = currentLine;
                } else {
                    for (size_t i = 0; i < currentLine.size(); ++i) {
                        if (consistentLine[i] != currentLine[i]) {
                            consistentLine[i] = 0;  // Mark as unknown if inconsistent
                        }
                    }
                }
            }
            return;
        }

        int clueLength = clues[clueIndex];
        size_t remainingSpace = currentLine.size() - position;
        size_t minRequiredLength = clueLength + (clues.size() - clueIndex - 1);
        if (remainingSpace < minRequiredLength) return;

        for (size_t i = position; i + clueLength <= currentLine.size(); ++i) {
            for (size_t j = 0; j < clueLength; ++j) {
                currentLine[i + j] = 1;
            }

            if (i + clueLength < currentLine.size()) {
                currentLine[i + clueLength] = -1;
            }

            // Improved segment matching logic
            bool segmentMatch = std::equal(
                currentLine.begin() + i, currentLine.begin() + i + clueLength,
                existingLine.begin() + i,
                [](int current, int existing) {
                    return existing == 0 || existing == current;
                }
            );

            if (segmentMatch) {
                findConsistentLine(clueIndex + 1, i + clueLength + 1);
            }

            for (size_t j = 0; j < clueLength; ++j) {
                currentLine[i + j] = 0;
            }

            if (i + clueLength < currentLine.size()) {
                currentLine[i + clueLength] = 0;
            }
        }
    };

    findConsistentLine(0, 0);
    return consistentLine;
}

// Create a Python module using pybind11
PYBIND11_MODULE(line_solver, m) {
    m.def("fill_in_line", &fillInLine, "Fill in line based on clues and existing line");
}
