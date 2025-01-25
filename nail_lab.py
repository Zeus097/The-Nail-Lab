from flask import Flask, request
import psycopg2
from datetime import datetime, timedelta

app = Flask(__name__)


@app.route("/", methods=["POST"])
def book_appointment():
    
    date_time = request.form.get("date")
    test_type = request.form.get("test_type")

    if not date_time or not test_type:
        return "All fields are required!", 400

    try:
        appointment_start = datetime.strptime(date_time, "%Y-%m-%d %H:%M")
    except ValueError:
        return "Invalid date format! Use 'YYYY-MM-DD HH:MM'", 400

    if test_type == "Test 1":
        test_duration = 2  # 2 hours
    elif test_type == "Test 2":
        test_duration = 4  # 4 hours
    else:
        return "Invalid test type!", 400

    appointment_end = appointment_start + timedelta(hours=test_duration)

    try:
        conn = psycopg2.connect(
            database="nail_lab",
            user="postgres",
            password="0897535532",
            host="localhost",
            port="5432"
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
            INSERT INTO appointments (date, start_time, end_time, test_type)
            VALUES (%s, %s, %s, %s)
            """,
            (appointment_start.date(), appointment_start, appointment_end, test_type)
        )
        conn.commit()
        conn.close()

        send_notification_email(appointment_start, appointment_end, test_type)

        return "Appointment booked successfully!", 200

    except Exception as e:
        return f"An error occurred: {e}", 500


def send_notification_email(start_time, end_time, test_type):
    import smtplib
    from email.mime.text import MIMEText

    SMTP_SERVER = "smtp.abv.bg"
    SMTP_PORT = 465
    EMAIL_ADDRESS = "test_subject@abv.bg"
    EMAIL_PASSWORD = "3EGZln1aYM"

    subject = "New Appointment Booking"
    body = f"""
    A new appointment has been booked:
    - Test Type: {test_type}
    - Start Time: {start_time}
    - End Time: {end_time}
    """

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = "test@mail.com"

    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)


if __name__ == "__main__":
    app.run(debug=True)
