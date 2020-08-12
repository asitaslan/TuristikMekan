from django.contrib import messages
import json

from django.contrib.auth import logout, login, authenticate
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

# Create your views here.
from home.forms import SearchForm, SignUpForm
from home.models import Setting, ContactFormu, ContactFormMessage, UserProfile
from mekan.models import Category, Mekan, Images, Comment


def index(request):
    setting = Setting.objects.get(pk=1)
    sliderdata = Mekan.objects.all()[:4]
    category = Category.objects.all()
    lastmekans= Mekan.objects.all().order_by('-id')[:4]
    randommekans = Mekan.objects.all().order_by('?')[:9]
    context = {
        'setting': setting,
        'sliderdata': sliderdata,
        'category': category,
        'lastmekans' : lastmekans,
        'mekans' : mekans,
        'randommekans': randommekans,

    }
    return render(request, 'index.html', context)

def hakkimizda(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    context = {'setting': setting, 'category': category, 'page': 'hakkimizda'}
    return render(request, 'hakkimizda.html', context)


def mekans(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    mekans = Mekan.objects.all()
    context = {'setting': setting, 'category': category, 'page': 'mekans' , 'mekans' : mekans}
    return render(request, 'mekans.html', context)


def iletisim(request):
    category = Category.objects.all()
    if request.method == 'POST':  # form post edildiyse
        form = ContactFormu(request.POST)
        if form.is_valid():
            data = ContactFormMessage()  # model ile bağlantı kur
            data.name = form.cleaned_data['name']  # formdan bilgiyi al
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()  # veritabanına kaydet
            messages.success(request, "Mesajınız başarı ile gönderilmiştir. Teşekkür Ederiz")
            return HttpResponseRedirect('/iletisim')
    setting = Setting.objects.get(pk=1)
    form = ContactFormu()
    context = {'setting': setting, 'category': category, 'form': form}
    return render(request, 'iletisim.html', context)


def mekans_category(request, id, slug):
    category = Category.objects.all()
    categorydata = Category.objects.get(pk=id)
    mekans= Mekan.objects.filter(category_id=id)
    context = {'mekans': mekans,
               'category': category,
               'categorydata': categorydata
               }
    return render(request, 'mekans.html', context)

def mekans_detail(request, id, slug):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    mekan = Mekan.objects.get(pk=id)
    images = Images.objects.filter(mekan_id=id)
    comments = Comment.objects.filter(mekan_id=id, status='True')
    context = {'mekan': mekan,
               'category': category,
               'images': images,
               'comments': comments,
               'setting': setting,

               }
    return render(request, 'mekans_detail.html', context)


def mekan_search(request):
    setting = Setting.objects.get(pk=1)
    if request.method == 'POST':  # Check form post
        form = SearchForm(request.POST)  # Get form data
        if form.is_valid():
            category = Category.objects.all()

            query = form.cleaned_data['query']  # Get form data
            catid = form.cleaned_data['catid']  # Get form data

            if catid == 0:
                mekans = Mekan.objects.filter(
                    title__icontains=query)  # Select * from mekan where title like %query%
            else:
                mekans = Mekan.objects.filter(title__icontains=query, category_id=catid)
            # return HttpResponse(mekans)
            context = {'mekans': mekans,
                       'category': category,
                       'setting': setting,
                       }
            return render(request, 'mekans_search.html', context)
    return HttpResponseRedirect('/')


def mekan_search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        mekan = Mekan.objects.filter(title__icontains=q)
        results = []
        for rs in mekan:
            mekan_json = {}
            mekan_json = rs.title
            results.append(mekan_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def login_view(request):
    setting = Setting.objects.get(pk=1)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return HttpResponseRedirect('/')
        else:
            messages.error(request, "Hatalı Giriş! Kullanıcı adı ve ya şifre yanlış")
            return HttpResponseRedirect('/login')
    category = Category.objects.all()
    context = {
        'category': category,
        'setting': setting,
               }
    return render(request, 'login.html', context)

def signup_view(request):
    setting = Setting.objects.get(pk=1)
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            login(request, user)
            current_user = request.user
            data = UserProfile()
            data.user_id = current_user.id
            data.image = 'images/users/user.png'
            data.save()
            messages.success(request, "Hoş geldiniz... Sitemize başarılı bir şekilde üye oldunuz.")
            return HttpResponseRedirect('/')

    form = SignUpForm()
    category = Category.objects.all()
    context = {'category': category,
               'form': form,
               'setting': setting,
               }
    return render(request, 'signup.html', context)