
from django.shortcuts import render, redirect
from . models import *
from django.contrib import messages
import bcrypt
from django.core.files.storage import FileSystemStorage


# Create your views here.
def home(request):
    return render (request, 'itoys/home.html')

def main(request):
    context = {
        'inventory' : Add.objects.all()
    }
    return render (request, 'itoys/main.html', context)

def contact(request):
    if request.method == 'POST':
        first_name = request.POST['f_name']
        last_name = request.POST['l_name']
        email = request.POST['email']
        description = request.POST['description']
        contact = Contact(first_name=first_name, last_name=last_name, email=email, description=description)
        contact.save()
        print('This is a request')
    return render(request, 'itoys/contact.html')

def registration(request):
    return render (request, 'itoys/registration.html')


def register(request):
    if request.method == 'POST':
        errors=User.objects.validator(request.POST)
        if errors:
            for error in errors:
                messages.error(request,errors[error])
            return redirect('/')

        user_pw = request.POST['pw']
        hash_pw = bcrypt.hashpw(user_pw.encode(), bcrypt.gensalt()).decode()
        print(hash_pw)
        new_user = User.objects.create(first_name=request.POST['f_n'], last_name=request.POST['l_n'], email=request.POST['email'], password=hash_pw)
        print(new_user)
        request.session['user_id']=new_user.id
        request.session['user_name']=f"{new_user.first_name} {new_user.last_name}"
        return redirect('/main' )
    return redirect('/')


def login(request):
    if request.method == 'POST':
        logged_user=User.objects.filter(email=request.POST['email'])
        if logged_user:
            logged_user=logged_user[0]
            if bcrypt.checkpw(request.POST['pw'].encode(), logged_user.password.encode()):
                request.session['user_id']=logged_user.id
                request.session['user_name']=f"{logged_user.first_name} {logged_user.last_name}"
                return redirect('/main')
    return redirect('/')

def logout(request):
    request.session.flush()
    return redirect ('/')

def create_add(request):
    if request.method == 'POST':
        errors=Add.objects.validator(request.POST)
        if errors:
            for error in errors:
                messages.error(request, errors[error])
            return redirect ('/main')
        
        new_post = Add.objects.create(name=request.POST['name'], age=request.POST['age'], city=request.POST['city'], condition=request.POST['condition'], desc=request.POST['desc'], header_image=request.FILES['header_image'], creator = User.objects.get(id=request.session['user_id']))
        print(new_post)
        new_post.members.add(User.objects.get(id=request.session['user_id']))
        return redirect('/main')



def delete_add(request, add_id):
    Add.objects.get(id=add_id).delete()
    return redirect ('/main')
