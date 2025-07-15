import os
from ultralytics import YOLO
from datetime import datetime
import json

model = YOLO('yolov8n.pt')

def process_images():
    date_str = datetime.now().strftime('%Y-%m-%d')
    input_dir = f'data/raw/telegram_images/{date_str}/lobelia4cosmetics'
    output_dir = f'data/staging/image_detections/{date_str}/lobelia4cosmetics'
    os.makedirs(output_dir, exist_ok=True)

    for img_file in os.listdir(input_dir):
        results = model.predict(os.path.join(input_dir, img_file))
        detections = [{'label': r.names[int(r.cls)], 'confidence': float(r.conf), 'box': r.xywh.tolist()} for r in results[0].boxes]
        with open(os.path.join(output_dir, f'{img_file}.json'), 'w') as f:
            json.dump(detections, f)

if __name__ == '__main__':
    process_images()
