from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import EmailUserCreationForm

from django.core.mail import send_mail
from django.contrib.auth.models import User


# Views
def home(request):
    return redirect("pages:homepage_view")
 
def register(request):
    #We'll need the the admin email to notify him/her that a new user has been registered
    admin = User.objects.filter(is_superuser=True).first()
    admin_email = admin.email
    if request.method == 'POST':
        form = EmailUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
             # send an email to the admin
            try:
                send_mail(
                    'Se ha registrado un nuevo usuario', 
                    'Se ha registrado un nuevo usuario en timbaanalitica, recomendamos revisarlo y aprobarlo/desaprobarlo desde la administración', 
                    'contacto@timbaanalitica.com', 
                    [admin_email], 
                    fail_silently=False,
                )
                print("Se ha registrado un nuevo usuario y notificado al admin")
            except:
                print("No se ha podido enviar el email al admin")
            login(request, user)
            return redirect('home')
    else:
        form = EmailUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})