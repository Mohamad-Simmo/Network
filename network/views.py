from email.policy import default
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Exists, OuterRef, F,  Count
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import json
from django.views.decorators.csrf import csrf_exempt
from .models import *


def index(request):
    if request.method == "POST":
        text = request.POST["post-text"]
        Post.objects.create(
            entity = Entity.objects.create(
                user = request.user,
                text = text
            )
        )
        return redirect('index')

    if request.user.is_authenticated:
        posts = Post.objects.annotate(
            is_liked=Exists(
                Like.objects.filter(user=request.user, entity_id=OuterRef('entity_id'))
            )
        ).select_related('entity').order_by('-entity__date', '-entity__id')

        paginator = Paginator(posts, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        return render(request, "network/index.html", {
            'page_obj': page_obj
        })
    posts = Post.objects.all().select_related('entity').order_by('-entity__date', '-entity__id')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, "network/index.html", {
        'page_obj': page_obj
    })

def following(request):
    posts = Post.objects.filter(
        entity__user__followers__in = Follow.objects.filter(
                follower=request.user
            )).annotate(
                is_liked=Exists(
                        Like.objects.filter(
                                user=request.user, entity_id=OuterRef('entity_id')
                            )
                    )
            ).select_related('entity').order_by('-entity__date', '-entity__id')

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, "network/following.html", {
        "page_obj": page_obj
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

def profile(request, user_id):
    user_posts = Post.objects.filter(
        entity__user_id=user_id
    )
    followers = Follow.objects.filter(following_id=user_id).count()
    following = Follow.objects.filter(follower_id=user_id).count()
    user = User.objects.get(id=user_id)
    cover = "style=background-color:{}".format(user.cover)

    if (request.user.is_authenticated):
        posts = user_posts.annotate(
        is_liked=Exists(
            Like.objects.filter(user=request.user, entity_id=OuterRef('entity_id'))
        )).select_related('entity').order_by('-entity__date', '-entity__id')

        is_followed = Follow.objects.filter(follower=request.user, following_id=user_id).exists()

        paginator = Paginator(posts, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, "network/profile.html", {
            "profile" : user,
            "page_obj": page_obj,
            "is_followed": is_followed,
            "followers" : followers,
            "following" : following,
            "cover": cover
        })
    posts = user_posts.select_related('entity').order_by('-entity__date', '-entity__id')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/profile.html", {
        "profile" : user,
        "page_obj": page_obj,
        "followers" : followers,
        "following" : following,
        "cover": cover
    })

def like (request, entity_id):
    if not request.user.is_authenticated:
        return HttpResponse(status=401)
    Like.objects.create(
        entity = Entity.objects.get(id=entity_id),
        user = request.user
    )
    return HttpResponse(status=204)

def unlike (request, entity_id):
    if not request.user.is_authenticated:
        return HttpResponse(status=401)
    Like.objects.get(
        entity = Entity.objects.get(id=entity_id),
        user = request.user
    ).delete()
    return HttpResponse(status=204)

def follow (request, user_id):
    Follow.objects.create(follower=request.user, following_id=user_id)
    return HttpResponseRedirect(reverse("profile", kwargs={'user_id':user_id}))

def unfollow(request, user_id):
    Follow.objects.get(follower=request.user, following_id=user_id).delete()
    return HttpResponseRedirect(reverse("profile", kwargs={'user_id':user_id}))

@csrf_exempt
def edit_post(request, post_id):
    post = Entity.objects.get(pk=post_id);
    data = json.loads(request.body)
    if data.get("new_post") is not None:
        post.text = data["new_post"]
    post.save()
    return HttpResponse(status=204)

def edit_profile(request):
    try:
        pfp = request.FILES["pfp"]
        request.user.pfp = pfp
    except:
        pass
    bio = request.POST["bio"]
    request.user.biography = bio
    color = request.POST["color"]
    request.user.cover = color
    request.user.save()
    return redirect('profile', request.user.id)


def post_view(request, entity_id):
    if(request.method == 'POST'):
        comment = request.POST["comment"]
        Comment.objects.create(
            entity = Entity.objects.create(
                user = request.user,
                text = comment
            ),
            post = Post.objects.get(entity_id=entity_id)
        )
        return redirect('post', entity_id)

    post = Post.objects.get(entity_id=entity_id)
    comments = Comment.objects.filter(post=post).annotate(
                count = Count('entity__likes')
            ).select_related('entity').order_by('-count', '-entity_id', '-entity__date')
    
    context = {}
    if request.user.is_authenticated:
        try:
            is_liked = Exists(Like.objects.get(entity_id=entity_id, user=request.user))
        except:
            is_liked = False

        context["is_liked"] = is_liked

        comments = comments.annotate(
            is_liked = Exists(
                    Like.objects.filter(user=request.user, entity=OuterRef('entity_id'))
                )
        )
    context.update({
            "post": post,
            "comments": comments
        })
        
    return render(request, "network/post.html", context)


def delete_post(request, entity_id):
    try:
        Entity.objects.get(pk=entity_id).delete()
    except:
        return HttpResponse(status=502)
    return HttpResponse(status=200)
    