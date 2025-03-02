import cv2
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilename(filetypes=[("PNG Images", "*.png")])
if not file_path:
    print("No file selected. Exiting.")
    exit()

image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
if image is None:
    print("Error: Could not load image.")
    exit()

Xmin, Ymin, Xmax, Ymax = -110.842703, 38.364678, -110.696422, 38.460551
pixelWidth, pixelHeight = 12802, 10664

h, w = image.shape
screen_w, screen_h = 800, 667
scale_factor = min(screen_w / w, screen_h / h, 1.0)
display_w, display_h = int(w * scale_factor), int(h * scale_factor)

zoom_factor = 1.0
zoom_step = 0.1
x_offset, y_offset = 0, 0
mouse_x, mouse_y = 0, 0
dragging = False
start_x, start_y = 0, 0

def pixel_to_latlong(px, py):
    long = Xmin + (px / pixelWidth) * (Xmax - Xmin)
    lat = Ymax - (py / pixelHeight) * (Ymax - Ymin)
    return lat, long

def display_image():
    global x_offset, y_offset
    
    zoom_w, zoom_h = int(w / zoom_factor), int(h / zoom_factor)
    x_offset = max(0, min(x_offset, w - zoom_w))
    y_offset = max(0, min(y_offset, h - zoom_h))
    
    cropped = image[y_offset:y_offset + zoom_h, x_offset:x_offset + zoom_w]
    display = cv2.resize(cropped, (display_w, display_h), interpolation=cv2.INTER_LINEAR)
    
    if 0 <= mouse_x < display_w and 0 <= mouse_y < display_h:
        orig_x = int(x_offset + (mouse_x / display_w) * zoom_w)
        orig_y = int(y_offset + (mouse_y / display_h) * zoom_h)
        
        if 0 <= orig_x < w and 0 <= orig_y < h:
            gray_value = image[orig_y, orig_x]
            lat, long = pixel_to_latlong(orig_x, orig_y)
            cv2.putText(display, f"Gray: {gray_value}", (mouse_x, mouse_y - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
            cv2.putText(display, f"Lat: {lat:.10f}, Long: {long:.10f}", (mouse_x, mouse_y - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
    
    cv2.imshow("Map Viewer", display)

def mouse_callback(event, x, y, flags, param):
    """Handles zooming and panning interactively."""
    global zoom_factor, x_offset, y_offset, start_x, start_y, dragging, mouse_x, mouse_y

    mouse_x, mouse_y = x, y 
    if event == cv2.EVENT_MOUSEWHEEL:
        prev_zoom = zoom_factor
        zoom_factor = max(1.0, min(5.0, zoom_factor + (zoom_step if flags > 0 else -zoom_step)))
        
        zoom_ratio = zoom_factor / prev_zoom
        x_offset = int(mouse_x / display_w * (w - (w / zoom_ratio)) + x_offset)
        y_offset = int(mouse_y / display_h * (h - (h / zoom_ratio)) + y_offset)

    elif event == cv2.EVENT_LBUTTONDOWN:
        dragging = True
        start_x, start_y = x, y

    elif event == cv2.EVENT_MOUSEMOVE and dragging:
        dx = (start_x - x) * (w / display_w) / zoom_factor
        dy = (start_y - y) * (h / display_h) / zoom_factor
        x_offset = max(0, min(x_offset + int(dx), w - int(w / zoom_factor)))
        y_offset = max(0, min(y_offset + int(dy), h - int(h / zoom_factor)))
        start_x, start_y = x, y

    elif event == cv2.EVENT_LBUTTONUP:
        dragging = False

    display_image()

cv2.namedWindow("Map Viewer", cv2.WINDOW_NORMAL)
cv2.setMouseCallback("Map Viewer", mouse_callback)

display_image()

while True:
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cv2.destroyAllWindows()
