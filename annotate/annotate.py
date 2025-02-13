import os
import cv2
from ultralytics import YOLO
from pathlib import Path
model = YOLO("yolov8n.pt")
VIDEOS_PATH = "videos"
DATASET_PATH = "dataset"
CLASS_NAME = "WaterBottle"  
EXCLUDE_CLASS = "person"  
os.makedirs(DATASET_PATH, exist_ok=True)

video_folders = [f for f in os.listdir(VIDEOS_PATH) if os.path.isdir(os.path.join(VIDEOS_PATH, f))]
yolo_classes = model.names

for video_folder in video_folders:
    video_path = os.path.join(VIDEOS_PATH, video_folder)
    output_folder = os.path.join(DATASET_PATH, video_folder)
    os.makedirs(output_folder, exist_ok=True)
    image_files = [f for f in os.listdir(video_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

    for image_file in image_files:
        image_path = os.path.join(video_path, image_file)
        output_image_path = os.path.join(output_folder, image_file)
        results = model(image_path)[0]
        annotations = []

        for box in results.boxes:
            class_id = int(box.cls.item())
            conf = box.conf.item()
            if yolo_classes[class_id] == EXCLUDE_CLASS:
                continue  
            x_center = (box.xywh[0][0].item() / results.orig_shape[1])
            y_center = (box.xywh[0][1].item() / results.orig_shape[0])
            width = (box.xywh[0][2].item() / results.orig_shape[1])
            height = (box.xywh[0][3].item() / results.orig_shape[0])
            annotations.append(f"0 {x_center} {y_center} {width} {height}")

        if annotations:
            cv2.imwrite(output_image_path, cv2.imread(image_path))
            label_path = os.path.join(output_folder, f"{Path(image_file).stem}.txt")
            with open(label_path, "w") as f:
                f.write("\n".join(annotations))
