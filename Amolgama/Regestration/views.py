from django.shortcuts import redirect, render
from django.urls import reverse
from django.http import Http404, HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib import messages
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from Models import UserRegistrationForm, PostForm
from Models.post import Post
import json
from django.core.mail import send_mail
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from time import timezone


User = get_user_model()

def generate_code():
    return random.randint(100000, 999999)

def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        email = request.POST.get("email")

        if form.is_valid():
            if User.objects.filter(email=email, is_verified=True).exists():
                form.add_error("email", "Пользователь c таким E-MAIL уже зарегистрирован!")
            else:
                user = form.save(commit=False) 
                user.is_verified = False  
                user.save()
                
                code = generate_code()  
                user.code = code  
                user.save()

                subject = "Ваш код подтверждения"
                message = f"Ваш код подтверждения: {user.code}"
                send_mail(subject, message, "noreply@example.com", [email])

                # Перенаправлення на сторінку введення коду
                return redirect("verify_code", email=email)

                message = f"<h3>Ваш код подтверждения - {code}</h3>"
                
                
                return redirect("email_confirmation", email=email)  

    else:
        form = UserRegistrationForm()

    return render(request, "registration/register.html", {"form": form})

from django.shortcuts import render, redirect

def verify_code(request, email):
    """Перевірка коду підтвердження"""
    if request.method == "POST":
        code_entered = request.POST.get("code")
        try:
            user = User.objects.get(email=email, is_verified=False)

            if user.code == code_entered:
                user.is_verified = True
                user.code = None  # Очистити код після успішної перевірки
                user.save()

                # Авторизуємо користувача
                login(request, user)
                
                messages.success(request, "Ваш аккаунт успешно подтвержден!")
                return redirect("home")  # Перенаправлення на головну сторінку
            else:
                messages.error(request, "Неверный код! Попробуйте еще раз.")
        except User.DoesNotExist:
            messages.error(request, "Пользователь не найден или уже подтвержден.")

    return render(request, "code/index.html", {"email": email})


def main(request):
    if request.user.is_authenticated:
        return redirect("user-account")  # Якщо користувач увійшов – перенаправити його
    return render(request, "Registration/index.html")  # Підключаємо HTML-файл



def email_confirmation(request, email):
    emil_obj = email
    if request.method == "POST":
        if User.objects.get(email= emil_obj, is_verificated= False).exists():
             code = User.objects.get(email= emil_obj).code
             data = request.POST
             data_code = data["code"]        
             if data_code == str(code):
                    User.objects.filter(email= emil_obj).update(is_vereficated= True)
                    quser =User.objects.get(email= emil_obj)
                    login(request, quser)
        return redirect("/")
    context = {"email":email}
    return render(request, "Code/index.html", context)
   

    
@login_required(login_url = "/")
def find_users(request):
    search_query = request.GET.get("search")
    if search_query:
        users = User.object.filter(first_name__icontains =search_query.capitalize(), is_vereficated = True).exclude(id = request.user.id)
    else:
        users = User.object.aii().filter (is_vereficated = True).exclude(id = request.user.id)
    context = {
        "users": users,
        "search_query": search_query,
    } 
    return render(request, "Amalgama/index.html", context)



from django.http import HttpResponse
from django.shortcuts import redirect, render
from Models.post import Post
from django.contrib.auth.decorators import login_required
from django.utils import timezone


@login_required(login_url= "/")
def delete_post(request):
    try:
        post_id = request.POST.get("post_id")
        print(post_id)
        return HttpResponse(
            json.dumps({
                "result": True,
            }),
            content_tupe = "application/json")
    except Exception as ex:
        return HttpResponse(
            json.dumps({
                "result": False,
            }),
            content_tupe = "application/json")
    
@login_required(login_url= "/")
def create_post(request):
    if request.method == "POST":
        data = request.POST
        print(request.FILES)
        form = PostForm(request.POST, request.FILES)
        if form.is_valid() and data["post_text"] !="":
            form = PostForm(request.POST, request.FILES)
            new_post = form.save(commit= False)
            new_post.author = request.user
            new_post.post_time = timezone.now()
            new_post.save()
            error = None
            return redirect("/")
        else:
            error = "Ми не можем опубликовать пустоту. Напиши текст."
    else:
        error = None
    context ={"error": error}
    return render(request, "Ad_Post/index.html", context)


@login_required(login_url = "/")
def edit_post(request):
    return None