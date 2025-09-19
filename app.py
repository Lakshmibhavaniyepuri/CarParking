# from flask import Flask, render_template, request
# from parking_model import detect_parking
# import os

# app = Flask(__name__)
# UPLOAD_FOLDER = 'static/uploads'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# @app.route('/')
# def home():
#     return render_template('index.html')

# @app.route('/predict', methods=['POST'])
# def predict():
#     if 'file' not in request.files:
#         return 'No file part'
    
#     file = request.files['file']
#     if file.filename == '':
#         return 'No selected file'
    
#     if file:
#         filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
#         file.save(filepath)
#         total, occupied, available, output_img = detect_parking(filepath)
#         return render_template('result.html',
#                                total=total,
#                                occupied=occupied,
#                                available=available,
#                                output_img=output_img)

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, render_template, request
from parking_model import detect_parking
import os
import smtplib
from email.message import EmailMessage
import ssl
import cv2
from dotenv import load_dotenv

load_dotenv()  # Load email password from .env

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def send_parking_report_email(to_email, total_slots, occupied_slots, available_slots, image_rgb, summary_csv_path):
    sender_email = ''
    app_password = os.getenv("EMAIL_PASS")  # Your Gmail app password

    subject = "🅿️ Parking Slot Detection Report"
    body = f"""\
Hello,

Please find attached the parking slot detection summary and visualization.

Summary:
- Total Slots     : {total_slots}
- Occupied Slots  : {occupied_slots}
- Available Slots : {available_slots}

Regards,
YOLOv8 Parking Bot
"""

    msg = EmailMessage()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.set_content(body)

    # Attach summary CSV
    with open(summary_csv_path, 'rb') as f:
        msg.add_attachment(f.read(), maintype='application', subtype='octet-stream', filename='parking_summary.csv')

    # Attach visualization
    annotated_img_path = os.path.join(UPLOAD_FOLDER, 'parking_visualization.jpg')
    cv2.imwrite(annotated_img_path, cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR))
    with open(annotated_img_path, 'rb') as f:
        msg.add_attachment(f.read(), maintype='image', subtype='jpeg', filename='parking_visualization.jpg')

    # Send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
        server.login(sender_email, app_password)
        server.send_message(msg)

    print("✅ Email sent successfully to:", to_email)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files or 'email' not in request.form:
        return 'Missing file or email.'

    file = request.files['file']
    email = request.form['email']

    if file.filename == '':
        return 'No selected file'

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    # Detect parking slots
    total, occupied, available, output_img_path, summary_csv_path = detect_parking(filepath)

    # Load image for email
    image_rgb = cv2.cvtColor(cv2.imread(output_img_path), cv2.COLOR_BGR2RGB)

    # Send email report
    send_parking_report_email(email, total, occupied, available, image_rgb, summary_csv_path)

    return render_template('result.html',
                           total=total,
                           occupied=occupied,
                           available=available,
                           output_img=output_img_path,
                           summary_csv='/' + summary_csv_path)


if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)
