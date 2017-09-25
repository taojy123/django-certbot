
set PATH=%PATH%;C:\Python27;C:\Python27\Scripts;
pip install -r requirement.txt
python manage.py migrate
explorer http://127.0.0.1:8000/
python manage.py runserver 0.0.0.0:8000
