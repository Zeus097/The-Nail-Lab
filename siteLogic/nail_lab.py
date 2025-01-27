from flask import Flask, request
from flask_cors import CORS
import psycopg2
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http://127.0.0.1:5500"]}})

@app.route("/", methods=["POST"])
def book_appointment():
    date_time = request.form.get("date")
    test_type = request.form.get("service")
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    phone = request.form.get("phone")

    if not date_time or not test_type or not first_name or not last_name or not phone:
        return "All fields are required!", 400

    try:
        appointment_start = datetime.strptime(date_time, "%Y-%m-%d %H:%M")
    except ValueError:
        return "Invalid date format! Use 'YYYY-MM-DD HH:MM'", 400

    if test_type == "Изграждане":
        test_duration = 2  # 2 hours
    elif test_type == "Лакиране":
        test_duration = 4  # 4 hours
    elif test_type == "Поправяне на нокти":
        test_duration = 4  # 4 hours
    else:
        return "Invalid test type!", 400

    appointment_end = appointment_start + timedelta(hours=test_duration)

    try:
        conn = psycopg2.connect(
            database="PRIVATE",
            user="PRIVATE",
            password="PRIVATE",
            host="PRIVATE",
            port="PRIVATE"
        )
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT * FROM appointments
            WHERE date = %s AND (
                (start_time < %s AND end_time > %s) OR
                (start_time < %s AND end_time > %s) OR
                (start_time >= %s AND end_time <= %s)
            )
            """,
            (appointment_start.date(), appointment_end, appointment_start,
             appointment_start, appointment_end, appointment_start, appointment_end)
        )

        if cursor.fetchone():
            return "This time slot is already booked!", 400

        cursor.execute(
            """
            INSERT INTO appointments (date, start_time, end_time, test_type, first_name, last_name, phone)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (appointment_start.date(), appointment_start, appointment_end, test_type, first_name, last_name, phone)
        )
        conn.commit()
        conn.close()

        send_notification_email(appointment_start, appointment_end, test_type, first_name, last_name, phone)

        return "Appointment booked successfully!", 200

    except Exception as e:
        return f"An error occurred: {e}", 500

def send_notification_email(start_time, end_time, test_type, first_name, last_name, phone):
    import smtplib
    from email.mime.text import MIMEText

    SMTP_SERVER = "PRIVATE"
    SMTP_PORT = "PRIVATE" # It is num without the ""...
    EMAIL_ADDRESS = "PRIVATE"
    EMAIL_PASSWORD = "PRIVATE"

    subject = "New Appointment Booking"
    body = f"""
    A new appointment has been booked:
    - Name: {first_name} {last_name}
    - Phone: {phone}
    - Test Type: {test_type}
    - Start Time: {start_time}
    - End Time: {end_time}
    """

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = "test_subject@abv.bg"

    try:

        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:

            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
            print("Notification email sent successfully!")

    except Exception as e:

        print(f"Failed to send email: {e}")

if __name__ == "__main__":
    app.run(debug=True)
