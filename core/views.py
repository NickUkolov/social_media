from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from core.models import Profile, Post


@login_required(login_url='signin')
def index(request):
    user_obj = User.objects.get(username=request.user.username)
    profile_obj = Profile.objects.get(user=user_obj)

    posts = Post.objects.all()

    return render(request, 'index.html', {'profile_obj': profile_obj, 'posts': posts})


@login_required(login_url='signin')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':

        if request.FILES.get('image') == None:
            image = user_profile.profile_img
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profile_img = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()

        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profile_img = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()

        return redirect('settings')

    return render(request, 'setting.html', {'user_profile': user_profile})


@login_required(login_url='signin')
def upload(request):

    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']

        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()
        return redirect('/')
    else:
        return redirect('/')


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Enter valid email!')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Enter valid username!')
                return redirect('signup')
            else:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password
                )
                user.save()

                 # log in and redirect to settings
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                # creating profile for new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('settings')

        else:
            messages.info(request, 'Enter matching passwords!')
            return redirect('signup')

    else:
        return render(request, 'signup.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Invalid login or password')
            return redirect('signin')

    else:
        return render(request, 'signin.html')


@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')
