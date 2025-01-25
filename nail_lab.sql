CREATE TABLE appointments (
    id SERIAL PRIMARY KEY,
    appointment_time TIMESTAMP UNIQUE NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    mobile_phone VARCHAR(20) NOT NULL
);
