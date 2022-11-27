from django.shortcuts import render, redirect, get_object_or_404, reverse
from .forms import ArticleForm
from django.contrib import messages
from .models import Article, Comment
from django.contrib.auth.decorators import login_required
import time
from functools import wraps

# Create your views here.

def timer(func):
    """helper function to estimate view execution time"""

    @wraps(func)  # used for copying func metadata
    def wrapper(*args, **kwargs):
        # record start time
        start = time.time()

        # func execution
        result = func(*args, **kwargs)
        
        duration = (time.time() - start) * 1000
        # output execution time to console
        print('view {} takes {:.2f} ms'.format(
            func.__name__, 
            duration
            ))
        return result
    return wrapper



@timer
def articles(request):
    keyword = request.GET.get("keyword")
    if keyword:
        articles = Article.objects.filter(title__contains = keyword)
        return render(request, "article/articles.html", {"articles": articles})
        
    articles = Article.objects.all()
    return render(request, "article/articles.html", {"articles": articles})
       
@timer
def index(request):    
    return render(request, "article/index.html")

@timer
def about(request):
    return render(request, "article/about.html")

@login_required(login_url="user:login")    
@timer
def dashboard(request):
    # defer(), only(), select_related() olaylarını öğren !
    articles = Article.objects.filter(author = request.user).defer("content")
    context = {
        "articles": articles
    }
    return render(request, "article/dashboard.html", context)
    

@login_required(login_url="user:login")
@timer
def addArticle(request):
    form  = ArticleForm(request.POST or None)
    if form.is_valid():
        article = form.save(commit=False)
        article.author = request.user
        article.save()
        messages.success(request, "Başarıyla Kaydedildi...")  
        return redirect("article:dashboard")
    return render(request, "article/addarticle.html", {"form": form})

@timer
def detail(request, id):
    # article = Article.objects.filter(id = id).first()
    article = get_object_or_404(Article, id = id)
    comments = article.comments.all()
    return render(request, "article/detail.html", {"article": article, "comments": comments})

@login_required(login_url="user:login")
@timer
def updateArticle(request, id):    
    article = get_object_or_404(Article, id = id)
    form = ArticleForm(request.POST or None, instance=article)
    if article.author != request.user:
        messages.warning(request, "Bu makaleyi değiştirme yetkiniz yok!")
        return render(request, "article/update.html", {"form": form})
    elif form.is_valid():
        article = form.save(commit=False)
        article.author = request.user
        article.save()
        messages.success(request, "Başarıyla Güncellendi...")
        return redirect("article:dashboard")             
    return render(request, "article/update.html", {"form": form})

@login_required(login_url="user:login")
def deleteArticle(request, id):
    article = get_object_or_404(Article, id = id)
    article.delete()
    messages.success(request, "Makale başarıyla silindi")
    return redirect("article:dashboard")      

def addComment(request, id):
    article = get_object_or_404(Article, id = id)
    if request.method == "POST":
        comment_author = request.POST.get("comment_author")
        comment_content = request.POST.get("comment_content")
        if comment_author and comment_content:
            newComment = Comment(comment_author = comment_author, comment_content = comment_content)
            newComment.article = article
            newComment.save()
            messages.success(request, "Yorumunuz başarıyla gönderildi")
        else:
            messages.warning(request, "Lütfen ilgili alanları doldurunuz..")

    return redirect(reverse("article:detail", kwargs={"id": id}))
