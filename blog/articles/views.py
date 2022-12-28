from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .models import Article

from django.http import Http404
from django.contrib.auth.models import User

from django.contrib.auth import authenticate,login,logout


def archive(request):
    return render(request, 'archive.html', {"posts": Article.objects.all()})


def get_article(request, article_id):
    try:
        post = Article.objects.get(id=article_id)
        return render(request, 'article.html', {"post": post})
    except Article.DoesNotExist:
        raise Http404


def newpost(request):
    if not request.user.is_anonymous:

        if request.method == "POST":
        # обработать данные формы, если метод POST
            form = {
                'text': request.POST["text"], 'title':  request.POST["title"].strip()
            }

        # в словаре form будет храниться информация, введенная пользователем
            if form["text"] and form["title"]:
        # если поля заполнены без ошибок + проверка уникальности
                unic = Article.objects.filter(title = form["title"])

                if not unic:
                    article = Article.objects.create(text=form["text"], title=form["title"], author=request.user)
                    return redirect('get_article', article_id = article.id)
                else:
                    form['errors'] = u"Такая статья уже есть!"
                    return render(request, 'newpost.html', {'form': form})

            # перейти на страницу поста
            else:
        # если введенные данные некорректны
                form['errors'] = u"Не все поля заполнены"
                return render(request, 'newpost.html', {'form': form})

        else:
        # просто вернуть страницу с формой, если метод GET
            return render(request, 'newpost.html', {})

    else:
        raise Http404


def registration_user(request):

    if request.user.is_anonymous:

        if request.method == "POST": 
            form = {
                    'login': request.POST["username"], 'pass': request.POST["password"], 'email': request.POST["email"]
                }
            
            if form["login"] and form["pass"]:

                if len(User.objects.filter(username=form["login"])) == 0:
                    
                    User.objects.create_user(form["login"],form["email"] ,form["pass"])
                    return redirect("../login/")

                else:
                    
                    form['errors'] = u"Такой пользователь уже существует"
                    return render(request, 'registration.html', {'form': form})
            
            else:
        # если введенные данные некорректны
                form['errors'] = u"Не все поля заполнены"
                return render(request, 'registration.html', {'form': form})
        
        else:
        
        # просто вернуть страницу с формой, если метод GET
            return render(request, 'registration.html', {})
    
    else:
        raise Http404



def login_user(request):
    if request.user.is_anonymous:

        if request.method == "POST": 
        
            form = {
                    'login': request.POST["username"], 'pass': request.POST["password"]
                }
        
            if form["login"] and form["pass"]:
        
                if authenticate(username=form["login"], password=form["pass"]):
        
                    login (request,authenticate(username=form["login"], password=form["pass"]))
                    return redirect('../articles/')
        
                else:
        
                    form['errors'] = u"Неправильный пароль или логин"
                    return render(request, 'login.html', {'form': form})
        
            else:
        # если введенные данные некорректны
                form['errors'] = u"Не все поля заполнены"
                return render(request, 'login.html', {'form': form})
        
        else:
        
        # просто вернуть страницу с формой, если метод GET
            return render(request, 'login.html', {})
    
    else:
        raise Http404


def logout_user(request):
    logout(request)
    return redirect("../")


def home(request):
    return render(request, 'home.html', {})


