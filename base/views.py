from multiprocessing import context
from django.shortcuts import render,get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from sqlalchemy import Update
from .models import Post
# Create your views here.


def home(request):
    context = {
        'posts':Post.objects.all()
    }
    return render(request,'base/home.html',context)

class PostListView(ListView):
    model = Post 
    template_name = 'base/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

class UserPostListView(ListView):
    model = Post 
    template_name = 'base/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User,username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')



class PostDetailView(DetailView):
    model = Post
    template_name = 'base/post_detail.html' 
    context_object_name = 'object'

class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post 
    fields = ['title','content']
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Post 
    fields = ['title','content']
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request,'base/about.html',{'title' : 'About'})