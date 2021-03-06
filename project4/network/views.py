import json

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt

from .models import User, Posts, Follow


def index(request):
    posts = Posts.objects.order_by('-timestamp')
    p = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)
    return render(request, "network/index.html", {
        'posts': page_obj
    })

@csrf_exempt
@login_required
def edit(request, editw):
    if request.method == 'POST':
        data = json.loads(request.body)
        post = Posts.objects.get(id= data['id'])
        if editw == 'edit':
            post.text = data['text']
            post.save()
            return JsonResponse(post.serialize()) 
        elif editw == 'likes':
            user = User.objects.get(username=request.user)
            try:
                post.likes.get(username=user.username)
                post.likes.remove(user)
            except:
                post.likes.add(user)
            post.save()
            return JsonResponse(post.serialize())
    return JsonResponse({'error': 'error'})


@login_required
def following(request):
    a, created = Follow.objects.get_or_create(user=request.user)
    follows = a.follows.all()
    posts = Posts.objects.none()
    for f in follows:
        posts |= Posts.objects.filter(user=f)
    posts = posts.order_by('-timestamp')
    p = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)
    return render(request, "network/following.html", {
       'posts': page_obj
    })


@login_required
def new_post(request):
    if request.method == 'POST':
        user = request.user
        text = request.POST['text']
        Posts.objects.create(user=user, text=text).save()
    return HttpResponseRedirect(reverse("index"))


@login_required
def follow(request):
    profile = request.POST['profile']
    profile = User.objects.get(username=profile)
    follow, created = Follow.objects.get_or_create(user=request.user)
    if request.POST['button'] == 'Follow':
        follow.follows.add(profile)
    else:
        follow.follows.remove(profile)
    return HttpResponseRedirect(reverse("profile", args=(profile.username,)))

    
def profile(request, profile):
    profile = User.objects.get(username=profile)
    a, created = Follow.objects.get_or_create(user=profile)
    try:
        profile.followersf.get(user=User.objects.get(username=request.user))
        fo_or_un = True
    except:
        fo_or_un = False
    posts = profile.postsp.all()
    posts = posts.order_by('-timestamp')
    p = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)
    return render(request, 'network/profile.html', {
        'profile': a.user,
        'follows': a.follows,
        'followers': profile.followersf.all(),
        'posts': page_obj,
        'fo_or_un': fo_or_un
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
