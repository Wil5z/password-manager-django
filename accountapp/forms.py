from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Savedpasswords

from django.conf import settings
# Create your forms here.

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("first_name","last_name","username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user


class SavenewpassForm(forms.ModelForm):
	of_user = settings.AUTH_USER_MODEL 

	class Meta:
		model = Savedpasswords
		# fields = '__all__'
		exclude = ['slug', 'of_user']


class EditpassForm(forms.ModelForm): 

	class Meta:
		model = Savedpasswords
		# fields = '__all__'
		exclude = ['slug', 'of_user']