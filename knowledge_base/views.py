from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Category, Article

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
    
    return render(request, 'knowledge_base/category_detail.html', {'category': category, 'articles': articles})

def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug, status='published')
    return render(request, 'knowledge_base/article_detail.html', {'article': article})

def search(request):
    query = request.GET.get('q', '').strip()
    articles = []
    error_message = None

    if query:
        if len(query) < 2:
            error_message = "Введите не менее 2 символов"
        else:
            articles = Article.objects.filter(
                Q(title__icontains=query) | 
                Q(content__icontains=query) | 
                Q(category__name__icontains=query),
                status='published'
            ).distinct()
            
    return render(request, 'knowledge_base/search.html', {
        'query': query,
        'articles': articles,
        'error_message': error_message
    })