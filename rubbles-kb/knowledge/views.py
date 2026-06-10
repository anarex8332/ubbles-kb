from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib import messages
from .models import Section, Article, ArticleVersion, Comment, Bookmark, RecentlyViewed, Changelog, Notification


def home(request):
    """Главная страница со списком последних статей и changelog'ом"""
    recent_articles = Article.objects.filter(status='published').order_by('-updated_at')[:5]
    recent_changelogs = Changelog.objects.filter(is_published=True)[:3]
    return render(request, 'knowledge/home.html', {
        'recent_articles': recent_articles,
        'recent_changelogs': recent_changelogs,
    })


def section_detail(request, slug):
    """Страница раздела со списком статей"""
    section = get_object_or_404(Section, slug=slug, is_active=True)
    articles = Article.objects.filter(section=section, status='published')
    sub_sections = section.get_children().filter(is_active=True)
    return render(request, 'knowledge/section.html', {
        'section': section,
        'articles': articles,
        'sub_sections': sub_sections,
    })


def article_detail(request, slug):
    """Страница статьи"""
    article = get_object_or_404(Article, slug=slug, status='published')

    # Увеличиваем счетчик просмотров
    article.views_count += 1
    Article.objects.filter(pk=article.pk).update(views_count=article.views_count)

    # Сохраняем в недавние, если пользователь авторизован
    if request.user.is_authenticated:
        RecentlyViewed.objects.update_or_create(
            user=request.user,
            article=article,
            defaults={'viewed_at': __import__('django').utils.timezone.now()}
        )

    comments = article.comments.filter(is_active=True)
    is_bookmarked = False
    if request.user.is_authenticated:
        is_bookmarked = Bookmark.objects.filter(user=request.user, article=article).exists()

    return render(request, 'knowledge/article.html', {
        'article': article,
        'comments': comments,
        'is_bookmarked': is_bookmarked,
    })


def search(request):
    """Поиск по статьям"""
    query = request.GET.get('q', '').strip()
    articles = Article.objects.none()
    if query:
        articles = Article.objects.filter(
            Q(status='published') &
            (Q(title__icontains=query) | Q(content__icontains=query))
        ).distinct()
    return render(request, 'knowledge/search.html', {
        'query': query,
        'articles': articles,
    })


@login_required
def article_create(request):
    """Создание новой статьи"""
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()
        section_id = request.POST.get('section')
        if title and content:
            article = Article.objects.create(
                title=title,
                content=content,
                content_markdown=content,
                section_id=section_id or None,
                author=request.user,
            )
            messages.success(request, 'Статья успешно создана!')
            return redirect('knowledge:article_detail', slug=article.slug)
        messages.error(request, 'Заполните заголовок и содержание статьи.')

    sections = Section.objects.filter(is_active=True)
    return render(request, 'knowledge/article_form.html', {
        'sections': sections,
        'is_edit': False,
    })


@login_required
def article_edit(request, slug):
    """Редактирование статьи"""
    article = get_object_or_404(Article, slug=slug)

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()
        if title and content:
            # Сохраняем текущую версию в историю
            ArticleVersion.objects.create(
                article=article,
                version_number=article.version,
                title=article.title,
                content=article.content,
                content_markdown=article.content_markdown,
                author=article.author,
                change_summary=request.POST.get('change_summary', ''),
            )
            article.title = title
            article.content = content
            article.content_markdown = content
            article.section_id = request.POST.get('section') or article.section_id
            article.version += 1
            article.is_outdated = False
            article.save()
            messages.success(request, 'Статья обновлена!')
            return redirect('knowledge:article_detail', slug=article.slug)
        messages.error(request, 'Заполните заголовок и содержание статьи.')

    sections = Section.objects.filter(is_active=True)
    return render(request, 'knowledge/article_form.html', {
        'article': article,
        'sections': sections,
        'is_edit': True,
    })


@login_required
def article_version_history(request, slug):
    """История версий статьи"""
    article = get_object_or_404(Article, slug=slug)
    versions = article.versions.all()
    return render(request, 'knowledge/version_history.html', {
        'article': article,
        'versions': versions,
    })


