# Add these new imports at the top
import cv2
import torch
import smtplib
from email.message import EmailMessage
from twilio.rest import Client  # For SMS alerts
import time

# SOS Configuration (Add to config.py)
SOS_SETTINGS = {
    "alert_threshold": 5,  # seconds of continuous detection
    "target_class": "person",  # YOLO class name to trigger SOS
    "sms": {
        "twilio_sid": "your_twilio_sid",
        "twilio_token": "your_twilio_token",
        "from_number": "+1234567890",
        "to_number": "+0987654321"
    },
    "email": {
        "smtp_server": "smtp.gmail.com",
        "smtp_port": 587,
        "from_email": "your_email@gmail.com",
        "password": "your_app_password",
        "to_email": "recipient@example.com"
    }
}

class SOSAlertSystem:
    def _init_(self):
        self.last_detection_time = None
        self.alert_triggered = False
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
        
    def send_email_alert(self):
        msg = EmailMessage()
        msg.set_content("EMERGENCY: SOS triggered by person detection!")
        msg["Subject"] = "SOS Alert"
        msg["From"] = SOS_SETTINGS["email"]["from_email"]
        msg["To"] = SOS_SETTINGS["email"]["to_email"]

        with smtplib.SMTP(SOS_SETTINGS["email"]["smtp_server"], SOS_SETTINGS["email"]["smtp_port"]) as server:
            server.starttls()
            server.login(SOS_SETTINGS["email"]["from_email"], SOS_SETTINGS["email"]["password"])
            server.send_message(msg)

    def send_sms_alert(self):
        client = Client(SOS_SETTINGS["sms"]["twilio_sid"], SOS_SETTINGS["sms"]["twilio_token"])
        client.messages.create(
            body="EMERGENCY: SOS triggered by person detection!",
            from_=SOS_SETTINGS["sms"]["from_number"],
            to=SOS_SETTINGS["sms"]["to_number"]
        )

    def check_sos_condition(self, frame):
        results = self.model(frame)
        detections = results.pandas().xyxy[0]
        
        # Check for target class detection
        target_detected = any(detections['name'] == SOS_SETTINGS["target_class"])
        
        if target_detected:
            if not self.last_detection_time:
                self.last_detection_time = time.time()
            else:
                duration = time.time() - self.last_detection_time
                if duration >= SOS_SETTINGS["alert_threshold"] and not self.alert_triggered:
                    self.trigger_sos()
                    self.alert_triggered = True
        else:
            self.last_detection_time = None
            self.alert_triggered = False

        # Add SOS status to frame
        if self.alert_triggered:
            cv2.putText(frame, "SOS TRIGGERED!", (10, 50), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
            frame = cv2.copyMakeBorder(frame, 10,10,10,10, cv2.BORDER_CONSTANT, value=(0,0,255))
            
        return frame

    def trigger_sos(self):
        print("EMERGENCY: Triggering SOS alerts!")
        speak("Emergency! Triggering SOS alerts!")
        
        # Send both email and SMS
        self.send_email_alert()
        self.send_sms_alert()