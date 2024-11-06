import Quartz
import mss
import cv2
import numpy as np
from Quartz.CoreGraphics import (
    CGEventCreateMouseEvent, kCGEventLeftMouseDown, kCGEventLeftMouseUp,
    kCGEventMouseMoved, kCGMouseButtonLeft, CGEventPost, kCGHIDEventTap
)

def get_scaling_factors():
    """Calculate scaling factors between the main display and screenshot resolution."""
    # Get main display resolution
    main_display = Quartz.CGMainDisplayID()
    screen_width = Quartz.CGDisplayPixelsWide(main_display)
    screen_height = Quartz.CGDisplayPixelsHigh(main_display)
    
    with mss.mss() as sct:
        monitor = sct.monitors[0]  # The primary monitor
        screenshot = sct.grab(monitor)
        screenshot_width, screenshot_height = screenshot.width, screenshot.height

    # Calculate scaling factors
    scaling_factor_x = screen_width / screenshot_width
    scaling_factor_y = screen_height / screenshot_height
    
    return screen_width, screen_height, scaling_factor_x, scaling_factor_y

screen_width, screen_height, scaling_factor_x, scaling_factor_y = get_scaling_factors()

def scale_coordinates(x, y):
    """Scale x and y coordinates based on screen-to-screenshot scaling factors."""
    return x * scaling_factor_x, y * scaling_factor_y

def click_at(x, y):
    """Simulate a click at the given screen coordinates, scaled for the current screen."""
    scaled_x, scaled_y = scale_coordinates(x, y)
    for event in [kCGEventMouseMoved, kCGEventLeftMouseDown, kCGEventLeftMouseUp]:
        CGEventPost(kCGHIDEventTap, CGEventCreateMouseEvent(None, event, (scaled_x, scaled_y), kCGMouseButtonLeft))


def take_screenshot():
    """Capture a screenshot of the full screen."""
    with mss.mss() as sct:
        monitor = {"top": 0, "left": 0, "width": screen_width, "height": screen_height}
        screenshot = sct.grab(monitor)
        return cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGRA2BGR)

def find_color_blocks(image, color_rgb):
    """Find blocks of a specific color in the image and return bounding rectangles."""
    target_hsv = cv2.cvtColor(color_rgb, cv2.COLOR_RGB2HSV)[0][0]
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    color_mask = cv2.inRange(hsv_image, target_hsv, target_hsv)
    color_mask = cv2.morphologyEx(color_mask, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    contours, _ = cv2.findContours(color_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return [cv2.boundingRect(contour) for contour in contours if cv2.contourArea(contour) > 10]
