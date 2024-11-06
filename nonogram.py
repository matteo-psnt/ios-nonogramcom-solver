import sys
import numpy as np
import time

sys.path.append('build')
import line_solver  # type: ignore

def to_hex(n: int) -> str:
    return chr(n + 48) if n < 10 else chr(n + 87) if n < 36 else chr(n + 29)

class Nonogram:
    def __init__(self, top_clues, side_clues, board=None):
        self.top_clues = top_clues
        self.side_clues = side_clues
        self.n_rows, self.n_cols = len(side_clues), len(top_clues)
        self.top_wdt = max(len(i) for i in top_clues)
        self.side_wdt = max(len(i) for i in side_clues)
        self.board = np.zeros((self.n_rows, self.n_cols), dtype=int) if board is None else board

    def __str__(self) -> str:
        board_lines = []
        for i in range(self.top_wdt, 0, -1):
            line = '  ' * self.side_wdt + '  '
            for j in self.top_clues:
                line += to_hex(j[-i]).lstrip('0x') + ' ' if len(j) >= i else '  '
            board_lines.append(line)
        board_lines.append('  ' * self.side_wdt + '┌' + '──' * self.n_cols)
        for j in range(self.n_rows):
            line = ''.join(to_hex(self.side_clues[j][-i]).lstrip('0x') + ' ' if len(self.side_clues[j]) >= i else '  ' for i in range(self.side_wdt, 0, -1))
            line += '│ ' + ''.join('  ' if sqr == 0 else '■ ' if sqr == 1 else '⨯ ' for sqr in self.board[j])
            board_lines.append(line)
        return '\n'.join(board_lines)

    def solve(self, verbose=False):
        first_run = True
        changed = True
        while changed:
            changed = False
            for i in range(self.n_rows):
                row = self.board[i, :]
                solved_row = line_solver.fill_in_line(self.side_clues[i], row)
                if not np.array_equal(row, solved_row) and len(solved_row) == len(row):
                    self.board[i, :] = solved_row
                    changed = True
                    if verbose:
                        self._update_console(first_run)
                        first_run = False
            for j in range(self.n_cols):
                col = self.board[:, j]
                solved_col = line_solver.fill_in_line(self.top_clues[j], col)
                if not np.array_equal(col, solved_col) and len(solved_col) == len(col):
                    self.board[:, j] = solved_col
                    changed = True
                    if verbose:
                        self._update_console(first_run)
                        first_run = False

    def _update_console(self, first_run=False):
        if not first_run:
            lines = len(str(self).split('\n'))
            print(f"\033[{lines}F", end='')
        print(self)
        time.sleep(0.001)
    
    def is_valid_board(self):
        return self._check_clue_sums() and self._check_clue_lengths()

    def _check_clue_sums(self):
        return sum(sum(clue) for clue in self.side_clues) == sum(sum(clue) for clue in self.top_clues)

    def _check_clue_lengths(self):
        return all(sum(clue) + len(clue) - 1 <= self.n_cols for clue in self.side_clues) and all(sum(clue) + len(clue) - 1 <= self.n_rows for clue in self.top_clues)
    
    def is_solved(self):
        return np.all(self.board != 0)