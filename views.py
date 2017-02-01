from django.shortcuts import render, redirect
from .models import User, Poke
from django.contrib import messages
# Create your views here.
def index(request):
    return render(request, 'Poke/index.html')

def register(request):
    if request.method == 'POST':
        print request.POST
        response_from_models = User.objects.add_user(request.POST)
        # if failed validations
        if not response_from_models['status']:
            for error in response_from_models['errors']:
                messages.error(request, error)
            return redirect('Poke:index')
        # if true on validations
        else:
            request.session['user_id'] = response_from_models['user'].id
            return redirect('Poke:pokes')
    else:
        return redirect('Poke:index')

def login(request):
    response_from_models = User.objects.check_user(request.POST)
    if not response_from_models['status']:
        for error in response_from_models['errors']:
            messages.error(request, error)
        return redirect('Poke:index')
    else:
        request.session['user_id'] = response_from_models['user_id']
        # request.session['alias'] = response_from_models['alias']
        return redirect('Poke:pokes')

def pokes(request):
    if request.method == 'POST':
        print request.POST
        Poke.objects.pokes(request.POST)
        return redirect('Poke:pokes')
    else:
        pokes = {
            'name': User.objects.get(id = request.session['user_id']),
            'users': User.objects.all().exclude(id = request.session['user_id']).order_by('-id'),
            'count': Poke.objects.filter(user__id = request.session['user_id']).count(),
            'counts': Poke.objects.all().count(),
            'mypokes': Poke.objects.all().exclude(user__id = request.session['user_id']).order_by('-id'),
            'pokes': Poke.objects.all().order_by('-id'),
        }
        return render(request, 'Poke/pokes.html', pokes)

def logout(request):
    request.session.clear()
    return redirect('Poke:index')
