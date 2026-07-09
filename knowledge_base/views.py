from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Category, Article
import re
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe

def home(request):
    categories = Category.objects.all()
    return render(request, 'knowledge_base/home.html', {'categories': categories})

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    articles_list = Article.objects.filter(category=category, status='published')
    
    paginator = Paginator(articles_list, 10) 
    page_number = request.GET.get('page', 1) 
    articles = paginator.get_page(page_number)
    
    page_range = paginator.get_elided_page_range(articles.number, on_each_side=1, on_ends=1)
    
    return render(request, 'knowledge_base/category_detail.html', {
        'category': category, 
        'articles': articles,
        'page_range': page_range
    })  

def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug, status='published')
    return render(request, 'knowledge_base/article_detail.html', {'article': article})

def search(request):
    if 'q' not in request.GET:
        return render(request, '404.html', status=404)

    query = request.GET.get('q', '').strip()
    articles = []
    error_message = None

    if 'q' in request.GET:
        if len(query) < 2:
            error_message = "Введите не менее 2 символов"
        else:
            # Ищем статьи
            articles_qs = Article.objects.filter(
                Q(title__icontains=query) | 
                Q(content__icontains=query) | 
                Q(category__name__icontains=query),
                status='published'
            ).distinct()
            
            # Умная обработка текста (Сниппеты)
            query_lower = query.lower()
            for article in articles_qs:
                # 1. Очищаем текст от HTML и спецсимволов (&nbsp;)
                plain_text = strip_tags(article.content).replace('&nbsp;', ' ')
                
                # 2. Ищем, на какой позиции находится искомое слово
                idx = plain_text.lower().find(query_lower)
                
                if idx != -1:
                    # Если нашли в тексте: берем 40 символов ДО и 60 ПОСЛЕ слова
                    start = max(0, idx - 40)
                    end = min(len(plain_text), idx + len(query) + 40)
                    
                    snippet = plain_text[start:end]
                    if start > 0: snippet = "..." + snippet
                    if end < len(plain_text): snippet = snippet + "..."
                        
                    # 3. Подсвечиваем найденное слово желтым маркером (Tailwind: bg-yellow-200)
                    highlighted = re.sub(
                        f"({re.escape(query)})", 
                        r'<mark class="bg-yellow-200">\1</mark>', 
                        snippet, 
                        flags=re.IGNORECASE
                    )
                    article.snippet = mark_safe(highlighted)
                else:
                    # Если совпадение только в заголовке, берем просто начало текста
                    snippet = plain_text[:100] + ("..." if len(plain_text) > 100 else "")
                    article.snippet = snippet
                    
            articles = articles_qs
            
    return render(request, 'knowledge_base/search.html', {
        'query': query,
        'articles': articles,
        'error_message': error_message
    })