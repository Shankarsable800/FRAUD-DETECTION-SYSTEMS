# FRAUD-DETECTION-SYSTEM
A real-time fraud detection system built with Django and machine learning. It analyzes transactions, detects suspicious patterns, alerts users, and maintains a fraud blacklist. Includes dashboard, email notifications, and REST API integration.

# Fraud Detection System (Django and Machine Learning)

This is a real-time fraud detection system built using Django and Machine Learning. It analyzes transaction data to detect suspicious behavior, alerts users via email, and includes an admin dashboard for monitoring.

## Features

- Real-time fraud detection using custom rules and ML
- Django backend with REST API
- Machine learning model integration
- Manual fraud blacklist for phone, account, card, and transaction ID
- Dashboard showing fraud reports and activity
- Email notifications for detected fraud
- Clean, responsive frontend (HTML, CSS, Bootstrap)
- Admin login and management

## Fraud Detection Logic

- Multiple transactions within short time intervals
- Location or IP address mismatch
- Suspicious amounts just under common alert limits
- Repeated failed attempts
- Matches with known fraud list (blacklist)

## Technologies Used

- Python
- Django and Django REST Framework
- Scikit-learn (Machine Learning)
- Pandas, NumPy (Data Analysis)
- HTML, CSS, Bootstrap
- SQLite
- SMTP for email notifications

## Project Structure

fraud_detection/  
├── core/                  - Django app with views, models, logic  
├── templates/             - HTML templates  
├── static/                - CSS, JS, images  
├── trained_model/         - Saved machine learning model  
├── fraud_list.txt         - Manual fraud entries  
├── db.sqlite3             - Local database  
├── manage.py  
├── requirements.txt  
└── README.md  

## Setup Instructions

1. Clone the repository:  
   git clone https://github.com/yourusername/fraud-detection-system.git  
   cd fraud-detection-system

2. Create a virtual environment:  
   python -m venv venv  
   source venv/bin/activate      (or venv\Scripts\activate on Windows)

3. Install dependencies:  
   pip install -r requirements.txt

4. Apply database migrations:  
   python manage.py makemigrations  
   python manage.py migrate

5. Create superuser (for admin login):  
   python manage.py createsuperuser

6. Start the development server:  
   python manage.py runserver

7. Open in browser:  
   http://localhost:8000  

Admin panel:  
   http://localhost:8000/admin

## Email Alert Configuration

In your Django settings.py, add your email credentials:

EMAIL_HOST = 'smtp.gmail.com'  
EMAIL_PORT = 587  
EMAIL_HOST_USER = 'your_email@gmail.com'  
EMAIL_HOST_PASSWORD = 'your_app_password'  
EMAIL_USE_TLS = True  

Or use environment variables and python-decouple to store credentials securely.

## Future Improvements

- Add interactive fraud charts on dashboard
- Add API authentication (JWT)
- GeoIP tracking for transaction origin
- Deployment to Heroku or AWS

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Author

Developed by Dipali Tompe  
Contact: dipalitompe820@gmail.com  
GitHub: https://github.com/Dipali820
