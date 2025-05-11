# 🏥 Healthcare Project DZ

A full-featured Django-based **Healthcare ERP system** designed to manage core clinical, administrative, and operational data. This project adheres to modern healthcare data standards while providing a modular, extensible architecture.

## 🚀 Features

### ✅ Core Modules
- **Patient Management**: Personal info, contact details, medical record numbers, insurance, and emergency contacts.
- **Clinical Data**:
  - Medical History (conditions, allergies, immunizations)
  - Clinical Measurements (vitals, labs)
- **Encounters & Observations**:
  - Inpatient, outpatient, emergency, telehealth visits
  - Procedures & observations (ICD, CPT, LOINC supported)
- **Billing**:
  - Insurance claims and payments
- **Scheduling**:
  - Appointment tracking and provider availability
- **Documents & Imaging**:
  - Uploads, PDF generation, and radiology integration
- **Mental Health**:
  - Therapy sessions and assessments
- **Reporting & Export**:
  - CSV & PDF exports with pagination and filtering

### 🧠 Intelligent Tools
- Dynamic filtering (AJAX-based)
- Fake patient seeding with AI-generated data (via Faker)
- Responsive table rendering
- Role-based permissions with Django Groups (Admin, Doctor, Nurse)

## 🗃️ Directory Structure



healthcare_project/
├── healthcare/ # Django project core
├── patients/ # Main app with submodules:
│ ├── models/ # Structured per domain (core, clinical, imaging, billing...)
│ ├── views/ # CBVs for API, PDF, data editing
│ ├── admin/ # Separated admin configs
│ ├── forms/ # Patient-related forms
│ ├── templates/ # Modular HTML
│ ├── static/ # CSS and assets
├── manage.py



## 📦 Tech Stack
- **Backend**: Django 5.2, Python 3.13
- **Frontend**: Bootstrap, AJAX
- **PDF Generator**: WeasyPrint
- **Fake Data**: Faker
- **Version Control**: Git + GitHub

## ⚙️ Getting Started

1. Clone the repo  
   ```bash
   git clone https://github.com/MerryfaceAI/Healthcare_Project_DZ.git
   cd Healthcare_Project_DZ

2. Create & activate a virtual environment  
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows

3. Install dependencies
   ```bash
   pip install -r requirements.txt

5. Run migrations & seed data
   ```bash
   python manage.py migrate
   python manage.py seed_patients

7. Start the server
   ```bash
   python manage.py runserver
   
 Standards & Compliance
 
Supports ICD-10, SNOMED CT, CPT, LOINC, HL7, DICOM codes
Modular structure designed for scalability and auditability

License
MIT License https://opensource.org/license/MIT


### 📝 Bonus Tip
Once added, save and run:

```bash
git add README.md
git commit -m "Complete README with setup and compliance info"
git push


