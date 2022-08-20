from autoslug import AutoSlugField
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

# Create your models here.

# create product catalog models
class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = AutoSlugField(unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self) -> str:
        return self.name

    # def get_absolute_url(self):
    #     return reverse("app:product_list_by_category", args=[self.slug])

    


# Product class model
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200, db_index=True)
    slug = AutoSlugField(unique=True)
    image = models.FileField(upload_to='app/images/products', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-name',)
        index_together = (('id','slug'),)

    def __str__(self) -> str:
        return self.name 

    # def get_absolute_url(self):
    #     return reverse("app:product_details", args=[self.id, self.slug])


class ContactForm(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    subject = models.CharField(max_length=200)
    message = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.name
        
    
class UserCreateForm(UserCreationForm):
    """We are going to create custome user here"""

    email = forms.EmailField(required=True, label="Email", error_messages={'exists':'This email is already exists.'})

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['password1'].widget.attrs['placeholder'] = 'Choose Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


    def clean_email(self):
        """Validate Email here"""

        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError(self.fields['email'].error_messages)

        return self.cleaned_data['email']


class Order(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.IntegerField()
    address = models.CharField(max_length=150)
    pincode = models.IntegerField()

    def __str__(self) -> str:
        return self.name
