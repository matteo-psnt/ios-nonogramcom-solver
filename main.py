import time
import cv2
import numpy as np
from image_utils import take_screenshot, click_at
from clue_extraction import find_color_blocks, process_image, separate_clues
from nonogram import Nonogram

def fill_in_solution(image, nonogram):
    target_rgb = np.uint8([[[235, 238, 247]]])
    bounding_boxes = [box for box in find_color_blocks(image, target_rgb) if box[2] > 10 and box[3] > 10]
    top_clue_boxes, side_clue_boxes = separate_clues(bounding_boxes)
    top_centers = [x + w // 2 for x, y, w, h in top_clue_boxes]
    side_centers = [y + h // 2 for x, y, w, h in side_clue_boxes]

    if len(top_centers) != nonogram.n_cols or len(side_centers) != nonogram.n_rows:
        print("Error: The number of detected clues does not match the nonogram dimensions.")
        return

    for row in range(nonogram.n_rows):
        for col in range(nonogram.n_cols):
            if nonogram.board[row, col] == 1:
                x, y = top_centers[col], side_centers[row]
                click_at(x, y)
                time.sleep(0.001)
                click_at(x, y)


if __name__ == "__main__":
    screenshot = take_screenshot()
    print("Screenshot taken.")
    
    top_clues, side_clues = process_image(screenshot)
    
    if top_clues == [] or side_clues == []:
        print("Error: No clues detected. Please ensure the iPhone emulator is visible on your screen and that the Nonogram.com app is open.")
        exit()
        
    print("Top Clues:", top_clues)
    print("Side Clues:", side_clues)
        
    if not all(top_clues) or not all(side_clues):
        print("Error: Invalid clues detected.")
        exit()
    
    
    nonogram = Nonogram(top_clues, side_clues)
    
    if not nonogram.is_valid_board():
        print("Error: Invalid board.")
        exit()
    
    nonogram.solve()
    print(nonogram)
    
    if nonogram.is_solved():
        print("Puzzle solved successfully!")
        fill_in_solution(screenshot, nonogram)
        
        # Second pass for larger puzzles to ensure all cells are filled in
        if nonogram.n_cols > 10 or nonogram.n_rows > 10:
            fill_in_solution(screenshot, nonogram)
        
    else:
        print("Puzzle could not be solved.")