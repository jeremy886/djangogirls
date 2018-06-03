from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from . import models
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import Http404
# CBV below
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

def post_list(request):
    posts = models.Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


class SearchView(ListView):
    template_name = "blog/post_list.html"
    context_object_name = "posts"

    def get_queryset(self):
        search_term = self.request.GET.get("term")
        posts = models.Post.objects.filter(
            Q(published_date__lte=timezone.now()),
            Q(title__icontains=search_term) | Q(text__icontains=search_term)
        ).order_by('-published_date')
        return posts


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
        """
        Without select_related or prefetch related:
            7 SQL queries, takes 3.99 ms
        With prefetch_related
            8 SQL queries, takes 0.5 ms
        With select_related
            5 SQL queries, takes 15.66 ms

        Not very sure if it is necessary to use these techniques.
        """
        username = self.kwargs.get("username")
        # try:
        #     posts = models.Post.objects.select_related('author').filter(author__username=username)
        # except models.Post.DoesNotExist:
        #     raise Http404
        # else:
        #     return posts

        posts = models.Post.objects.filter(author__username=username)
        return posts



