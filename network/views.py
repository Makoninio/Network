from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from datetime import datetime
from django.core.paginator import Paginator
import json
from django.http import JsonResponse

from .models import User, Post, Following


def index(request):
    posts = Post.objects.all().order_by('post_date').reverse()
    page = Paginator(posts, 10)

    page_number = request.GET.get('page')
    page_obj = page.get_page(page_number)

    return render(request, "network/index.html", {
        'page_obj': page_obj
    })

def profile(request, user_id):
    user = User.objects.get(pk=user_id)
    posts = Post.objects.filter(user=user).order_by('post_date').reverse()

    following = Following.objects.filter(follower=user)
    followers = Following.objects.filter(followed=user)
    
    try:
        checkFollow = followers.filter(user=User.objects.get(pk=request.user.id))
        if len(checkFollow) != 0:
            isFollowing = True
        else:
            isFollowing = False
    except:
        isFollowing = False


    page = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = page.get_page(page_number)

    
    return render(request, "network/profile.html", {
        'page_obj': page_obj,
        'name': user.username,
        'following': following,
        'followers': followers,
        "user_profile": user,
        "isFollowing": isFollowing,  
    })

def following(request):
    user = User.objects.get(pk=request.user.id)
    following = Following.objects.filter(follower=user)
    posts = Post.objects.all().order_by('id').reverse()
    
    postsfollowing = []
    
    for post in posts:
        for person in following:
            if person.followed == post.user:
                postsfollowing.append(post)
                
    # Pagination
    page = Paginator(postsfollowing, 10)
    page_number = request.GET.get('page')
    page_obj = page.get_page(page_number)
    
    return render(request, "network/following.html", {
        'page_obj': page_obj
    })

def follow(request):
    userfollow = request.POST['userfollow']
    currentUser = User.objects.get(pk=request.user.id)
    userfollowData = User.objects.get(username=userfollow)
    f = Following(follower=currentUser, followed=userfollowData)
    f.save()

    user_id = userfollowData.id
    return HttpResponseRedirect(reverse(profile, kwargs={'user_id': user_id}))

def unfollow(request):
    userfollow = request.POST['userfollow']
    currentUser = User.objects.get(pk=request.user.id)
    userfollowData = User.objects.get(username=userfollow)
    f = Following.objects.get(follower=currentUser, followed=userfollowData)
    f.delete()
    user_id = userfollowData.id
    return HttpResponseRedirect(reverse(profile, kwargs={'user_id': user_id}))


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

def new_post(request):
    if request.method == "POST":
        content = request.POST["post"]

        post = Post(
            user = request.user,
            content = content
        )
        post.save()
        return HttpResponseRedirect(reverse('index'))

    else:
        return render(request, 'network/new_post.html')

def edit(request, post_id):
    if request.method == "POST":
        data = json.loads(request.body)
        edit_post = Post.objects.get(pk=post_id)
        edit_post.content = data["content"]
        edit_post.save()
        return JsonResponse({"message": "Changes saved", "data": data["content"]})
