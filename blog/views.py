from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from . import models
from .forms import PostForm
from django.contrib.auth.decorators import login_required
# CBV below
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

def post_list(request):
    posts = models.Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

@login_required
def post_draft_list(request):
    posts = models.Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

@login_required
def post_publish(request, pk):
    post = get_object_or_404(models.Post, pk=pk)
    post.publish()
    return redirect('blog:post_detail', pk=pk)

def post_detail(request, pk):
    post = get_object_or_404(models.Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # post.published_date = timezone.now()
            post.save()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(models.Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # post.published_date = timezone.now()
            post.save()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_remove(request, pk):
    post = get_object_or_404(models.Post, pk=pk)
    post.delete()
    return redirect('blog:post_list')


# CBV below


class ListUserPost(LoginRequiredMixin, ListView):
    template_name = "blog/user_post_list.html"

    def get_queryset(self):
        username = self.kwargs.get("username")
        posts = models.Post.objects.filter(author__username=username)
        return posts