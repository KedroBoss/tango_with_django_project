from django import forms
from django.contrib.auth.models import User
from rango.models import Page, Category, UserProfile, CATEGORY_NAME_LENGTH, PAGE_TITLE_LENGTH


class CategoryForm(forms.ModelForm):
    """Form for adding Catrgory"""
    name = forms.CharField(max_length=CATEGORY_NAME_LENGTH,
                           help_text="Enter the category name")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        """Meta definition for Categoryform."""

        model = Category  # Associations between the ModelForm and a model
        fields = ('name',)


class PageForm(forms.ModelForm):
    """Form for creating Page"""

    title = forms.CharField(
        max_length=PAGE_TITLE_LENGTH, help_text="Enter the title of the page.")
    url = forms.URLField(
        max_length=200, help_text="Enter the URL of the page.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        """Meta definition for Pageform."""

        model = Page
        exclude = ('category',)
        #fields = ('title','url','views',)

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        if url and not url.startswith('http://'):
            url = 'http://' + url
            cleaned_data['url'] = url

            return cleaned_data


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')
