from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import DetailView, CreateView
from django.views.generic.edit import UpdateView, DeleteView
from requests.api import get
from .models import Post
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PostCreateForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from users.decorators import expert_required
from users.models import Investor
from .request import get_news


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'posts/post_delete.html'
    success_url = reverse_lazy('home')

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'posts/update.html'
    fields = ('body', 'image',)

class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'posts/post_detail.html'


@login_required
@expert_required
def create_post(request):
    form = PostCreateForm()
    if request.method == 'POST':
        form = PostCreateForm(request.POST)
        if form.is_valid():
                author = request.user
                post = form.save(commit=False)
                post.author = author
                post.save()
                
                # data = []
                # item = {"id": post.id, "body": post.body, "author": post.author.username,}
                # data.append(item)
                return redirect('home')
    return render(request, 'posts/addpost.html', {"form": form})

@require_POST
@csrf_exempt
def post_like(request):
    post_id = request.POST.get('id')
    action = request.POST.get('action')
    post = Post.objects.get(id=post_id)

    if post_id and action:
       
        if action == 'like':
            post.likes.add(request.user)
        else:
            post.likes.remove(request.user)
        return JsonResponse({"status": "ok"})

    else:
        return JsonResponse({"status": "error"})

def interesing_news(request, interest):
    # user = request.user 
    # if user.is_investor:
    #       user = Investor.objects.get(user=request.user)
    #       interests = user.interests.all()
    # for item in interests:
    #     print(item)
    news = get_news(interest)
    return render(request, 'posts/blog.html', {"news": news, "interest": interest})

