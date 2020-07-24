from django.contrib import admin
from .models import Article, Banner, Category, Tag


class TagAdmin(admin.ModelAdmin):
    fields = [
        'name'
    ]


class CategoryAdmin(admin.ModelAdmin):
    fields = [
        'name',
        'index'
    ]


class ArticleAdmin(admin.ModelAdmin):
    # 编辑时分为多个字段集
    fieldsets = [
        ('文章标题', {'fields': ['title']}),
        ('封面', {'fields': ['cover']}),
        ('分类和标签', {'fields': ['category', 'tags']}),
        ('文章内容', {'fields': ['abstract', 'content']}),
        ('阅读量', {'fields': ['views'], 'classes': ['collapse']}),
    ]

    # 文章列表里显示想要显示的字段
    list_display = ('id', 'title', 'category', 'views', 'created_time')

    # 满50条数据就自动分页
    list_per_page = 50

    # 后台数据列表排序方式
    ordering = ('-created_time',)

    # 设置哪些字段可以点击进入编辑界面
    list_display_links = ('id', 'title')

    # 设置后台查询时用的字段
    search_fields = ['title']

    # 用来过滤字段的过滤器
    list_filter = ['created_time', 'modified_time']


class ArticleInline(admin.StackedInline):
    model = Article
    extra = 2


class BannerAdmin(admin.ModelAdmin):
    # 编辑时的排列顺序
    fields = [
        'text_info',
        'img',
        'link',
        'is_active',
        'index'
    ]


admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Banner, BannerAdmin)
