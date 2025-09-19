# # parking_model.py
# import cv2
# import pandas as pd
# from ultralytics import YOLO

# def detect_parking(image_path):
#     model = YOLO('C:/Users/Dinesh Kumar M/OneDrive/图片/new-parking/best.pt')
#     image = cv2.imread(image_path)
#     image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#     results = model.predict(source=image_path, conf=0.5)
#     boxes = results[0].boxes

#     output_data = []
#     available_boxes = [box for box in boxes if int(box.cls[0]) == 0]
#     occupied_boxes = [box for box in boxes if int(box.cls[0]) == 1]
#     available_slots = len(available_boxes)
#     occupied_slots = len(occupied_boxes)
#     total_slots = available_slots + occupied_slots
#     slot_id = 1

#     for box in available_boxes:
#         x1, y1, x2, y2 = map(int, box.xyxy[0])
#         cv2.rectangle(image_rgb, (x1, y1), (x2, y2), (0, 255, 0), 2)
#         output_data.append({'Slot ID': slot_id, 'X1': x1, 'Y1': y1, 'X2': x2, 'Y2': y2, 'Status': 'Available'})
#         slot_id += 1

#     for box in occupied_boxes:
#         x1, y1, x2, y2 = map(int, box.xyxy[0])
#         cv2.rectangle(image_rgb, (x1, y1), (x2, y2), (255, 0, 0), 2)
#         output_data.append({'Slot ID': slot_id, 'X1': x1, 'Y1': y1, 'X2': x2, 'Y2': y2, 'Status': 'Occupied'})
#         slot_id += 1

#     df = pd.DataFrame(output_data)
#     df.to_csv('parking_status_output.csv', index=False)
#     summary_df = pd.DataFrame({
#         'Total Number of Slots': [total_slots],
#         'Occupied Slots': [occupied_slots],
#         'Available Slots': [available_slots]
#     })
#     summary_df.to_csv('parking_summary.csv', index=False)
#     result_path = 'static/uploads/annotated.jpg'
#     cv2.imwrite(result_path, cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR))

#     return total_slots, occupied_slots, available_slots, result_path
# import cv2
# import pandas as pd
# from ultralytics import YOLO
# import os

# def detect_parking(image_path):
#     # Load YOLOv8 model
#     model = YOLO('C:/Users/Dinesh Kumar M/OneDrive/图片/new-parking/best.pt')

#     # Read image
#     image = cv2.imread(image_path)
#     image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

#     # Run inference
#     results = model.predict(source=image_path, conf=0.5)
#     boxes = results[0].boxes

#     output_data = []
#     available_boxes = [box for box in boxes if int(box.cls[0]) == 0]
#     occupied_boxes = [box for box in boxes if int(box.cls[0]) == 1]
#     available_slots = len(available_boxes)
#     occupied_slots = len(occupied_boxes)
#     total_slots = available_slots + occupied_slots

#     slot_id = 1
#     for box in available_boxes:
#         x1, y1, x2, y2 = map(int, box.xyxy[0])
#         cv2.rectangle(image_rgb, (x1, y1), (x2, y2), (0, 255, 0), 2)
#         cv2.putText(image_rgb, 'Available', (x1, y1 - 10),
#                     cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
#         output_data.append({'Slot ID': slot_id, 'X1': x1, 'Y1': y1, 'X2': x2, 'Y2': y2, 'Status': 'Available'})
#         slot_id += 1

#     for box in occupied_boxes:
#         x1, y1, x2, y2 = map(int, box.xyxy[0])
#         cv2.rectangle(image_rgb, (x1, y1), (x2, y2), (255, 0, 0), 2)
#         cv2.putText(image_rgb, 'Occupied', (x1, y1 - 10),
#                     cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
#         output_data.append({'Slot ID': slot_id, 'X1': x1, 'Y1': y1, 'X2': x2, 'Y2': y2, 'Status': 'Occupied'})
#         slot_id += 1

#     # Save annotated image and CSVs
#     os.makedirs('static/results', exist_ok=True)

#     result_path = 'static/results/annotated.jpg'
#     summary_csv_path = 'static/results/parking_summary.csv'

#     cv2.imwrite(result_path, cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR))

#     df = pd.DataFrame(output_data)
#     df.to_csv('static/results/parking_status_output.csv', index=False)

#     summary_df = pd.DataFrame({
#         'Total Number of Slots': [total_slots],
#         'Occupied Slots': [occupied_slots],
#         'Available Slots': [available_slots]
#     })
#     summary_df.to_csv(summary_csv_path, index=False)

#     return total_slots, occupied_slots, available_slots, result_path, summary_csv_path
import cv2
import pandas as pd
from ultralytics import YOLO
import os

def detect_parking(image_path):
    model = YOLO('C:/Users/Bhava/OneDrive/Desktop/cars-1/new-parking')
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = model.predict(source=image_path, conf=0.5)
    boxes = results[0].boxes

    output_data = []
    available_boxes = [box for box in boxes if int(box.cls[0]) == 0]
    occupied_boxes = [box for box in boxes if int(box.cls[0]) == 1]
    available_slots = len(available_boxes)
    occupied_slots = len(occupied_boxes)
    total_slots = available_slots + occupied_slots
    slot_id = 1

    for box in available_boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        cv2.rectangle(image_rgb, (x1, y1), (x2, y2), (0, 255, 0), 2)
        output_data.append({'Slot ID': slot_id, 'X1': x1, 'Y1': y1, 'X2': x2, 'Y2': y2, 'Status': 'Available'})
        slot_id += 1

    for box in occupied_boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        cv2.rectangle(image_rgb, (x1, y1), (x2, y2), (255, 0, 0), 2)
        output_data.append({'Slot ID': slot_id, 'X1': x1, 'Y1': y1, 'X2': x2, 'Y2': y2, 'Status': 'Occupied'})
        slot_id += 1

    output_dir = 'static/uploads'
    os.makedirs(output_dir, exist_ok=True)

    status_path = os.path.join(output_dir, 'parking_status_output.csv')
    summary_path = os.path.join(output_dir, 'parking_summary.csv')
    image_out_path = os.path.join(output_dir, 'annotated.jpg')

    df = pd.DataFrame(output_data)
    df.to_csv(status_path, index=False)

    summary_df = pd.DataFrame({
        'Total Number of Slots': [total_slots],
        'Occupied Slots': [occupied_slots],
        'Available Slots': [available_slots]
    })
    summary_df.to_csv(summary_path, index=False)

    cv2.imwrite(image_out_path, cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR))

    return total_slots, occupied_slots, available_slots, image_out_path, summary_path
