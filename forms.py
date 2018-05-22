from django import forms
from datetime import datetime
from django.forms.extras.widgets import SelectDateWidget
from django.contrib.auth.models import User
from django.db import connection, transaction
from system.models import ChartStyleList,ChartThemeList,PriorityList,ThemeList,Statistic,Theme,Sequences,Framework,FrameworkList,TimelineList
    
class NoteForm(forms.Form):
    title = forms.CharField(label='Title', max_length=100, initial='')
    tags = forms.CharField(label='Tags', max_length=100, initial='')
    
class TagForm(forms.Form):
    title = forms.CharField(label='Title', max_length=100, initial='')

class IdeaForm(forms.Form):
    name= forms.CharField(label='Title', max_length=200, initial='')
    text= forms.CharField(widget=forms.Textarea,label='', max_length=1000, initial='')
    
class LinkForm(forms.Form):
    name= forms.CharField(label='Title', max_length=200, initial='')
    text= forms.CharField(label='URL', max_length=1000, initial='')

class TodoForm(forms.Form):
    name= forms.CharField(label='Title', max_length=200, initial='')
    text= forms.CharField(widget=forms.Textarea,label='', max_length=1000, initial='')

class RegistrationForm(forms.Form):
    username = forms.CharField(label='Userame', max_length=30, initial='')
    email = forms.EmailField(label='Email', max_length=75, initial='')
    password1 = forms.CharField(widget=forms.PasswordInput(),label='Password', max_length=200, initial='')
    password2 = forms.CharField(widget=forms.PasswordInput(),label='Password (again)', max_length=200, initial='')

    def signup(self,username,email,password1,password2):
        if password1==password2:
            user = User.objects.create_user(username, email, password1)
            user.is_staff=False
            user.save()
            
            chartstylelist=ChartStyleList()
            chartstylelist.user=user
            chartstylelist.chartstyle=1
            chartstylelist.save()
            
            themelist=ThemeList()
            themelist.user=user
            themelist.theme=Theme.objects.filter(name = "Blue")[0]
            themelist.save()
            
            chartthemelist=ChartThemeList()
            chartthemelist.charttheme=0
            chartthemelist.user=user
            chartthemelist.save()
            
            prioritylist=PriorityList()
            prioritylist.user=user
            prioritylist.priority=10
            prioritylist.save()
            
            statistic=Statistic()
            statistic.user=user
            statistic.tags=0
            statistic.notes=0
            statistic.links=0
            statistic.ideas=0
            statistic.todos=0
            statistic.problems=0
            statistic.projects=0
            statistic.files=0
            statistic.save()
            
            for o in Framework.objects.all():
                fl=FrameworkList()
                fl.user=user
                fl.framework=o
                fl.active=True
                fl.save()
    
            o=TimelineList()
            o.user=user
            o.show=1
            o.save()

