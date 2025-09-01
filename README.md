🔐 Fraud Detection System (Django + Machine Learning)
📖 Project Overview

A real-time fraud detection system built with Django and Machine Learning.
It analyzes transactions, detects suspicious patterns, alerts users via email notifications, and maintains a fraud blacklist.
The project includes an admin dashboard and REST API integration for monitoring and management.

✨ Features

⚡ Real-time fraud detection using custom rules and ML model

🖥️ Django backend with REST API support

🤖 Machine Learning integration for anomaly detection

🚫 Manual fraud blacklist for phone, account, card, and transaction IDs

📊 Dashboard displaying fraud reports and activities

📧 Email notifications for detected fraud cases

🎨 Clean, responsive frontend (HTML, CSS, Bootstrap)

🔑 Admin login and management panel

🕵️ Fraud Detection Logic

Multiple transactions within short time intervals

Location/IP mismatch for transactions

Suspicious amounts just under alert thresholds

Repeated failed login/payment attempts

Matches with known fraud blacklist entries

🛠️ Technologies Used

Python

Django & Django REST Framework

Scikit-learn (Machine Learning)

Pandas, NumPy (Data Analysis)

HTML, CSS, Bootstrap (Frontend)

SQLite (Database)

SMTP (Email notifications)

📂 Project Structure
fraud_detection/
├── core/              # Django app with views, models, fraud logic
├── templates/         # HTML templates
├── static/            # CSS, JS, images
├── trained_model/     # Saved ML model
├── fraud_list.txt     # Manual fraud blacklist
├── db.sqlite3         # Local database
├── manage.py
├── requirements.txt
└── README.md

⚙️ Setup Instructions
1. Clone the repository
git clone https://github.com/yourusername/fraud-detection-system.git
cd fraud-detection-system

2. Create virtual environment
python -m venv venv
# Activate
venv\Scripts\activate   # On Windows  
source venv/bin/activate # On Mac/Linux

3. Install dependencies
pip install -r requirements.txt

4. Apply migrations
python manage.py makemigrations
python manage.py migrate

5. Create superuser (Admin)
python manage.py createsuperuser

6. Run the server
python manage.py runserver


App: http://localhost:8000

Admin: http://localhost:8000/admin

📧 Email Alert Configuration

In settings.py, configure your email credentials:

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'your_email@gmail.com'
EMAIL_HOST_PASSWORD = 'your_app_password'
EMAIL_USE_TLS = True


🔒 For security, use environment variables with python-decouple instead of hardcoding credentials.

🚀 Future Improvements

📊 Add interactive fraud charts to the dashboard

🔐 Implement API authentication (JWT)

🌍 Enable GeoIP tracking for transactions

☁️ Deploy on Heroku / AWS

📜 License

This project is licensed under the MIT License.
See the LICENSE
 file for details.

👩‍💻 Author

Shankar Sable
📧 Email:sableshankar98@gmail.com

🔗 GitHub: Shankarsable800












