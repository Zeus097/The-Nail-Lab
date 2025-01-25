import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import psycopg2
from flask import Flask, request, jsonify

app = Flask(__name__)

DB_CONFIG = {
    'dbname': 'nail_lab',
    'user': 'postgres',
    'password': '0897535532',
    'host': 'localhost',
    'port': 5432
}

EMAIL_HOST = 'smtp.abv.bg'
EMAIL_PORT = 465
EMAIL_ADDRESS = 'test_subject@abv.bg'
EMAIL_PASSWORD = '3EGZln1aYM'


def get_db_connection():
    conn = psycopg2.connect(**DB_CONFIG)
    return conn


def send_email_notification_to_admin(appointment_time):
    try:
        message = MIMEMultipart()
        message['From'] = EMAIL_ADDRESS
        message['To'] = EMAIL_ADDRESS
        message['Subject'] = 'New Appointment Booking Notification'

        body = f"""
        Hello,

        A new appointment has been booked at the following time:
        Appointment Time: {appointment_time}

        Please check the system for more details.
        """
        message.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(message)

    except Exception as e:
        print(f"Failed to send email: {e}")


@app.route('/', methods=['POST'])
def book_appointment():
    data = request.get_json()

    date = data.get('date')
    time = data.get('time')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    mobile_phone = data.get('mobile_phone')

    if not all([date, time, first_name, last_name, mobile_phone]):
        return jsonify({'error': 'All fields are required!'}), 400

    appointment_datetime = f"{date} {time}"

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT COUNT(*)
            FROM appointments
            WHERE appointment_time = %s
            """,
            (appointment_datetime,)
        )
        (conflict_count,) = cur.fetchone()

        if conflict_count > 0:
            return jsonify({'error': 'This time slot is already booked!'}), 409

        cur.execute(
            """
            INSERT INTO appointments (appointment_time, first_name, last_name, mobile_phone)
            VALUES (%s, %s, %s, %s)
            """,
            (appointment_datetime, first_name, last_name, mobile_phone)
        )
        conn.commit()

        send_email_notification_to_admin(appointment_datetime)

        cur.close()
        conn.close()

        return jsonify({'message': 'Appointment successfully booked!'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)


