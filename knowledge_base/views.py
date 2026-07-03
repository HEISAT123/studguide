from django.shortcuts import render, get_object_or_404
from .models import Category, Article

def home(request):
    # US-01: Выводим все категории на главную
    categories = Category.objects.all()
    return render(request, 'knowledge_base/home.html', {'categories': categories})

def category_detail(request, slug):
    # US-02: Статьи конкретной категории
    category = get_object_or_404(Category, slug=slug)
    # Показываем только опубликованные статьи, черновики прячем!
    articles = Article.objects.filter(category=category, status='published')
    return render(request, 'knowledge_base/category_detail.html', {'category': category, 'articles': articles})

def article_detail(request, slug):
    # US-03: Полный текст статьи
    article = get_object_or_404(Article, slug=slug, status='published')
    return render(request, 'knowledge_base/article_detail.html', {'article': article})
