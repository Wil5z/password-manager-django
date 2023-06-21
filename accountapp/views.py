from django.shortcuts import  render, redirect
from .forms import NewUserForm, SavenewpassForm, EditpassForm
from django.contrib.auth import login
from django.contrib import messages

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth import login, authenticate, logout

from django.views.generic.edit import FormView, CreateView,DeleteView, UpdateView
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from . models import Savedpasswords
from . encrypt_util import *
from django.conf import settings

from django.contrib.auth.models import User

from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm,PasswordResetForm

#for password reset -- imports
from django.core.mail import send_mail, BadHeaderError
# from django.http import HttpResponse

from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib import messages
#added new
from django.contrib.messages.views import SuccessMessageMixin


#working password reset
@login_required
def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "accountapp/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')

					# messages.success(request, 'A message with reset password instructions has been sent to your inbox.')
					# return redirect ("/password_reset/done/")
					messages.success(request, 'A message with reset password instructions has been sent to your inbox.')
					return redirect ("homepage")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="accountapp/password_reset.html", context={"password_reset_form":password_reset_form})





















def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("homepage")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="accountapp/register.html", context={"register_form":form})

# def home(request):
#     return render(request, "accountapp/home.html")

class HomeView(LoginRequiredMixin,ListView):
	model = Savedpasswords
	template_name = "accountapp/home.html"
	context_object_name = 'password_list'
	raise_exception = True
	permission_denied_message = "please login"

	def get_queryset(self):
		return self.model.objects.filter(of_user=self.request.user) 
	






def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("homepage")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="accountapp/login.html", context={"login_form":form})



@login_required
def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("userlogin")


class SavenewView(LoginRequiredMixin,CreateView):
	# model = Savedpasswords
	form_class = SavenewpassForm
	template_name = "accountapp/savepassword.html"
	success_url = "home"

	def form_valid(self, form):
		form.instance.of_user = self.request.user
		# print(self.request.user)
		form.instance.password = encrypt(form.instance.password)
		# print("original : "+form.instance.password)
		# print("decrypted: "+form.instance.password)
		messages.success(self.request, "New entry saved successfully." )#added new
		return super(SavenewView,self).form_valid(form)
	

	# def form_valid(self, form):
	# 	instance = form.save(commit = False)
	# 	instance.password = encrypt(str(instance.password))
	# 	instance.save()
	# 	return super(SavenewView,self).form_valid(form)


# class DetialsView(DetailView):
# 	template_name = "accountapp/details.html"
# 	model = Savedpasswords
# 	context_object_name= "password"
	
@login_required
def DetialView(request, pk):
	password = get_object_or_404(Savedpasswords, pk = pk)
	if password.password is not None:
		password.password = decrypt(password.password)
	else:
		password.password = ""
	# print(password.password)
	return render(request, "accountapp/details.html", context={
		"password":password 
		})

	
#added SuccessMessageMixin new
class DeletePassView(SuccessMessageMixin,LoginRequiredMixin,DeleteView):
	model = Savedpasswords
	success_url = "/home"
	template_name = "accountapp/confirm-delete.html"
	context_object_name = "password"

	success_message = "Saved account data deleted successfully! " #added new
	



#added SuccessMessageMixin new
class EditPassView(SuccessMessageMixin,LoginRequiredMixin,UpdateView):
	model = Savedpasswords
	form_class = EditpassForm
	template_name = "accountapp/update-pass.html"

	success_message = "password updated successfully! " #added new

	def get_object(self):
		queryset = self.get_queryset()
		obj = queryset.get(pk = self.kwargs['pk'])
		obj.password = decrypt(obj.password)
		return obj


	def form_valid(self, form):
		self.object = form.save(commit = False)
		# print(self.object.password)
		self.object.password = encrypt(self.object.password)
		# print(self.object.password)
		self.object.save()
		return super().form_valid(form)




class AccountinfoView(LoginRequiredMixin,DetailView):
	template_name = "accountapp/account-info.html"
	model = User
	context_object_name = "cur_user"

	#added to fix multiple user signin on same browser and get respective data
	def get_queryset(self):
		return self.model.objects.filter(pk=self.request.user.pk) 
	


#---------------! working account delete class view ------------------#
# class DeleteAccView(LoginRequiredMixin,DeleteView):
# 	model = User
# 	success_url = "/login"
# 	template_name = "accountapp/confirm-acc-del.html"
# 	context_object_name = "User"

def DeleteAccView(request, pk):
	context ={} 
	try:
		current_user = User.objects.get(pk=pk)
		# current_user.delete() # working delete option
		current_user.is_active = False # making active false but not deleting
		current_user.save()
	except current_user.DoesNotExist:
		context['msg'] = e.message
	return redirect('/login') #redirecting working
	# return render(request, "accountapp/confirm-acc-del.html", context) 
	
	

#change user password
#added SuccessMessageMixin new
class PassChangeView(SuccessMessageMixin,LoginRequiredMixin,PasswordChangeView):
	template_name = "accountapp/change-pass.html"
	form_class = PasswordChangeForm
	success_url = '/login'

	success_message = "Account password changed successfully! " #added new


class Template404View(TemplateView):
	template_name = "accountapp/404.html"
