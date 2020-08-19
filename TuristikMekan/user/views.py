from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from home.models import Setting, UserProfile
from mekan.models import Category, Comment, MekanForm, Mekan, MekanImageForm, Images
from user.forms import UserUpdateForm, ProfileUpdateForm


@login_required(login_url='/login')  # Check login
def index(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    current_user = request.user  # Access User Session information
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {'category': category,
               'profile': profile,
               'setting': setting,

               }
    return render(request, 'user_profile.html', context)

@login_required(login_url='/login')  # Check login
def user_update(request):
    setting = Setting.objects.get(pk=1)
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)  # request.user is user data
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('/user')
    else:
        category = Category.objects.all()
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)
        context = {
            'category': category,
            'user_form': user_form,
            'profile_form': profile_form,
            'setting': setting,
        }
        return render(request, 'user_update.html', context)

@login_required(login_url='/login')  # Check login
def change_password(request):
    setting = Setting.objects.get(pk=1)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated')
            return HttpResponseRedirect('/user')
        else:
            messages.error(request, 'Please correct the error below.<br>' + str(form.errors))
            return HttpResponseRedirect('/user/password')
    else:
        category = Category.objects.all()
        form = PasswordChangeForm(request.user)
        return render(request, 'change_password.html',
                      {
                          'form': form,
                          'category': category,
                          'setting': setting,
        })
@login_required(login_url='/login')  # Check login
def comments(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    current_user = request.user
    comments = Comment.objects.filter(user_id=current_user.id)
    context = {
        'category': category,
        'comments': comments,
        'setting': setting,
    }
    return render(request, 'user_comments.html', context)


@login_required(login_url='/login')  # Check login
def deletecomment(request, id):
    current_user = request.user
    Comment.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, 'Comment delete..')
    return HttpResponseRedirect('/user/comments')

@login_required(login_url='/login')  # Check login
def mekans(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    current_user = request.user
    mekans = Mekan.objects.filter(user_id=current_user.id, status='True')
    context = {
        'category': category,
        'mekans': mekans,
        'setting': setting,
    }
    return render(request, 'user_mekans.html', context)
@login_required(login_url='/login')  # Check login
def addmekan(request):
    setting = Setting.objects.get(pk=1)
    if request.method == 'POST':
        form = MekanForm(request.POST, request.FILES)
        if form.is_valid():
            current_user = request.user
            data = Mekan()  # model ile bağlantı kur
            data.user_id = current_user.id
            data.category = form.cleaned_data['category']
            data.title = form.cleaned_data['title']
            data.keywords = form.cleaned_data['keywords']
            data.description = form.cleaned_data['description']
            data.image = form.cleaned_data['image']
            data.detail = form.cleaned_data['detail']
            data.slug = form.cleaned_data['slug']
            data.sehir = form.cleaned_data['sehir']
            data.ulke = form.cleaned_data['ulke']
            data.status = 'False'
            data.save()  # veritabanına kaydet
            messages.success(request, 'Your Content Insterted Successfuly')
            return HttpResponseRedirect('/user/mekans')
        else:
            messages.success(request, 'Content Form Error:' + str(form.errors))
            return HttpResponseRedirect('/user/addmekan')
    else:
        category = Category.objects.all()
        form = MekanForm()
        context = {
            'category': category,
            'form': form,
            'setting': setting,
        }
        return render(request, 'user_addmekan.html', context)
    
@login_required(login_url='/login')  # Check login
def mekanedit(request, id):
    setting = Setting.objects.get(pk=1)
    mekan = Mekan.objects.get(id=id)
    if request.method == 'POST':
        form = MekanForm(request.POST, request.FILES, instance=mekan)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your mekan Updated Successfuly')
            return HttpResponseRedirect('/user/mekans')
        else:
            messages.success(request, 'mekan Form Error: ' + str(form.errors))
            return HttpResponseRedirect('/user/addmekan/' + str(id))
    else:
        category = Category.objects.all()
        form = MekanForm(instance=mekan)
        context = {
            'category': category,
            'form': form,
            'setting': setting,
        }
        return render(request, 'user_addmekan.html', context)

@login_required(login_url='/login')  # Check login
def mekandelete(request, id):
    current_user = request.user
    Mekan.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, 'mekan deleted...')
    return HttpResponseRedirect('/user/mekans')

def mekanaddimage(request, id):
    if request.method == 'POST':
        lasturl = request.META.get('HTTP_REFERER')
        form = MekanImageForm(request.POST, request.FILES)
        if form.is_valid():
            data = Images()
            data.title = form.cleaned_data['title']
            data.mekan_id = id
            data.image = form.cleaned_data['image']
            data.save()
            messages.success(request, 'Your image has been successfuly uploaded')
            return HttpResponseRedirect(lasturl)
        else:
            messages.warning(request, 'Form Error: ' + str(form.errors))
            return HttpResponseRedirect(lasturl)
    else:
        mekan = Mekan.objects.get(id=id)
        images = Images.objects.filter(mekan_id=id)
        form = MekanImageForm()
        context = {
            'mekan': mekan,
            'images': images,
            'form': form,
        }
        return render(request, 'mekan_galery.html', context)