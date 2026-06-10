from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from slugify import slugify
from mptt.models import MPTTModel, TreeForeignKey


class Section(MPTTModel):
    """Раздел базы знаний"""
    name = models.CharField('Название', max_length=200)
    slug = models.SlugField('Slug', max_length=200, unique=True, blank=True)
    description = models.TextField('Описание', blank=True)
    icon = models.CharField('Иконка', max_length=50, blank=True, help_text='Emoji для раздела')
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                            related_name='children', verbose_name='Родительский раздел')
    order = models.PositiveIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активен', default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class MPTTMeta:
        order_insertion_by = ['order', 'name']

    class Meta:
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'
        ordering = ['order', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Article(models.Model):
    """Статья базы знаний"""
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('published', 'Опубликовано'),
        ('archived', 'В архиве'),
    ]

    title = models.CharField('Заголовок', max_length=500)
    slug = models.SlugField('Slug', max_length=500, unique=True, blank=True)
    content = models.TextField('Содержимое (HTML)')
    content_markdown = models.TextField('Содержимое (Markdown)', blank=True)
    section = TreeForeignKey(Section, on_delete=models.CASCADE, related_name='articles',
                             verbose_name='Раздел', null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                               related_name='articles', verbose_name='Автор')
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='published')
    is_outdated = models.BooleanField('Устаревшая', default=False)
    outdated_notification_sent = models.BooleanField(default=False)
    version = models.PositiveIntegerField('Версия', default=1)
    allow_comments = models.BooleanField('Разрешить комментарии', default=True)
    views_count = models.PositiveIntegerField('Просмотры', default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['status', 'updated_at']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)
            slug = base
            counter = 1
            while Article.objects.filter(slug=slug).exists():
                slug = f"{base}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class ArticleVersion(models.Model):
    """Версия статьи"""
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='versions')
    version_number = models.PositiveIntegerField('Номер версии')
    title = models.CharField(max_length=500)
    content = models.TextField()
    content_markdown = models.TextField(blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    change_summary = models.TextField('Описание изменений', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Версия статьи'
        verbose_name_plural = 'Версии статей'
        ordering = ['-version_number']
        unique_together = ['article', 'version_number']

    def __str__(self):
        return f"{self.article.title} v{self.version_number}"


class Comment(models.Model):
    """Комментарий к статье"""
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField('Текст комментария')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField('Активен', default=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['created_at']

    def __str__(self):
        return f"{self.author.username} - {self.article.title[:50]}"


class Bookmark(models.Model):
    """Закладка (избранное) пользователя"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='bookmarks')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Закладка'
        verbose_name_plural = 'Закладки'
        unique_together = ['user', 'article']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} -> {self.article.title[:50]}"


class RecentlyViewed(models.Model):
    """Недавно просмотренные статьи"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recently_viewed')
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Недавний просмотр'
        verbose_name_plural = 'Недавние просмотры'
        ordering = ['-viewed_at']
        unique_together = ['user', 'article']

    def __str__(self):
        return f"{self.user.username} -> {self.article.title[:50]}"


class Changelog(models.Model):
    """Запись о релизе/изменении"""
    version = models.CharField('Версия', max_length=50)
    title = models.CharField('Заголовок', max_length=300)
    description = models.TextField('Описание изменений', blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    is_published = models.BooleanField('Опубликовано', default=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Релиз'
        verbose_name_plural = 'Релизы'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.version} - {self.title}"