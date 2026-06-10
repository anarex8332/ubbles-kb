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

        # Создаем начальный changelog
        admin = User.objects.filter(is_superuser=True).first()
        Changelog.objects.get_or_create(
            version='1.0.0',
            defaults={
                'title': 'Запуск базы знаний',
                'description': 'Первоначальный запуск базы знаний RUBBLES Planning Force. Добавлены основные разделы и функционал управления документацией.',
                'author': admin,
            }
        )
        self.stdout.write('  ✓ Релиз: v1.0.0 — Запуск базы знаний')

        self.stdout.write(self.style.SUCCESS('\n✅ Начальные данные успешно созданы!'))