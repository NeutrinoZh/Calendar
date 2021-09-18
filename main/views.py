from django.http.response import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.shortcuts import render
from django.urls import reverse
from .models import Event
import datetime

def index(request):
    # Тут переадрисация на текущий день

    now = datetime.datetime.now()
    return HttpResponseRedirect(reverse('day', args=[now.strftime("%Y-%m-%d")]))

def day(request, pk):
    # Здесь, отображение событий на конкретный день.
    
    if not request.user.is_authenticated: # Если пользователь не авторизован переадресовываем на логин 
        return HttpResponseRedirect(reverse('login'))

    user_events = Event.objects.filter(user=request.user)
    events = user_events.filter(date=pk)
    month = (pk[-5:])[:2]
    year = pk[:4]
    
    return render(request, 'index.html', { 'day': pk[-2:], 'month': month, 'year': year, 'events': events })

def detail(request, pk):
    # Детали события

    if not request.user.is_authenticated: # Если пользователь не авторизован переадресовываем на логин 
        return HttpResponseRedirect(reverse('login'))

    event = Event.objects.get(id=pk)
    
    # Здесь проверяем принадлежит ли это событие этому пользователю      
    return render(request, 'detail.html', { 'event': event, 'guest': event.user != request.user })

def add(request, pk):
     # Добавление событий

    if not request.user.is_authenticated: # Если пользователь не авторизован переадресовываем на логин 
        return HttpResponseRedirect(reverse('login'))

    if request.method == 'POST': # Если есть запрос формируем новое событие
        event = Event()
        event.title = request.POST['title']      
        event.text = request.POST['text'] 
        event.user = request.user

        event.date = pk

        event.save()
        return HttpResponseRedirect(reverse('edit', args=[event.id]))

    # Иначе возвращаем форму
    return render(request, 'add.html', { 'date': pk })

def edit(request, pk):
    # Редактирование события

    if not request.user.is_authenticated: # Если пользователь не авторизован переадресовываем на логин 
        return HttpResponseRedirect(reverse('login'))

    event = Event.objects.get(id=pk)
    if event.user != request.user: # Если это событие не этого пользователя, переадресовываем на главную
        return HttpResponseRedirect(reverse('index'))

    if request.method == 'POST': # Если есть запрос то редактируем
        event.title = request.POST['title']
        event.text = request.POST['text']
        event.save()

        return HttpResponseRedirect(reverse('day', args=[event.date]))

    # Иначе возвращаем форму
    return render(request, 'add.html', { 'event': event, 'date': event.date })

def addParticipant(request, pk):
    if request.method == 'POST':
        try:
            event = Event.objects.get(id=pk)
            if event.user != request.user: # Если это событие не этого пользователя, кидаем ошибку
                return HttpResponse('error')

            user = User.objects.get(username=request.POST['name'])
            event.participants.add(user)
            event.save()
        except:
            return HttpResponse('error')
    return HttpResponse('success')

def remParticipant(request, pk):
    if request.method == 'POST':
        try:
            event = Event.objects.get(id=pk)
            if event.user != request.user: # Если это событие не этого пользователя, кидаем ошибку
                return HttpResponse('error')
                
            user = User.objects.get(username=request.POST['name'])
            event.participants.remove(user)
            event.save()
        except:
            return HttpResponse('error')
    return HttpResponse('success')

def participant(request):
    events = Event.objects.filter(participants__in=[request.user])
    return render(request, 'participant.html', { 'events': events })

def remove(request, pk):
    # Удаление события, и последующая переадрисация на главную страницу

    if not request.user.is_authenticated: # Если пользователь не авторизован переадресовываем на логин 
        return HttpResponseRedirect(reverse('login'))
    
    event = Event.objects.get(id=pk)
    if event.user != request.user: # Если это событие не этого пользователя, переадресовываем на главную
        return HttpResponseRedirect(reverse('index'))
    
    # Если этого - удалем, и переадресовываем на главную 
    event.delete()
    del event

    return HttpResponseRedirect(reverse('index'))