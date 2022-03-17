from django.contrib.auth.decorators import login_required

from blog.models import Post, Category
from django.shortcuts import render, get_object_or_404, redirect

from blog.forms import PostForm
from django.utils import timezone


def index(request):
    # 포스트 목록
    post_list = Post.objects.order_by('-pub_date')    # ('pk'대신'-pub_date')최근작성일 - 내림차순
    categories = Category.objects.all()
    context = {'post_list':post_list, 'categories' :categories}
    return render(request, 'blog/post_list.html', context)

def detail(request, post_id):
    # 상세 페이지
    post = get_object_or_404(Post, pk=post_id)
    # post = Post.objects.get(id=post_id)  # 포스트 1개 가져오기
    categories = Category.objects.all()
    context = {'post':post, 'categories' :categories}
    return render(request, 'blog/post_detail.html', context)

def category_page(request, slug):
    # 카테고리
    category = Category.objects.get(slug=slug)
    post_list = Post.objects.filter(category=category)
    categories = Category.objects.all()
    context = {
        'category' :category,
        'post_list' :post_list,
        'categories' :categories
    }
    return render(request, 'blog/post_list.html', context)

@login_required(login_url='common:login')
def post_create(request):
    # 포스트 쓰기
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.pub_date = timezone.now()
            post.author = request.user     # 작성자
            post.save()     # db에 저장
            return redirect('blog:index')
    else:
        form = PostForm()
    context = {'form':form}
    return render(request, 'blog/post_form.html', context)


