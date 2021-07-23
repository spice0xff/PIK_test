# Требования
python 3.8

# Деплой и запуск
* git clone https://github.com/spice0xff/PIK_test
* cd PIK_test
* python3 -m venv env
* source venv/bin/activate
* pip3 install -r requirements.txt
* python3 manage.py makemigrations service_organizations
* python3 manage.py migrate
* python3 manage.py test
* python3 manage.py runserver

# Проверка работы
curl.sh
