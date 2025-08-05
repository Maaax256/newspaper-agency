# Newspaper agency website

A web application for managing newspapers, which allows  
users to track editor assignments for each issue and  
create their own newspapers.

---
## Deployed version

https://newspaper-agency-m9df.onrender.com

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/Maaax256/newspaper-agency.git
cd newspaper-agency
git checkout develop
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate      # Linux/macOS
venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run migrations

```bash
python manage.py migrate
```

### 5. Create a superuser

```bash
python manage.py createsuperuser
```

### 6. Fill database with fake data

```bash
python manage.py load_fake_data
```

### 7. Start the development server

```bash
python manage.py runserver
```

📍 Open your browser and go to http://127.0.0.1:8000