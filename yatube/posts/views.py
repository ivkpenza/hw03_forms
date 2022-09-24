from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm
from .models import Group, Post, User


# Главная страница.
def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_list(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'posts': posts,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=author).order_by('-pub_date')
    post_count = len(posts)
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'author': author,
        'post_count': post_count,
        'page_obj': page_obj,
        'username': username,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    author_post = post.author
    post_count = Post.objects.filter(author=author_post).count()
    context = {
        'post': post,
        'post_count': post_count,
        'author_post': author_post,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    is_edit = False
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect(f'/profile/{request.user.username}/')
    else:
        form = PostForm()
    context = {
        'form': form,
        'is_edit': is_edit,
    }
    return render(request, 'posts/post_create.html', context)


@login_required
def post_edit(requst, post_id):
    post = get_object_or_404(Post, pk=post_id)
    is_edit = True
    form = PostForm(requst.POST or None, instance=post)
    if requst.user.pk != post.author.pk:
        return redirect('posts:post_detail', post.pk)
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post.pk)
    context = {
        'form': form,
        'is_edit': is_edit,
        'post_id': post_id,
    }
    return render(requst, 'posts/post_create.html', context)
