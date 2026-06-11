from django.core.management.base import BaseCommand
from knowledge.models import Section, Changelog
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Создает начальные данные для базы знаний'

    def handle(self, *args, **options):
        # Создаем разделы
        sections_data = [
            {'name': 'О компании', 'icon': '🏢', 'description': 'Назначение продукта RUBBLES Planning Force, миссия, цели, ценности компании'},
            {'name': 'Команда', 'icon': '👥', 'description': 'Структура команды, роли, контакты, кто за что отвечает'},
            {'name': 'Регламенты', 'icon': '📋', 'description': 'Регламенты работы между специалистами, SLA, процессы взаимодействия'},
            {'name': 'Продукты', 'icon': '⚙️', 'description': 'Описание модулей: прогнозирование спроса, промоакции, производственное планирование, управление запасами, ценообразование, ассортимент'},
            {'name': 'Бизнес-процессы', 'icon': '🧩', 'description': 'Визуальные диаграммы и описания бизнес-процессов'},
            {'name': 'Доступы', 'icon': '🔐', 'description': 'Ролевая модель, политики доступа, процессы управления доступом'},
        ]

        for data in sections_data:
            Section.objects.get_or_create(
                name=data['name'],
                defaults={'icon': data['icon'], 'description': data['description']}
            )
            self.stdout.write(f'  ✓ Раздел: {data["icon"]} {data["name"]}')

        # Создаем подразделы
        company = Section.objects.get(name='О компании')
        products = Section.objects.get(name='Продукты')

        subs = [
            {'name': 'Миссия и ценности', 'parent': company, 'icon': '🎯'},
            {'name': 'История компании', 'parent': company, 'icon': '📜'},
            {'name': 'Прогнозирование спроса', 'parent': products, 'icon': '📊'},
            {'name': 'Промоакции', 'parent': products, 'icon': '🏷️'},
            {'name': 'Управление запасами', 'parent': products, 'icon': '📦'},
            {'name': 'Ценообразование', 'parent': products, 'icon': '💰'},
            {'name': 'Ассортимент', 'parent': products, 'icon': '📋'},
        ]

        for data in subs:
            Section.objects.get_or_create(
                name=data['name'],
                defaults={'icon': data['icon'], 'parent': data['parent']}
            )
            self.stdout.write(f'  ✓ Подраздел: {data["icon"]} {data["name"]}')

        # Создаем changelog записи
        admin = User.objects.filter(is_superuser=True).first()

        changelogs = [
            {
                'version': '1.0.0',
                'title': 'Запуск базы знаний',
                'description': 'Первоначальный запуск базы знаний RUBBLES Planning Force. Добавлены основные разделы и функционал управления документацией.',
            },
            {
                'version': '1.1.0',
                'title': 'Улучшения интерфейса и новый функционал',
                'description': (
                    '• Полный редизайн в стиле Telegram Web с новым сайдбаром, шапкой и карточками\n'
                    '• Тёмная тема с плавным переключателем (сохраняется в localStorage)\n'
                    '• Система уведомлений: колокольчик с red dot, @упоминания в комментариях\n'
                    '• Emoji-пикер при добавлении комментариев\n'
                    '• Боковая панель: секции сворачиваются/разворачиваются по клику\n'
                    '• Увеличенная ширина контента (до 1200px)\n'
                    '• Улучшенная мобильная версия и исправления багов'
                ),
            },
        ]

        for cl in changelogs:
            Changelog.objects.get_or_create(
                version=cl['version'],
                defaults={
                    'title': cl['title'],
                    'description': cl['description'],
                    'author': admin,
                }
            )
            self.stdout.write(f'  ✓ Релиз: v{cl["version"]} — {cl["title"]}')

        self.stdout.write(self.style.SUCCESS('\n✅ Начальные данные успешно созданы!'))
