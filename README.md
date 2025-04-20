# The-Nail-Lab-Demo

Website with topic - "nails", for a client. I am working on this at the moment. The goal is to gain experience as a beginner and learn new things.
<br><br><br>

    Screenshot of the main page
![Screenshot 2025-04-20 at 11 01 02](https://github.com/user-attachments/assets/818b162e-0d79-41b9-9195-6e870e44fe33)
<br><br>

    Screenshot of the main page (max-width: 800px)
![Screenshot 2025-04-20 at 11 00 40](https://github.com/user-attachments/assets/933016cf-d122-4fd9-8775-a4d6bc605e7a)
<br><br>

This project is a responsive appointment booking interface for a nail studio. It allows clients to easily schedule services like nail building, polishing, and repair (for testing random features for appointment), with date and time selection powered by Flatpickr.

<br><br><br>
### Visual Elements
    A welcoming image in the header and footer for branding.
    Social media links to Facebook and Instagram.
    Footer includes contact info and business hours.

### The top navigation bar provides access to:
    Начало (Home)
    За мен (About)
    Продукти (Products)
    Галерия (Gallery)
    Услуги (Services)

### Users can book appointments by filling out a form that includes:
    - Service selection (dropdown)
    - Date and time picker
    - First name
    - Last name
    - Phone number (with validation)

<br><br><br>
### The UI is focusing on a clean layout with responsive behavior.
    Header: 
        Moving background with a seamless nail collage using @keyframes moveBackground.
        
    Main Section (Appointment Form):
        Clean form styling with: 
            Rounded corners, Light shadows, Focus on readability and input validation (:invalid border coloring).

        Date & Time Picker (Flatpickr):
            The project uses Flatpickr v4.6.9 (in the js file) to enhance the date-time input with an intuitive UI and built-in restrictions.
            Features:
                Date format: YYYY-MM-DD HH:MM
                Time selection: Enabled, 24-hour format
                Interval: 30-minute steps
                Restrictions: No appointments on weekends, Only between 10:00 and 18:00, Disables past dates
                If a user tries to book outside of working hours, a popup appears:
                    \\[[[ alert("Изберете час между 10:00 и 18:00!"); ]]]//
                    …and the date input is reset.

        The form with ID appointment-form uses fetch() to send an asynchronous POST request to a backend endpoint (default)

    Responsive Design:
        The layout adapts for screens under 800px:
        Navigation switches to vertical menu.
        Form and image stack vertically.
        Footer sections stack instead of aligning side-by-side.
        Adjustments to padding and widths for mobile comfort.
            
    Footer:
        Split contact/info sections with themed colors and rounded containers.


<br><br><br>
## Backend (Flask)

    This app provides a simple Flask-based API to handle appointment bookings with PostgreSQL integration and email notifications.
    I managed to connect the DB to the form. It was my first time facing this method. When I started this project I was not familiar with Django ORM and instead of creating Django Project I used Flask.
    Because I'm running the project on local host, I didn't manage to send an actual email to my account for the appointment.

<br><br><br>
## Conclusion

    I will re-develop this project using Django and extend the logic. This is demo version with one page(Others are not developed).
    The documentation is not that detailed, but it is enough to give an overview of the project itself.







