from django.contrib.auth.models import User
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)        # 카테고리 이름
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)    # 한글인코딩

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return "/blog/category/{}".format(self.slug)

    class Meta:
        verbose_name_plural = 'Categories'

# Post 모델
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    pub_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    photo = models.ImageField(upload_to='blog/images/%Y/%m/%d/',
                              null=True, blank=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, null=True, blank=True,
                            on_delete=models.SET_NULL)
    # 카테고리가 삭제되어도 블로그는 유지됨(미분류가 있을 수 있다)

    def __str__(self):
        return self.title
