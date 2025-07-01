# MediTrack

**MediTrack** is a medical records system designed to help healthcare professionals securely manage patient data, vital signs, and care history.

The platform provides a user-friendly dashboard for monitoring patient progress and recording essential health data with ease.

---

## 🏠 Homepage Overview (Updated)

The landing page now features:

- ✅ A modern **Hero Section** with medical branding, headline, and CTA button
- ✅ A **Features Section** highlighting key functionality
- ✅ An **About Us Section** embedded directly in the homepage
- ✅ A **Contact Us Section** with location, email, and phone
- ✅ A clean, responsive design with Bootstrap 5 and Bootstrap Icons

---

## 🌟 Features

- Secure user authentication (register/login/logout)
- Dashboard to view, search, and manage patients
- Add/Edit/Delete patients
- Add and view vital signs (blood pressure, heart rate, temperature, oxygen saturation)
- Form validation & error handling
- RESTful API endpoint for vitals
- Modern responsive UI using Bootstrap 5
- Homepage with:
  - Hero section introducing MediTrack
  - "About Us" section
  - Contact info
  - Call-to-action buttons
- Deployment on AWS (EC2 Ubuntu)

---

## 🛠 Tech Stack

- **Backend:** Django 2.2.4, Python 3.10
- **Database:** MySQL 8
- **Frontend:** HTML5, Bootstrap 5, Bootstrap Icons
- **Security:** Bcrypt for password hashing, CSRF protection
- **API:** JSON via `JsonResponse`
- **Deployment:** AWS EC2 + Gunicorn + Nginx

---

## 🚀 Getting Started

1. **Clone the repository**
```bash
git clone https://github.com/MosabAbdallah/meditrack.git
cd meditrack
