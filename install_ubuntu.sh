sudo pip install uwsgi
sudo pip install pyyaml
python manage.py makemigrations authority
python manage.py sqlmigrate authority 0001
python manage.py makemigrations blog
python manage.py sqlmigrate blog 0001
python manage.py makemigrations file
python manage.py sqlmigrate file 0001
python manage.py migrate
