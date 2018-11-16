from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User
import bcrypt

def index(request):
	request.session.clear()
	return render(request, 'login/index.html')

def create(request):
	errors = User.objects.basic_validator(request.POST)
	if len(errors):
		for key, value in errors.items():
			messages.error(request, value)
		return redirect('/')
	else:
		password = request.POST['password']
		password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
		User.objects.create(first_name= request.POST['first_name'], last_name = request.POST['last_name'], email= request.POST['email'], password= password)

	return redirect('/')

def login(request):
	errors = User.objects.login_validator(request.POST)
	if len(errors):
		for key, value in errors.items():
			messages.info(request, value)
		return redirect('/')
	else: 
		request.session['email'] = request.POST['email_log']

	return redirect('/logged')

def logged(request):

	return render(request, 'login/success.html')
