# Online Course App — Django Mock Exam Feature

## Windows setup
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py makemigrations onlinecourse
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
Admin: http://127.0.0.1:8000/admin/ ; app: http://127.0.0.1:8000/

This is a starter implementation to review against your course lab. Push it to your own public GitHub repository before using file URLs in the assessment.
