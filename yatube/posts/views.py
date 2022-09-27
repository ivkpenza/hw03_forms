from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm
from .models import Group, Post, User
from .utils import get_page_context


# Главная страница.
def index(request):
    context = get_page_context(Post.objects.all(), request)
    return render(request, 'posts/index.html', context)


def group_list(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    context = {
        'group': group,
        'posts': posts,
    }
    context.update(get_page_context(group.posts.all(), request))
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    context = {
        'author': author,
        'username': username,
    }
    context.update(get_page_context(author.posts.all(), request))
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    context = {
        'post': post,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:profile', request.user.username)
        form = PostForm()
    context = {
        'form': form,
    }
    return render(request, 'posts/post_create.html', context)


@login_required
def post_edit(requst, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if requst.user.pk != post.author.pk:
        return redirect('posts:post_detail', post.pk)
    form = PostForm(requst.POST or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post.pk)
    context = {
        'form': form,
        'post_id': post_id,
        'is_edit': True,
    }
    return render(requst, 'posts/post_create.html', context)
