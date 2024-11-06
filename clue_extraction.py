import os
from dotenv import load_dotenv
import pytesseract
import cv2
import numpy as np

load_dotenv()

tesseract_path = os.getenv('TESSERACT_PATH')
if not tesseract_path:
    print("Error: TESSERACT_PATH is missing in .env. Please run setup.sh to configure.")
    exit(1)
pytesseract.pytesseract.tesseract_cmd = tesseract_path

    
def process_image(image):
    target_rgb = np.uint8([[[235, 238, 247]]])
    bounding_boxes = find_color_blocks(image, target_rgb)
    if len(bounding_boxes) == 0:
        return [], []
    
    top_clues, side_clues = separate_clues(bounding_boxes)
    return extract_numbers_for_top(image, top_clues), extract_numbers_for_side(image, side_clues)

def find_color_blocks(image, color_rgb):
    target_hsv = cv2.cvtColor(color_rgb, cv2.COLOR_RGB2HSV)[0][0]
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    color_mask = cv2.inRange(hsv_image, target_hsv, target_hsv)
    color_mask = cv2.morphologyEx(color_mask, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    contours, _ = cv2.findContours(color_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return [cv2.boundingRect(contour) for contour in contours if cv2.contourArea(contour) > 10]

def separate_clues(bounding_boxes):
    top_clues = [box for box in bounding_boxes if box[3] > box[2]]
    side_clues = [box for box in bounding_boxes if box[2] >= box[3]]
    top_clues.sort(key=lambda box: box[0])
    side_clues.sort(key=lambda box: box[1])
    return top_clues, side_clues

def estimate_gap_width(side_clues, image):
    gap_widths = []
    for (x, y, w, h) in side_clues:
        cropped_image = image[y:y + h, x:x + w]
        gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        vertical_projection = np.sum(binary, axis=0)
        gap_indices = np.where(vertical_projection == 0)[0]
        prev_idx = gap_indices[0] if len(gap_indices) > 0 else 0
        gap_size = 1
        for idx in gap_indices[1:]:
            if idx - prev_idx == 1:
                gap_size += 1
            else:
                if gap_size > 0:
                    gap_widths.append(gap_size)
                gap_size = 1 
            prev_idx = idx
        if gap_size > 0:
            gap_widths.append(gap_size)
    return max(set(gap_widths), key=gap_widths.count) * .8


image_folder = 'proc_images'

def preprocess_segment(segment, padding=20):
    # Convert to grayscale
    gray_segment = cv2.cvtColor(segment, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur to reduce noise
    blurred_segment = cv2.GaussianBlur(gray_segment, (3, 3), 0)
    
    # Threshold the image to binary (black text on white background)
    _, thresh_segment = cv2.threshold(blurred_segment, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    # Find contours of the text
    contours, _ = cv2.findContours(thresh_segment, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Get bounding box for all contours (text region)
    x, y, w, h = cv2.boundingRect(np.vstack(contours))
    cropped_segment = gray_segment[y:y+h, x:x+w]
    
    # Add white padding around the cropped segment
    padded_segment = cv2.copyMakeBorder(cropped_segment, padding, padding, padding, padding, cv2.BORDER_CONSTANT, value=255)
    
    return padded_segment

def extract_numbers_for_top(image, top_clues):
    extracted_numbers = []
    for (x, y, w, h) in top_clues:
        cropped_image = image[y:y + h, x:x + w]
        processed_image = preprocess_segment(cropped_image)
        ocr_result = pytesseract.image_to_string(processed_image, config='--psm 6 digits')
        
        numbers = [int(s) for s in ocr_result.split() if s.isdigit()]
        extracted_numbers.append(numbers)
    return extracted_numbers

def extract_numbers_for_side(image, side_clues):
    gap_width = estimate_gap_width(side_clues, image)
    extracted_numbers = []
    for (x, y, w, h) in side_clues:
        cropped_image = image[y:y + h, x:x + w]
        segments = split_side_clue_image(cropped_image, gap_width - 1)
        numbers = []
        for segment in segments:
            processed_segment = preprocess_segment(segment)
            ocr_result = pytesseract.image_to_string(processed_segment, config='--psm 10 digits')
            segment_numbers = [int(s) for s in ocr_result.split() if s.isdigit()]
            numbers.extend(segment_numbers)
        extracted_numbers.append(numbers)
    return extracted_numbers

def split_side_clue_image(image, gap_width):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    vertical_projection = np.sum(binary, axis=0)
    gap_indices = np.where(vertical_projection == 0)[0]
    split_images = []
    prev_idx = 0
    gap_size = 0
    for idx in range(1, len(gap_indices)):
        if gap_indices[idx] - gap_indices[idx - 1] == 1:
            gap_size += 1
        else:
            if gap_size >= gap_width:
                segment = image[:, prev_idx:gap_indices[idx - gap_size]]
                if segment.shape[1] > 1:
                    split_images.append(segment)
                prev_idx = gap_indices[idx - gap_size]
            gap_size = 1
    if prev_idx < image.shape[1]:
        segment = image[:, prev_idx:]
        if segment.shape[1] > 1:
            split_images.append(segment)
    return split_images