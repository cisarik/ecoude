from django.db import models
from django.contrib.auth.models import User

class Shellserver(models.Model):
    port=models.IntegerField()
    state=models.CharField(max_length=10)

class Sequences(models.Model):
    problems=models.IntegerField()
    problemlists=models.IntegerField()
    tags=models.IntegerField()
    taglists=models.IntegerField()
    problemtaglists=models.IntegerField()
    notes=models.IntegerField()
    links=models.IntegerField()
    linklists=models.IntegerField()
    ideas=models.IntegerField()
    idealists=models.IntegerField()
    todos=models.IntegerField()
    todolists=models.IntegerField()
    projects=models.IntegerField()
    sourcecodefiles=models.IntegerField()
    inputfiles=models.IntegerField()
    outputfiles=models.IntegerField()
    inputgeneratorfiles=models.IntegerField()
    projectlinklists=models.IntegerField()
    projectidealists=models.IntegerField()
    projecttodolists=models.IntegerField()

    def __unicode__(self):
        return 'Sequence'

class Framework(models.Model):
    name=models.CharField(max_length=200)
    dir=models.CharField(max_length=200)
    extension=models.CharField(max_length=5)
    coding=models.CharField(max_length=20)
    rundirectly=models.BooleanField()
    buildcommand=models.CharField(max_length=50)
    buildparameters=models.CharField(max_length=200)
    runcommand=models.CharField(max_length=50)
    beforeruncommands=models.CharField(max_length=200)

    def __unicode__(self):
        return self.name
            
class Problem(models.Model):
    user=models.ForeignKey(User)
    date = models.DateTimeField()
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    template = models.CharField(max_length=100)
    notes=models.IntegerField()
    links=models.IntegerField()
    ideas=models.IntegerField()
    todos=models.IntegerField()

    def __unicode__(self):
        return self.title

class Project(models.Model):
    title = models.CharField(max_length=200)
    framework = models.ForeignKey(Framework)
    problem=models.ForeignKey(Problem)
    runnable=models.BooleanField()
    public=models.BooleanField()
    user=models.ForeignKey(User)

    def __unicode__(self):
        return self.title
    
class InputFile(models.Model):
    template = models.CharField(max_length=200)
    problem=models.ForeignKey(Problem)
    
    def __unicode__(self):
        return self.template
    
class OutputFile(models.Model):
    fitness = models.IntegerField()
    template = models.CharField(max_length=200)
    inputfile=models.ForeignKey(InputFile)
    solved=models.BooleanField()
    framework=models.ForeignKey(Framework)
    
    def __unicode__(self):
        return self.template
    
class InputGeneratorFile(models.Model):
    user=models.ForeignKey(User)
    name = models.CharField(max_length=20)
    template = models.CharField(max_length=200)
    problem=models.ForeignKey(Problem)
    
    def __unicode__(self):
        return self.name

class SourceCodeFile(models.Model):
    name = models.CharField(max_length=20)
    template = models.CharField(max_length=200)
    project=models.ForeignKey(Project)
    
    def __unicode__(self):
        return self.name
    
class TimelineList(models.Model):
    show=models.BooleanField()
    user=models.ForeignKey(User)

    def __unicode__(self):
        return self.user.username
        
class Theme(models.Model):
    name=models.CharField(max_length=200)

    def __unicode__(self):
        return self.name
            
class ThemeList(models.Model):
    theme=models.ForeignKey(Theme)
    user=models.ForeignKey(User)

    def __unicode__(self):
        return self.user.username
    
class ChartThemeList(models.Model):
    charttheme=models.IntegerField()
    user=models.ForeignKey(User)

    def __unicode__(self):
        return self.user.username   
    
class ChartStyleList(models.Model):
    chartstyle=models.IntegerField()
    user=models.ForeignKey(User)

    def __unicode__(self):
        return self.user.username  
    
class PriorityList(models.Model):
    user=models.ForeignKey(User)
    priority=models.IntegerField()

class FrameworkList(models.Model):
    user=models.ForeignKey(User)
    framework=models.ForeignKey(Framework)
    active=models.BooleanField()

    def __unicode__(self):
        return self.framework.name

class Menu(models.Model):
    name=models.CharField(max_length=20)
    url = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

class MenuList(models.Model):
    framework=models.ForeignKey(Framework)
    menu=models.ForeignKey(Menu)

    def __unicode__(self):
        return self.framework.name+"-"+self.menu.name
            
class Statistic(models.Model):
    user=models.ForeignKey(User)
    tags=models.IntegerField()
    notes=models.IntegerField()
    links=models.IntegerField()
    ideas=models.IntegerField()
    todos=models.IntegerField()
    problems=models.IntegerField()
    projects=models.IntegerField()
    files=models.IntegerField()

    def __unicode__(self):
        return self.user.username
            
class Tag(models.Model):
    title = models.CharField(max_length=200)
    user=models.ForeignKey(User)
    date = models.DateTimeField()

    def __unicode__(self):
        return self.title

class Note(models.Model):
    title = models.CharField(max_length=200)
    problem=models.ForeignKey(Problem)	
    user=models.ForeignKey(User)
    date = models.DateTimeField()

    def __unicode__(self):
        return self.title

class TagList(models.Model):
    note=models.ForeignKey(Note)	
    tag=models.ForeignKey(Tag)

class Idea(models.Model):
    name = models.CharField(max_length=200)
    user=models.ForeignKey(User)
    text = models.CharField(max_length=1000)
    date = models.DateTimeField()

    def __unicode__(self):
        return self.name

class IdeaList(models.Model):
    note=models.ForeignKey(Note)
    idea=models.ForeignKey(Idea)
    
    def __unicode__(self):
        return self.note.id
    
class ProjectIdeaList(models.Model):
    project=models.ForeignKey(Project)
    idea=models.ForeignKey(Idea)
    
    def __unicode__(self):
        return self.project.id

class Link(models.Model):
    name = models.CharField(max_length=200)
    user=models.ForeignKey(User)
    text = models.CharField(max_length=1000)
    date = models.DateTimeField()

    def __unicode__(self):
        return self.name

class LinkList(models.Model):
    note=models.ForeignKey(Note)
    link=models.ForeignKey(Link)
    
    def __unicode__(self):
        return self.note.title
    
class ProjectLinkList(models.Model):
    project=models.ForeignKey(Project)
    link=models.ForeignKey(Link)
    
    def __unicode__(self):
        return self.project.id
    
class Todo(models.Model):
    name = models.CharField(max_length=200)
    user=models.ForeignKey(User)
    text = models.CharField(max_length=1000)
    date = models.DateTimeField()

    def __unicode__(self):
        return self.name

class TodoList(models.Model):
    note=models.ForeignKey(Note)
    todo=models.ForeignKey(Todo)
    
    def __unicode__(self):
        return self.note.id
    
class ProjectTodoList(models.Model):
    project=models.ForeignKey(Project)
    todo=models.ForeignKey(Todo)
    
    def __unicode__(self):
        return self.project.id

class ProblemTagList(models.Model):
    problem=models.ForeignKey(Problem)
    tag=models.ForeignKey(Tag)

    def __unicode__(self):
        return self.tag.title

