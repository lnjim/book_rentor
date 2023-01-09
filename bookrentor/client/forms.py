from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from bibliotheque.models import Genre, Editor, Author, Book, Library, BooksInLibrary, LibraryLocation

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

class NewRentBookForm(forms.Form):
    rent_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    return_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    quantity = forms.IntegerField()

class SearchBookForm(forms.Form):
    title = forms.CharField(max_length=100, required=False)
    author = forms.CharField(max_length=100, required=False)
    genre = forms.ModelChoiceField(queryset=Genre.objects.all(), required=False)
    editor = forms.ModelChoiceField(queryset=Editor.objects.all(), required=False)
    library = forms.ModelChoiceField(queryset=Library.objects.all(), required=False)
    location = forms.ModelChoiceField(queryset=LibraryLocation.objects.all(), required=False)

class SearchLibraryForm(forms.Form):
    location = forms.ModelChoiceField(queryset=LibraryLocation.objects.all())