### Overview:
ATM is based on sqlite3. Works on Python 3.5 and Python 2.7 and uses Django 1.10

### How to:
1. pip install -r requirements.txt
2. python manage.py migrate
3. python manage.py createsuperuser
3. python manage.py runserver
4. Open http://localhost:8000/admin/bank_account/bankaccount/ to add test data
5. Open http://localhost:8000/check_card_id to start using app
