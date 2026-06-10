# RUBBLES KB — База знаний

## Деплой на PythonAnywhere (бесплатно)

### 1. Зарегистрируйтесь на PythonAnywhere
https://www.pythonanywhere.com — кнопка **"Create a Beginner Account"** (бесплатно, без карты).

### 2. Откройте консоль Bash
После регистрации нажмите **Consoles** → **Bash**.

### 3. Склонируйте репозиторий
```bash
git clone https://github.com/anarex8332/ubbles-kb.git
cd ubbles-kb
```

### 4. Создайте виртуальное окружение и установите зависимости
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 5. Настройте статику и базу данных
```bash
python manage.py collectstatic --noinput
python manage.py migrate
python manage.py seed_data
python manage.py createsuperuser
```

### 6. Настройте Web приложение
В панели PythonAnywhere нажмите **Web** → **Add a new web app**:
- Выберите **Manual configuration**
- Python версия: **3.10**

### 7. Настройте WSGI файл
На странице Web найдите **"WSGI configuration file"** — нажмите на эту ссылку.
В открывшемся редакторе **удалите всё** и вставьте этот код:

```python
import os
import sys

path = '/home/anarex8332/ubbles-kb'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

Нажмите **Save**.

### 8. Настройте Virtualenv
Вернитесь на страницу Web. В разделе **Virtualenv** укажите:
```
/home/anarex8332/ubbles-kb/venv
```

### 9. Настройте Static Files
В разделе **Static files**:
- **URL:** `/static/`
- **Directory:** `/home/anarex8332/ubbles-kb/staticfiles`

### 10. Перезагрузите
Нажмите зелёную кнопку **Reload**.

### Готово!
Ваш сайт: **https://anarex8332.pythonanywhere.com**

Разошлите ссылку друзьям!

### Если сайт не работает
На странице Web в разделе **Logs** нажмите **Error log file** — скопируйте текст ошибки и покажите мне.