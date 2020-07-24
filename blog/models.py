from django.db import models
from ckeditor.fields import RichTextField


class Category(models.Model):
    """分类表"""

    name = models.CharField(max_length=100, unique=True)
    index = models.IntegerField(default=999)

    def __str__(self):
        return self.name

    class Meta:
        # 排序方式按照index排序
        ordering = ["index"]
        verbose_name = '分类'
        verbose_name_plural = '分类'


class Tag(models.Model):
    """标签表"""

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = '标签'


class Article(models.Model):
    """文章表"""

    title = models.CharField(max_length=128)
    content = RichTextField(blank=True, null=True)
    abstract = models.TextField(max_length=500, blank=True, null=True)
    cover = models.ImageField(upload_to='article_cover/%Y/%m/%d/',
                              verbose_name='文章封面', blank=True, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.DO_NOTHING, blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True)
    views = models.PositiveIntegerField(default=0)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_time"]
        verbose_name = '文章'
        verbose_name_plural = '文章'

    def __str__(self):
        return self.title


class Banner(models.Model):
    """幻灯片表"""

    text_info = models.CharField(max_length=50, default='')
    img = models.ImageField(upload_to='banner/')
    link = models.URLField(max_length=100)
    is_active = models.BooleanField(default=False)
    index = models.IntegerField(default=999)

    def __str__(self):
        return self.text_info

    class Meta:
        ordering = ["index"]
        verbose_name = '幻灯片'
        verbose_name_plural = '幻灯片'
