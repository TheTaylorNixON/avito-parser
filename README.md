avito-parser
web parser for avito(flask)

Установка:

В консоли:
- cd /Downloads/avito-parser-master
1) pip install virtualenv (Если не получилось: sudo pip install virtualenv)
2) virtualenv venv
3) source venv/bin/activate
4) pip install -r requirements.txt
5) python database_creater.py
6) python parser-flask.py

Готово, переходим по ссылке http://127.0.0.1:5000/

- Если на локальной машине не установлен mysql:
1) Заменить файл 'mysql_wrapper.py' в папке 'avito-parser-master' файлом 'mysql_wrapper.py' из папки 'mysql_wrapper_for_remote_acsess'
2) https://cp-hosting.jino.ru/management/mysql/ipaccess/
3) Login: 9883814296    
   Password: xtF7uKk2
4) Добавить разрешенный IP, в Диапазон IP добавить ваш текущий IP-адрес
В консоли:
5) pip install virtualenv (Если не получилось: sudo pip install virtualenv)
6) virtualenv venv
7) source venv/bin/activate
8) pip install -r requirements.txt
6) python parser-flask.py

Готово, переходим по ссылке http://127.0.0.1:5000/