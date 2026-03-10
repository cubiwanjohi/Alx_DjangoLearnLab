# blog/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q

from .forms import CustomUserCreationForm, PostForm, CommentForm
from .models import Post, Comment, Tag


# -----------------------
# AUTHENTICATION VIEWS
# -----------------------

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('blog:profile')

        messages.error(request, 'Registration failed. Please correct the errors.')

    else:
        form = CustomUserCreationForm()

    return render(request, 'blog/register.html', {'form': form})


def login_view(request):

    if request.method == 'POST':

        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Logged in successfully!')
            return redirect('blog:profile')

        messages.error(request, 'Login failed. Check username and password.')

    else:
        form = AuthenticationForm()

    return render(request, 'blog/login.html', {'form': form})


def logout_view(request):

    logout(request)

    messages.info(request, 'You have been logged out.')

    return redirect('blog:login')


@login_required
def profile_view(request):

    user = request.user

    if request.method == 'POST':

        user.username = request.POST.get('username')
        user.email = request.POST.get('email')

        user.save()

        messages.success(request, 'Profile updated successfully!')

    return render(request, 'blog/profile.html')


# -----------------------
# BLOG POST CRUD VIEWS
# -----------------------

class PostListView(ListView):

    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date']
    paginate_by = 5


class PostDetailView(DetailView):

    model = Post
    template_name = 'blog/post_detail.html'


class PostCreateView(LoginRequiredMixin, CreateView):

    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):

        form.instance.author = self.request.user
        response = super().form_valid(form)

        tags = form.cleaned_data.get("tags")

        if tags:

            tag_list = [tag.strip() for tag in tags.split(",")]

            for tag_name in tag_list:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                self.object.tags.add(tag)

        messages.success(self.request, 'Post created successfully!')

        return response


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):

    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):

        response = super().form_valid(form)

        tags = form.cleaned_data.get("tags")

        if tags:

            tag_list = [tag.strip() for tag in tags.split(",")]

            self.object.tags.clear()

            for tag_name in tag_list:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                self.object.tags.add(tag)

        messages.success(self.request, 'Post updated successfully!')

        return response


    def test_func(self):

        post = self.get_object()

        return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):

    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')

    def test_func(self):

        post = self.get_object()

        return self.request.user == post.author


# -----------------------
# COMMENT CRUD VIEWS
# -----------------------

class CommentCreateView(LoginRequiredMixin, CreateView):

    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def form_valid(self, form):

        form.instance.author = self.request.user
        form.instance.post_id = self.kwargs['post_id']

        messages.success(self.request, 'Comment added successfully!')

        return super().form_valid(form)


    def get_success_url(self):

        return self.object.post.get_absolute_url()


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):

    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def form_valid(self, form):

        messages.success(self.request, 'Comment updated successfully!')

        return super().form_valid(form)


    def test_func(self):

        return self.request.user == self.get_object().author


    def get_success_url(self):

        return self.object.post.get_absolute_url()


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):

    model = Comment
    template_name = 'blog/comment_confirm_delete.html'

    def test_func(self):

        return self.request.user == self.get_object().author


    def get_success_url(self):

        return self.object.post.get_absolute_url()


@login_required
def add_comment(request, post_id):

    post = get_object_or_404(Post, pk=post_id)

    if request.method == 'POST':

        form = CommentForm(request.POST)

        if form.is_valid():

            comment = form.save(commit=False)

            comment.post = post
            comment.author = request.user

            comment.save()

            messages.success(request, 'Comment added successfully!')

            return redirect('blog:post_detail', pk=post.pk)

        messages.error(request, 'There was an error adding your comment.')

    else:

        form = CommentForm()

    return render(request, 'blog/add_comment.html', {'form': form, 'post': post})


# -----------------------
# SEARCH FUNCTIONALITY
# -----------------------

def search_posts(request):

    query = request.GET.get("q")

    results = []

    if query:

        results = Post.objects.filter(

            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__name__icontains=query)

        ).distinct()

    return render(

        request,
        "blog/search_results.html",
        {"query": query, "results": results}

    )


# -----------------------
# POSTS BY TAG
# -----------------------

def posts_by_tag(request, tag_name):

    tag = get_object_or_404(Tag, name=tag_name)

    posts = tag.posts.all()

    return render(

        request,
        "blog/tag_posts.html",
        {"tag": tag, "posts": posts}

    )