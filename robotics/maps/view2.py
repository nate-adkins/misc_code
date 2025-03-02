import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog

# Hide Tkinter root window
root = tk.Tk()
root.withdraw()

# Load image
file_path = filedialog.askopenfilename(filetypes=[("PNG Images", "*.png")])
if not file_path:
    print("No file selected. Exiting.")
    exit()

image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
if image is None:
    print("Error: Could not load image.")
    exit()

# Map coordinates
Xmin, Ymin, Xmax, Ymax = -110.842703, 38.364678, -110.696422, 38.460551
pixelWidth, pixelHeight = image.shape[1], image.shape[0]

# Screen setup
screen_w, screen_h = 800, 667
zoom_factor = 1.0
zoom_step = 0.1
x_offset, y_offset = 0.0, 0.0
mouse_x, mouse_y = 0, 0
dragging = False
start_x, start_y = 0, 0

def pixel_to_latlong(px, py):
    """Convert pixel coordinates to latitude and longitude."""
    long = Xmin + (px / pixelWidth) * (Xmax - Xmin)
    lat = Ymax - (py / pixelHeight) * (Ymax - Ymin)
    return lat, long

def display_image():
    """Displays the zoomed and panned image."""
    global x_offset, y_offset, zoom_factor

    # Compute the zoomed region
    zoom_w = pixelWidth / zoom_factor
    zoom_h = pixelHeight / zoom_factor
    x_offset = max(0, min(x_offset, pixelWidth - zoom_w))
    y_offset = max(0, min(y_offset, pixelHeight - zoom_h))

    # Extract the zoomed region with fractional precision
    x1, y1 = int(x_offset), int(y_offset)
    x2, y2 = min(int(x_offset + zoom_w), pixelWidth), min(int(y_offset + zoom_h), pixelHeight)
    
    cropped = image[y1:y2, x1:x2]

    # Resize smoothly using cubic interpolation
    display = cv2.resize(cropped, (screen_w, screen_h), interpolation=cv2.INTER_CUBIC)

    # Display lat/long information
    if 0 <= mouse_x < screen_w and 0 <= mouse_y < screen_h:
        orig_x = x_offset + (mouse_x / screen_w) * zoom_w
        orig_y = y_offset + (mouse_y / screen_h) * zoom_h
        
        lat, long = pixel_to_latlong(orig_x, orig_y)
        gray_value = image[int(orig_y), int(orig_x)]
        
        cv2.putText(display, f"Gray: {gray_value}", (mouse_x, mouse_y - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(display, f"Lat: {lat:.6f}, Long: {long:.6f}", (mouse_x, mouse_y - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

    cv2.imshow("Map Viewer", display)

def mouse_callback(event, x, y, flags, param):
    """Handles zooming and panning interactively."""
    global zoom_factor, x_offset, y_offset, start_x, start_y, dragging, mouse_x, mouse_y

    mouse_x, mouse_y = x, y

    if event == cv2.EVENT_MOUSEWHEEL:
        prev_zoom = zoom_factor
        zoom_factor = max(1.0, min(20.0, zoom_factor + (zoom_step if flags > 0 else -zoom_step)))

        # Adjust offsets to keep the zoom centered at the cursor position
        zoom_ratio = zoom_factor / prev_zoom
        x_offset += (x / screen_w) * (pixelWidth - pixelWidth / zoom_ratio)
        y_offset += (y / screen_h) * (pixelHeight - pixelHeight / zoom_ratio)

    elif event == cv2.EVENT_LBUTTONDOWN:
        dragging = True
        start_x, start_y = x, y

    elif event == cv2.EVENT_MOUSEMOVE and dragging:
        dx = (start_x - x) * (pixelWidth / screen_w) / zoom_factor
        dy = (start_y - y) * (pixelHeight / screen_h) / zoom_factor
        x_offset = max(0, min(x_offset + dx, pixelWidth - pixelWidth / zoom_factor))
        y_offset = max(0, min(y_offset + dy, pixelHeight - pixelHeight / zoom_factor))
        start_x, start_y = x, y

    elif event == cv2.EVENT_LBUTTONUP:
        dragging = False

    display_image()

# Set up window
cv2.namedWindow("Map Viewer", cv2.WINDOW_NORMAL)
cv2.setMouseCallback("Map Viewer", mouse_callback)

display_image()

while True:
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cv2.destroyAllWindows()
