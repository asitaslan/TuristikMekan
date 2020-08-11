from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from home.models import Setting, ContactFormu, ContactFormMessage
from mekan.models import Category, Mekan, Images, Comment


def index(request):
    setting = Setting.objects.get(pk=1)
    sliderdata = Mekan.objects.all()[:10]
    category = Category.objects.all()
    lastmekans= Mekan.objects.all()[:6]
    context = {
        'setting': setting,
        'sliderdata': sliderdata,
        'category': category,
         'lastmekans' : lastmekans,
    }
    return render(request, 'index.html', context)

def hakkimizda(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    context = {'setting': setting, 'category': category, 'page': 'hakkimizda'}
    return render(request, 'hakkimizda.html', context)


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