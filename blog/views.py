from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Article, Banner, Category, Tag


# 获取全部页面都有的一些参数, 包括所有分类, 标签和热门文章
def getGlobalParameter():
    categories = Category.objects.all()
    tags = Tag.objects.all()
    hot_articles = Article.objects.order_by('-views')[:5]
    result = {'categories': categories, 'category_link': '/categories/',
              'tags': tags, 'tag_link': '/tags/',
              'hot_articles': hot_articles, 'article_link': '/articles/'}
    return result


# 获取给定文章的基本信息
def getArticlesInfo(articles, has_content=False):
    articles_info = []
    # 所有文章的除内容外的信息
    for article in articles:
        info = {'id': article.id, 'title': article.title, 'cover': article.cover,
                'abstract': article.abstract, 'views': article.views,
                'category': article.category, 'tags': article.tags.all(),
                'created_time': article.created_time,
                'link': '/articles/{}'.format(article.id)
                }
        if has_content:
            info.update({'content': article.content})
        articles_info.append(info)

    return articles_info


# 获取给定文章的分页信息和当前页面的文章
def getPageInfoAndArticles(articles, current_page=1, pages_num=5):
    paginator = Paginator(articles, pages_num)
    if current_page < 0 or current_page > paginator.num_pages:
        current_page = 1
    current_articles = paginator.page(current_page)
    page_info = {'pages': paginator.page_range, 'current': current_page,
                 'has_next': current_articles.has_next(), 'has_previous': current_articles.has_previous}
    return page_info, current_articles


# 首页
def index(request):
    # 获取当前请求的页面
    try:
        current_page = int(request.GET.get(
            "page")) if request.GET.get("page") else 1
    except:
        current_page = 1
    # 获取页面信息和当前页面的文章
    page_info, articles = getPageInfoAndArticles(
        Article.objects.all(), current_page=current_page, pages_num=5)
    # 获取幻灯片
    banners = Banner.objects.filter(is_active=True)
    # 将所有内容传递给模板
    content = {'page_info': page_info,
               'banners': banners, 'articles': getArticlesInfo(articles)}
    content.update(getGlobalParameter())
    return render(request, 'blog/index.html', content)


# 文章内容页
def article(request, id):
    article = Article.objects.get(id=id)
    # 更新该文章阅读数
    article.views += 1
    article.save()
    # 获取包括内容在内的文章信息, 并将文章信息加入content传递给模板
    content = {'article': getArticlesInfo([article], has_content=True)[0]}
    content.update(getGlobalParameter())
    return render(request, 'blog/article.html', content)


def category(request, category):
    # 获取当前请求的页面
    try:
        current_page = int(request.GET.get(
            "page")) if request.GET.get("page") else 1
    except:
        current_page = 1
    # 获取页面信息和当前页面的同类文章
    page_info, articles = getPageInfoAndArticles(
        Article.objects.filter(category__name=category), current_page=current_page, pages_num=5)
    content = {'page_info': page_info, 'articles': getArticlesInfo(articles)}
    content.update(getGlobalParameter())
    return render(request, 'blog/category.html', content)


def tag(request, tag):
    # 获取当前请求的页面
    try:
        current_page = int(request.GET.get(
            "page")) if request.GET.get("page") else 1
    except:
        current_page = 1
    # 获取页面信息和当前页面的同类文章
    page_info, articles = getPageInfoAndArticles(
        Article.objects.filter(tags__name=tag), current_page=current_page, pages_num=5)
    content = {'page_info': page_info, 'articles': getArticlesInfo(articles)}
    content.update(getGlobalParameter())
    return render(request, 'blog/tag.html', content)


def search(request):
    q = request.GET.get('q')  # 获取搜索的关键词q
    try:
        current_page = int(request.GET.get(
            "page")) if request.GET.get("page") else 1
    except:
        current_page = 1
    content = {}
    if q != None:
        # 获取到搜索关键词通过标题进行匹配
        page_info, articles = getPageInfoAndArticles(
            Article.objects.filter(title__icontains=q), current_page=current_page, pages_num=5)
        content = {'q': q,
                   'page_info': page_info,
                   'articles': getArticlesInfo(articles)}
    content.update(getGlobalParameter())
    return render(request, 'blog/search.html', content)
