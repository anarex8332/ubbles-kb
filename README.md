# RUBBLES KB — База знаний

## Деплой на PythonAnywhere (бесплатно)

### 1. Зарегистрируйтесь на PythonAnywhere
https://www.pythonanywhere.com — кнопка **"Create a Beginner Account"** (бесплатно, без карты).

### 2. Откройте консоль Bash
Нажмите **Consoles** → **Bash**.

### 3. Склонируйте репозиторий и установите зависимости
```bash
git clone https://github.com/anarex8332/ubbles-kb.git
cd ubbles-kb
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Настройте статику и базу данных
```bash
python manage.py collectstatic --noinput
python manage.py migrate
python manage.py seed_data
python manage.py createsuperuser
```

### 5. Настройте Web приложение
Нажмите **Web** → **Add a new web app**:
- Выберите **Manual configuration**
- Python версия: **3.10**

### 6. Настройте WSGI файл
На странице Web нажмите на ссылку **"WSGI configuration file"** (под Code:).
Удалите всё и вставьте этот код:

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

### 7. Настройте Virtualenv
Вернитесь на страницу Web. В разделе **Virtualenv** укажите:
```
/home/anarex8332/ubbles-kb/venv
```

### 8. Настройте Static Files
В разделе **Static files**:
- **URL:** `/static/`
- **Directory:** `/home/anarex8332/ubbles-kb/staticfiles`

### 9. Перезагрузите
Нажмите зелёную кнопку **Reload**.

### ✅ Готово!
Сайт: **https://anarex8332.pythonanywhere.com**