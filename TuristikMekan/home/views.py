from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from home.models import Setting, ContactFormu, ContactFormMessage
from mekan.models import Category, Mekan


def index(request):
    setting = Setting.objects.get(pk=1)
    sliderdata = Mekan.objects.all()[:10]
    category = Category.objects.all()
    context = {
        'setting': setting,
        'sliderdata': sliderdata,
        'category': category,
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