@login_required
def article_restore_version(request, slug, version_number):
    """Восстановить версию статьи"""
    article = get_object_or_404(Article, slug=slug)
    version = get_object_or_404(ArticleVersion, article=article, version_number=version_number)
    if request.method == 'POST':
        ArticleVersion.objects.create(
            article=article,
            version_number=article.version,
            title=article.title,
            content=article.content,
            content_markdown=article.content_markdown,
            author=request.user,
            change_summary=f'Откат к версии {version.version_number}',
        )
        article.title = version.title
        article.content = version.content
        article.content_markdown = version.content_markdown
        article.version += 1
        article.save()
        messages.success(request, f'Статья восстановлена к версии {version_number}')
        return redirect('knowledge:article_detail', slug=article.slug)
    return render(request, 'knowledge/version_restore.html', {
        'article': article,
        'version': version,
    })


@login_required
def toggle_bookmark(request, slug):
    """Добавить/удалить закладку"""
    article = get_object_or_404(Article, slug=slug)
    bookmark, created = Bookmark.objects.get_or_create(user=request.user, article=article)
    if not created:
        bookmark.delete()
    return redirect('knowledge:article_detail', slug=slug)


@login_required
def add_comment(request, slug):
    """Добавить комментарий к статье"""
    article = get_object_or_404(Article, slug=slug)
    if request.method == 'POST' and article.allow_comments:
        text = request.POST.get('text', '').strip()
        if text:
            comment = Comment.objects.create(article=article, author=request.user, text=text)
            
            # Уведомление автору статьи о новом комментарии
            if article.author and article.author != request.user:
                Notification.objects.create(
                    user=article.author,
                    article=article,
                    message=f'Новый комментарий от {request.user.username} к статье "{article.title[:50]}"',
                    notification_type='comment_added',
                    from_user=request.user,
                )
            
            # Уведомления пользователям, упомянутым через @username
            import re
            mentions = re.findall(r'@(\w+)', text)
            for username in mentions:
                try:
                    mentioned_user = User.objects.get(username=username)
                    if mentioned_user != request.user:
                        Notification.objects.create(
                            user=mentioned_user,
                            article=article,
                            message=f'{request.user.username} упомянул вас в комментарии к статье "{article.title[:50]}"',
                            notification_type='comment_mention',
                            from_user=request.user,
                        )
                except User.DoesNotExist:
                    pass
    
    return redirect('knowledge:article_detail', slug=slug)


def changelog_list(request):
    """Список релизов"""
    changelogs = Changelog.objects.filter(is_published=True)
    return render(request, 'knowledge/changelog.html', {'changelogs': changelogs})


@login_required
def mark_article_outdated(request, slug):
    """Переключить статус устаревшей статьи (toggle)"""
    article = get_object_or_404(Article, slug=slug)
    if request.method == 'POST':
        if article.is_outdated:
            article.is_outdated = False
            article.save()
            messages.success(request, 'Статья снова актуальна')
        else:
            article.is_outdated = True
            article.save()
            messages.warning(request, 'Статья помечена как устаревшая')
    return redirect('knowledge:article_detail', slug=slug)


@login_required
def recently_viewed_list(request):
    """Страница со списком недавних статей"""
    articles = RecentlyViewed.objects.filter(user=request.user)
    return render(request, 'knowledge/recently_viewed.html', {
        'articles': articles,
    })


@login_required
def bookmark_list(request):
    """Страница со списком закладок"""
    bookmarks = Bookmark.objects.filter(user=request.user)
    return render(request, 'knowledge/bookmarks.html', {
        'bookmarks': bookmarks,
    })


@login_required
def notification_list(request):
    """Список уведомлений пользователя"""
    notifications = Notification.objects.filter(user=request.user)
    return render(request, 'knowledge/notifications.html', {
        'notifications': notifications,
    })


@login_required
def notification_read(request, pk):
    """Отметить уведомление как прочитанное"""
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.is_read = True
    notification.save()
    if notification.article:
        return redirect('knowledge:article_detail', slug=notification.article.slug)
    return redirect('knowledge:notification_list')
