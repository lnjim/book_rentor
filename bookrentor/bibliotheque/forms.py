from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class NewGenreForm(forms.Form):
    name = forms.CharField(max_length=200)

class NewEditorForm(forms.Form):
    name = forms.CharField(max_length=200)

class NewAuthorForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    date_of_birth = forms.DateField(required=False)
    date_of_death = forms.DateField(required=False)

class NewBookForm(forms.Form):
    title = forms.CharField(max_length=200)
    author = forms.ChoiceField()
    editor = forms.ChoiceField()
    summary = forms.CharField(max_length=1000)
    genre = forms.ChoiceField()

class NewLibraryForm(forms.Form):
    name = forms.CharField(max_length=200)
    location = forms.CharField(max_length=200)

class NewBooksInLibraryForm(forms.Form):
    book = forms.ChoiceField()
    library = forms.ChoiceField()
    quantity = forms.IntegerField()