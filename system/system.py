#-*- coding: utf8 -*- 

from xml.dom.minidom import Document
import codecs
import os
from django.db import connection
from models import Problem,Framework,FrameworkList,Menu,MenuList,Theme,ProblemTagList,Tag,Note,Idea,Todo,Link,Project
from django.contrib.auth.models import User
from datetime import datetime

PROJECT_FOLDER="/ecoude_cooking/"

def parsedate(date):
    weekday = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][date.weekday()]
    month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"] [date.month - 1]
    return "%s %s %02d %04d %02d:%02d:%02d GMT" % (weekday, month, date.day,date.year, date.hour, date.minute,date.second)

def xmlrefresh_notes(problem_id):
    os.remove(PROJECT_FOLDER+"static/xml/problem."+str(problem_id)+".xml")

def xmlrefresh_projects(framework_id):
    os.remove(PROJECT_FOLDER+"static/xml/projects-"+str(framework_id)+".xml")

def xmlrefresh_note(note_id):
    os.remove(PROJECT_FOLDER+"static/xml/note."+str(note_id)+".xml")

def xmlrefresh_problems():
    os.remove(PROJECT_FOLDER+"static/xml/problems.xml")

def xmlrefresh_problemlists(problem_id):
    os.remove(PROJECT_FOLDER+"static/xml/problemnotes-"+str(problem_id)+".xml")

def xmlcheck_note(note_id):
    return not (os.path.exists(PROJECT_FOLDER+"static/xml/note."+str(note_id)+".xml"))

def xmlcheck_notes(problem_id):
    return not (os.path.exists(PROJECT_FOLDER+"static/xml/problem."+str(problem_id)+".xml"))

def xmlinit_notes(problem_id):
    doc=Document()
    wml = doc.createElement('data')
    doc.appendChild(wml)
    path=PROJECT_FOLDER+"static/xml/problem."+str(problem_id)+".xml"
    f=codecs.open(path,'w','utf-8')
    cursor = connection.cursor()
    cursor.execute("SELECT id,title,user_id,date FROM system_note WHERE problem_id=%s;", [problem_id] )
    private_notes = cursor.fetchall()
    for project in private_notes:
        event = doc.createElement('event')
        event.setAttribute('start', parsedate(project[3]))
        event.setAttribute('isDuration', 'false')
        event.setAttribute('title', str(project[1]))
        wml.appendChild(event)
    data=doc.toprettyxml(indent='  ')
    f.write(data)
    f.close()
        
def xmlinit_note(note_id):
    doc=Document()
    wml = doc.createElement('data')
    doc.appendChild(wml)
    path=PROJECT_FOLDER+"static/xml/note."+str(note_id)+".xml"
    f=codecs.open(path,'w','utf-8')
    cursor = connection.cursor()
    cursor.execute("SELECT todo.* FROM system_todolist list, system_todo todo WHERE list.note_id=%s AND todo.id=list.todo_id ORDER BY todo.id DESC;", [note_id] )
    private_todos = cursor.fetchall()
    for project in private_todos:
        event = doc.createElement('event')
        event.setAttribute('start', parsedate(project[4]))
        event.setAttribute('isDuration', 'false')
        event.setAttribute('title', str(project[1]))
        text = doc.createTextNode(str(project[3]))
        event.appendChild(text)
        wml.appendChild(event)
    cursor = connection.cursor()
    cursor.execute("SELECT idea.* FROM system_idealist list, system_idea idea WHERE list.note_id=%s AND idea.id=list.idea_id ORDER BY idea.id DESC;", [note_id] )
    private_ideas = cursor.fetchall()
    for project in private_ideas:
        event = doc.createElement('event')
        event.setAttribute('start', parsedate(project[4]))
        event.setAttribute('isDuration', 'false')
        event.setAttribute('title', str(project[1]))
        text = doc.createTextNode(str(project[3]))
        event.appendChild(text)
        wml.appendChild(event)
    cursor = connection.cursor()
    cursor.execute("SELECT link.* FROM system_linklist list, system_link link WHERE list.note_id=%s AND link.id=list.link_id ORDER BY link.id DESC;", [note_id] )
    private_links = cursor.fetchall()
    for project in private_links:
        event = doc.createElement('event')
        event.setAttribute('start', parsedate(project[4]))
        event.setAttribute('isDuration', 'false')
        event.setAttribute('title', str(project[1]))
        text = doc.createTextNode(str(project[3]))
        event.appendChild(text)
        wml.appendChild(event)
    data=doc.toprettyxml(indent='  ')
    f.write(data)
    f.close()

def anonymoususer():
    return User.objects.filter(username="AnonymousUser")[0]

def xmlcheck_problems():
    return not (os.path.exists(PROJECT_FOLDER+"static/xml/problems.xml"))

def xmlcheck_problemlists(event_id):
    return not (os.path.exists(PROJECT_FOLDER+"static/xml/problemnotes-"+str(event_id)+".xml"))

def xmlinit_problems():
    doc=Document()
    wml = doc.createElement('data')
    doc.appendChild(wml)
    f=codecs.open(PROJECT_FOLDER+"static/xml/problems.xml",'w','utf-8')
    cursor = connection.cursor()
    cursor.execute("SELECT id,user_id,date,description,title,template,notes,links,ideas,todos FROM system_problem;" )
    events = cursor.fetchall()
    for project in events:
        event = doc.createElement('event')
        event.setAttribute('start', parsedate(project[2]))
        event.setAttribute('isDuration', 'false')
        event.setAttribute('title', str(project[4]))
        text = doc.createTextNode(str(project[3]))
        event.appendChild(text)
        wml.appendChild(event)
    data=doc.toprettyxml(indent='  ')
    f.write(data)
    f.close()

def menu(id):
    menu=dict()
    cursor = connection.cursor()
    cursor.execute("SELECT framework.id,framework.name FROM system_framework framework,system_frameworklist l WHERE l.framework_id=framework.id AND l.user_id=%s AND l.active=TRUE;", [id] )
    #cursor.execute("SELECT framework.id,framework.name FROM system_framework framework,system_frameworklist l WHERE l.framework_id=framework.id AND l.user_id=%s AND l.active=1;", [id] )
    frameworks=cursor.fetchall()
    for id,name in frameworks:
	print(name)
        li=dict()
        #items=MenuList.objects.filter(framework__name=name)
        #menuitems=items.values_list("id",flat=True)
        #for menuitem in menuitems:
        #    li[Menu.objects.values_list("name",flat=True).get(id=menuitem)]=Menu.objects.values_list("url",flat=True).get(id=menuitem)
        #    menu[name]=li
            #`
	#cursor.execute("SELECT DISTINCT p.id, p.title FROM system_problem p,system_project j,system_framework f WHERE j.framework_id=f.id AND j.problem_id=p.id AND f.id=%s",[id])
        cursor = connection.cursor()
        cursor.execute("SELECT DISTINCT p.id, p.title FROM system_problem p,system_project j,system_framework f WHERE j.framework_id=f.id AND j.problem_id=p.id AND f.id=%s",[id])
        problems = cursor.fetchall()
        for problem_id,problem_name in problems:
	    print(problem_name)
            li[problem_name]="solutions/"+str(problem_id)+"/"+str(id)
            menu[name]=li
    return menu
    
def system(user):
    logged=(str(user)!="AnonymousUser")
    out=dict()
    system_dict=dict()
    if logged:
            out=menu(user.id)
            cursor = connection.cursor()
            cursor.execute("SELECT chartstyle FROM system_chartstylelist WHERE user_id=%s",[user.id])
            chartstyle = cursor.fetchone()[0]
            system_dict["chartstyle"]=chartstyle
            cursor = connection.cursor()
            cursor.execute("SELECT charttheme FROM system_chartthemelist WHERE user_id=%s",[user.id])
            charttheme = cursor.fetchone()[0]
            system_dict["charttheme"]=charttheme
            cursor = connection.cursor()	
	    cursor.execute("SELECT IF(`show`,'True','False') FROM system_timelinelist WHERE user_id=%s",[user.id])
	    #cursor.execute("SELECT REPLACE(REPLACE(show,'0','false'),'1','true') AS shows FROM system_timelinelist WHERE user_id=%s",[user.id])
            #cursor.execute("SELECT show AS IF(1,'True','False') FROM system_timelinelist WHERE user_id=%s",[user.id])
            timeline=cursor.fetchone()[0]
            system_dict["timeline"]=str(timeline)
	    #system_dict["timeline"]="True"
            cursor = connection.cursor()
            cursor.execute("SELECT priority FROM system_prioritylist WHERE user_id=%s",[user.id])
            priority = cursor.fetchone()[0]
            system_dict["priority"]=priority
    else:
            anonymous=anonymoususer()
            out=menu(anonymous.id)
    
    system_dict["logged"]=str(logged)
    system_dict["menu"]=out
    system_dict["user"]=str(user.username)
    cursor = connection.cursor()
    cursor.execute("SELECT t.name FROM system_theme t,system_themelist l WHERE l.user_id=%s AND l.theme_id=t.id;", [user.id])
    theme=None
    if user.id==None:
        theme="Blue"
    else:
        theme=cursor.fetchone()[0]

    system_dict["theme"]=theme
    
    favorites=FrameworkList.objects.filter(active=1,user=user.id)
    others=FrameworkList.objects.filter(active=0,user=user.id)
    system_dict["favorites"]=favorites
    system_dict["others"]=others
    
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM system_theme;")
    themes = cursor.fetchall()
    system_dict["themes"]=themes
    
    anonymous=User.objects.filter(username="AnonymousUser")[0]
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT tag.id,tag.title FROM system_problemtaglist list, system_tag tag WHERE list.tag_id=tag.id;")
    outtags = cursor.fetchall()
    system_dict["problemstag"]=outtags
    cursor = connection.cursor()
    return system_dict.items()

def activate(user_id,framework_id):
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM system_frameworklist WHERE framework_id=%s AND user_id=%s;",[framework_id,user_id])
    frameworklist_id=None
    try:
        frameworklist_id=cursor.fetchone()[0]
    except:
        frameworklist_id=add_frameworklist(user_id,framework_id,1)
    cursor = connection.cursor()
    cursor.execute("UPDATE system_frameworklist SET active=1 WHERE id=%s;",[frameworklist_id])
    return frameworklist_id

def deactivate(user_id,framework_id):
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM system_frameworklist WHERE framework_id=%s AND user_id=%s;",[framework_id,user_id])
    frameworklist_id=None
    try:
        frameworklist_id=cursor.fetchone()[0]
    except:
        frameworklist_id=add_frameworklist(user_id,framework_id,0)
    cursor = connection.cursor()
    cursor.execute("UPDATE system_frameworklist SET active=0 WHERE id=%s;",[frameworklist_id])
    return frameworklist_id
        
        
def statistic_inc_tags(user_id):
    cursor = connection.cursor()
    cursor.execute("SELECT tags FROM system_statistic WHERE user_id=%s;", [user_id])
    tags=cursor.fetchone()[0]+1
    cursor = connection.cursor()
    cursor.execute("UPDATE system_statistic SET tags=%s WHERE user_id=%s;", [tags,user_id])

def statistic_inc_notes(user_id):
    cursor = connection.cursor()
    cursor.execute("SELECT notes FROM system_statistic WHERE user_id=%s;", [user_id])
    notes=cursor.fetchone()[0]+1
    cursor = connection.cursor()
    cursor.execute("UPDATE system_statistic SET notes=%s WHERE user_id=%s;", [notes,user_id])
    
def statistic_inc_ideas(user_id):
    cursor = connection.cursor()
    cursor.execute("SELECT ideas FROM system_statistic WHERE user_id=%s;", [user_id])
    ideas=cursor.fetchone()[0]+1
    cursor = connection.cursor()
    cursor.execute("UPDATE system_statistic SET ideas=%s WHERE user_id=%s;", [ideas,user_id])
        
def statistic_inc_todos(user_id):
    cursor = connection.cursor()
    cursor.execute("SELECT todos FROM system_statistic WHERE user_id=%s;", [user_id])
    todos=cursor.fetchone()[0]+1
    cursor = connection.cursor()
    cursor.execute("UPDATE system_statistic SET todos=%s WHERE user_id=%s;", [todos,user_id])
    
def statistic_inc_links(user_id):
    cursor = connection.cursor()
    cursor.execute("SELECT links FROM system_statistic WHERE user_id=%s;", [user_id])
    links=cursor.fetchone()[0]+1
    cursor = connection.cursor()
    cursor.execute("UPDATE system_statistic SET links=%s WHERE user_id=%s;", [links,user_id])
 
def statistic_inc_problems(user_id):
    cursor = connection.cursor()
    cursor.execute("SELECT problems FROM system_statistic WHERE user_id=%s;", [user_id])
    problems=cursor.fetchone()[0]+1
    cursor = connection.cursor()
    cursor.execute("UPDATE system_statistic SET problems=%s WHERE user_id=%s;", [problems,user_id])
    
def statistic_dec_tags(user_id):
    cursor = connection.cursor()
    cursor.execute("SELECT tags FROM system_statistic WHERE user_id=%s;", [user_id])
    tags=cursor.fetchone()[0]-1
    cursor = connection.cursor()
    cursor.execute("UPDATE system_statistic SET tags=%s WHERE user_id=%s;", [tags,user_id])

def statistic_dec_notes(user_id):
    cursor = connection.cursor()
    cursor.execute("SELECT notes FROM system_statistic WHERE user_id=%s;", [user_id])
    notes=cursor.fetchone()[0]-1
    cursor = connection.cursor()
    cursor.execute("UPDATE system_statistic SET notes=%s WHERE user_id=%s;", [notes,user_id])
    
def statistic_dec_ideas(user_id):
    cursor = connection.cursor()
    cursor.execute("SELECT ideas FROM system_statistic WHERE user_id=%s;", [user_id])
    ideas=cursor.fetchone()[0]-1
    cursor = connection.cursor()
    cursor.execute("UPDATE system_statistic SET ideas=%s WHERE user_id=%s;", [ideas,user_id])
        
def statistic_dec_todos(user_id):
    cursor = connection.cursor()
    cursor.execute("SELECT todos FROM system_statistic WHERE user_id=%s;", [user_id])
    todos=cursor.fetchone()[0]-1
    cursor = connection.cursor()
    cursor.execute("UPDATE system_statistic SET todos=%s WHERE user_id=%s;", [todos,user_id])
    
def statistic_dec_links(user_id):
    cursor = connection.cursor()
    cursor.execute("SELECT links FROM system_statistic WHERE user_id=%s;", [user_id])
    links=cursor.fetchone()[0]-1
    cursor = connection.cursor()
    cursor.execute("UPDATE system_statistic SET links=%s WHERE user_id=%s;", [links,user_id])
 
def statistic_inc_projects(user_id):
    cursor = connection.cursor()
    cursor.execute("SELECT projects FROM system_statistic WHERE user_id=%s;", [user_id])
    projects=cursor.fetchone()[0]+1
    cursor = connection.cursor()
    cursor.execute("UPDATE system_statistic SET projects=%s WHERE user_id=%s;", [projects,user_id])

def statistic_inc_files(user_id):
    cursor = connection.cursor()
    cursor.execute("SELECT files FROM system_statistic WHERE user_id=%s;", [user_id])
    files=cursor.fetchone()[0]+1
    cursor = connection.cursor()
    cursor.execute("UPDATE system_statistic SET files=%s WHERE user_id=%s;", [files,user_id])

def system_id():
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM system_sequences;")
    return cursor.fetchone()[0]
    
def system_inc_frameworks():
    id=system_id()
    cursor = connection.cursor()
    cursor.execute("SELECT frameworks FROM system_sequences WHERE id=%s;",[id])
    new_count=cursor.fetchone()[0]+1
    cursor = connection.cursor()
    cursor.execute("UPDATE system_sequences SET frameworks=%s WHERE id=%s;", [new_count,id])
    return new_count
    
def system_inc_projects():
    id=system_id()
    cursor = connection.cursor()
    cursor.execute("SELECT projects FROM system_sequences WHERE id=%s;",[id])
    new_count=cursor.fetchone()[0]+1
    cursor = connection.cursor()
    cursor.execute("UPDATE system_sequences SET projects=%s WHERE id=%s;", [new_count,id])
    return new_count

def system_inc_sourcecodefiles():
    id=system_id()
    cursor = connection.cursor()
    cursor.execute("SELECT sourcecodefiles FROM system_sequences WHERE id=%s;",[id])
    new_count=cursor.fetchone()[0]+1
    cursor = connection.cursor()
    cursor.execute("UPDATE system_sequences SET sourcecodefiles=%s WHERE id=%s;", [new_count,id])
    return new_count

def system_inc_inputgeneratorfiles():
    id=system_id()
    cursor = connection.cursor()
    cursor.execute("SELECT inputgeneratorfiles FROM system_sequences WHERE id=%s;",[id])
    new_count=cursor.fetchone()[0]+1
    cursor = connection.cursor()
    cursor.execute("UPDATE system_sequences SET inputgeneratorfiles=%s WHERE id=%s;", [new_count,id])
    return new_count

def system_inc_inputfiles():
    id=system_id()
    cursor = connection.cursor()
    cursor.execute("SELECT inputfiles FROM system_sequences WHERE id=%s;",[id])
    new_count=cursor.fetchone()[0]+1
    cursor = connection.cursor()
    cursor.execute("UPDATE system_sequences SET inputfiles=%s WHERE id=%s;", [new_count,id])
    return new_count

def system_inc_outputfiles():
    id=system_id()
    cursor = connection.cursor()
    cursor.execute("SELECT outputfiles FROM system_sequences WHERE id=%s;",[id])
    new_count=cursor.fetchone()[0]+1
    cursor = connection.cursor()
    cursor.execute("UPDATE system_sequences SET outputfiles=%s WHERE id=%s;", [new_count,id])
    return new_count

    
def system_inc_menus():
    id=system_id()
    cursor = connection.cursor()
    cursor.execute("SELECT menus FROM system_sequences WHERE id=%s;",[id])
    new_count=cursor.fetchone()[0]+1
    cursor = connection.cursor()
    cursor.execute("UPDATE system_sequences SET menus=%s WHERE id=%s;", [new_count,id])
    return new_count
    
def system_inc_menulists():
    id=system_id()
    cursor = connection.cursor()
    cursor.execute("SELECT menulists FROM system_sequences WHERE id=%s;",[id])
    new_count=cursor.fetchone()[0]+1
    cursor = connection.cursor()
    cursor.execute("UPDATE system_sequences SET menulists=%s WHERE id=%s;", [new_count,id])
    return new_count
    
def system_inc_todos():
    id=system_id()
    cursor = connection.cursor()
    cursor.execute("SELECT todos FROM system_sequences WHERE id=%s;",[id])
    new_todo_id=cursor.fetchone()[0]+1
    cursor.execute("UPDATE system_sequences SET todos=%s WHERE id=%s;", [new_todo_id,id])
    return new_todo_id
    
def system_inc_ideas():
    id=system_id()
    cursor = connection.cursor()
    cursor.execute("SELECT todos FROM system_sequences WHERE id=%s;",[id])
    new_idea_id=cursor.fetchone()[0]+1
    cursor.execute("UPDATE system_sequences SET ideas=%s WHERE id=%s;", [new_idea_id,id])
    return new_idea_id
    
def system_inc_links():
    id=system_id()
    cursor = connection.cursor()
    cursor.execute("SELECT links FROM system_sequences WHERE id=%s;",[id])
    new_link_id=cursor.fetchone()[0]+1
    cursor.execute("UPDATE system_sequences SET links=%s WHERE id=%s;", [new_link_id,id])
    return new_link_id
    
def system_inc_tags():
    id=system_id()
    cursor = connection.cursor()
    cursor.execute("SELECT tags FROM system_sequences WHERE id=%s;",[id])
    new_tag_id=cursor.fetchone()[0]+1
    cursor = connection.cursor()
    cursor.execute("UPDATE system_sequences SET tags=%s WHERE id=%s;", [new_tag_id,id])
    return new_tag_id
    
def system_inc_problems():
    id=system_id()
    cursor = connection.cursor()
    cursor.execute("SELECT problems FROM system_sequences WHERE id=%s;",[id])
    new_id=cursor.fetchone()[0]+1
    cursor = connection.cursor()
    cursor.execute("UPDATE system_sequences SET problems=%s WHERE id=%s;", [new_id,id])
    return new_id
    
def system_inc_projects():
    id=system_id()
    cursor = connection.cursor()
    cursor.execute("SELECT projects FROM system_sequences WHERE id=%s;",[id])
    new_id=cursor.fetchone()[0]+1
    cursor = connection.cursor()
    cursor.execute("UPDATE system_sequences SET projects=%s WHERE id=%s;", [new_id,id])
    return new_id
    
def system_inc_problemtaglists():
    id=system_id()
    cursor = connection.cursor()
    cursor.execute("SELECT problemtaglists FROM system_sequences WHERE id=%s;",[id])
    new_id=cursor.fetchone()[0]+1
    cursor = connection.cursor()
    cursor.execute("UPDATE system_sequences SET problemtaglists=%s WHERE id=%s;", [new_id,id])
    return new_id
    
def system_inc_taglists():
    id=system_id()
    cursor = connection.cursor()
    cursor.execute("SELECT taglists FROM system_sequences WHERE id=%s;",[id])
    new_id=cursor.fetchone()[0]+1
    cursor = connection.cursor()
    cursor.execute("UPDATE system_sequences SET taglists=%s WHERE id=%s;", [new_id,id])
    return new_id
    
def system_inc_todolists():
    id=system_id()
    cursor = connection.cursor()
    cursor.execute("SELECT todolists FROM system_sequences WHERE id=%s;",[id])
    new_id=cursor.fetchone()[0]+1
    cursor = connection.cursor()
    cursor.execute("UPDATE system_sequences SET todolists=%s WHERE id=%s;", [new_id,id])
    return new_id
    
def system_inc_idealists():
    id=system_id()
    cursor = connection.cursor()
    cursor.execute("SELECT idealists FROM system_sequences WHERE id=%s;",[id])
    new_id=cursor.fetchone()[0]+1
    cursor = connection.cursor()
    cursor.execute("UPDATE system_sequences SET idealists=%s WHERE id=%s;", [new_id,str(id)])
    return new_id
    
def system_inc_linklists():
    id=system_id()
    cursor = connection.cursor()
    cursor.execute("SELECT linklists FROM system_sequences WHERE id=%s;",[id])
    new_id=cursor.fetchone()[0]+1
    cursor = connection.cursor()
    cursor.execute("UPDATE system_sequences SET linklists=%s WHERE id=%s;", [new_id,str(id)])
    return new_id

def system_inc_projecttodolists():
    id=system_id()
    cursor = connection.cursor()
    cursor.execute("SELECT projecttodolists FROM system_sequences WHERE id=%s;",[id])
    new_id=cursor.fetchone()[0]+1
    cursor = connection.cursor()
    cursor.execute("UPDATE system_sequences SET projecttodolists=%s WHERE id=%s;", [new_id,id])
    return new_id
    
def system_inc_projectidealists():
    id=system_id()
    cursor = connection.cursor()
    cursor.execute("SELECT projectidealists FROM system_sequences WHERE id=%s;",[id])
    new_id=cursor.fetchone()[0]+1
    cursor = connection.cursor()
    cursor.execute("UPDATE system_sequences SET projectidealists=%s WHERE id=%s;", [new_id,str(id)])
    return new_id
    
def system_inc_projectlinklists():
    id=system_id()
    cursor = connection.cursor()
    cursor.execute("SELECT projectlinklists FROM system_sequences WHERE id=%s;",[id])
    new_id=cursor.fetchone()[0]+1
    cursor = connection.cursor()
    cursor.execute("UPDATE system_sequences SET projectlinklists=%s WHERE id=%s;", [new_id,str(id)])
    return new_id
    
def system_inc_notes():
    id=system_id()
    cursor = connection.cursor()
    cursor.execute("SELECT notes FROM system_sequences WHERE id=%s;",[id])
    new_id=cursor.fetchone()[0]+1
    cursor = connection.cursor()
    cursor.execute("UPDATE system_sequences SET notes=%s WHERE id=%s;", [new_id,str(id)])
    return new_id

def problem_inc_notes(problem_id):
    cursor = connection.cursor()
    cursor.execute("SELECT notes FROM system_problem WHERE id=%s;", [problem_id])
    notes=cursor.fetchone()[0]+1
    cursor = connection.cursor()
    cursor.execute("UPDATE system_problem SET notes=%s WHERE id=%s;", [notes,problem_id])

def problem_inc_ideas(user_id,problem_id):
    statistic_inc_ideas(user_id)
    cursor = connection.cursor()
    cursor.execute("SELECT ideas FROM system_problem WHERE id=%s;", [problem_id])
    ideas=cursor.fetchone()[0]+1
    cursor = connection.cursor()
    cursor.execute("UPDATE system_problem SET ideas=%s WHERE id=%s;", [ideas,problem_id])

def problem_inc_todos(user_id,problem_id):
    statistic_inc_todos(user_id)
    cursor = connection.cursor()
    cursor.execute("SELECT todos FROM system_problem WHERE id=%s;", [problem_id])
    todos=cursor.fetchone()[0]+1
    cursor = connection.cursor()
    cursor.execute("UPDATE system_problem SET todos=%s WHERE id=%s;", [todos,problem_id])

def problem_inc_links(user_id,problem_id):
    statistic_inc_links(user_id)
    id=system_id()
    cursor = connection.cursor()
    cursor.execute("SELECT links FROM system_problem WHERE id=%s;", [problem_id])
    links=cursor.fetchone()[0]+1
    cursor = connection.cursor()
    cursor.execute("UPDATE system_problem SET links=%s WHERE id=%s;", [links,problem_id])
    
def system_dec_frameworks():
    id=system_id()
    cursor = connection.cursor()
    cursor.execute("SELECT frameworks FROM system_sequences WHERE id=%s;",[id])
    new_count=cursor.fetchone()[0]-1
    cursor = connection.cursor()
    cursor.execute("UPDATE system_sequences SET frameworks=%s WHERE id=%s;", [new_count,id])
    return new_count
    
def system_dec_menus():
    id=system_id()
    cursor = connection.cursor()
    cursor.execute("SELECT menus FROM system_sequences WHERE id=%s;",[id])
    new_count=cursor.fetchone()[0]-1
    cursor = connection.cursor()
    cursor.execute("UPDATE system_sequences SET menus=%s WHERE id=%s;", [new_count,id])
    return new_count
    
def system_dec_menulists():
    id=system_id()
    cursor = connection.cursor()
    cursor.execute("SELECT menulists FROM system_sequences WHERE id=%s;",[id])
    new_count=cursor.fetchone()[0]-1
    cursor = connection.cursor()
    cursor.execute("UPDATE system_sequences SET menulists=%s WHERE id=%s;", [new_count,id])
    return new_count
    
def system_dec_todos():
    id=system_id()
    cursor = connection.cursor()
    cursor.execute("SELECT todos FROM system_sequences WHERE id=%s;",[id])
    new_todo_id=cursor.fetchone()[0]-1
    cursor.execute("UPDATE system_sequences SET todos=%s WHERE id=%s;", [new_todo_id,id])
    return new_todo_id
    
def system_dec_ideas():
    id=system_id()
    cursor = connection.cursor()
    cursor.execute("SELECT todos FROM system_sequences WHERE id=%s;",[id])
    new_idea_id=cursor.fetchone()[0]+1
    cursor.execute("UPDATE system_sequences SET ideas=%s WHERE id=%s;", [new_idea_id,id])
    return new_idea_id
    
def system_dec_links():
    id=system_id()
    cursor = connection.cursor()
    cursor.execute("SELECT links FROM system_sequences WHERE id=%s;",[id])
    new_link_id=cursor.fetchone()[0]+1
    cursor.execute("UPDATE system_sequences SET links=%s WHERE id=%s;", [new_link_id,id])
    return new_link_id
    
def system_dec_tags():
    id=system_id()
    cursor = connection.cursor()
    cursor.execute("SELECT tags FROM system_sequences WHERE id=%s;",[id])
    new_tag_id=cursor.fetchone()[0]-1
    cursor = connection.cursor()
    cursor.execute("UPDATE system_sequences SET tags=%s WHERE id=%s;", [new_tag_id,id])
    return new_tag_id
    
def system_dec_problems():
    id=system_id()
    cursor = connection.cursor()
    cursor.execute("SELECT problems FROM system_sequences WHERE id=%s;",[id])
    new_id=cursor.fetchone()[0]-1
    cursor = connection.cursor()
    cursor.execute("UPDATE system_sequences SET problems=%s WHERE id=%s;", [new_id,id])
    
def system_dec_projects():
    id=system_id()
    cursor = connection.cursor()
    cursor.execute("SELECT projects FROM system_sequences WHERE id=%s;",[id])
    new_id=cursor.fetchone()[0]-1
    cursor = connection.cursor()
    cursor.execute("UPDATE system_sequences SET projects=%s WHERE id=%s;", [new_id,id])
    return new_id
    
def system_dec_problemtaglists():
    id=system_id()
    cursor = connection.cursor()
    cursor.execute("SELECT problemtaglists FROM system_sequences WHERE id=%s;",[id])
    new_id=cursor.fetchone()[0]-1
    cursor = connection.cursor()
    cursor.execute("UPDATE system_sequences SET problemtaglists=%s WHERE id=%s;", [new_id,id])
    return new_id
    
def system_dec_taglists():
    id=system_id()
    cursor = connection.cursor()
    cursor.execute("SELECT taglists FROM system_sequences WHERE id=%s;",[id])
    new_id=cursor.fetchone()[0]+1
    cursor = connection.cursor()
    cursor.execute("UPDATE system_sequences SET taglists=%s WHERE id=%s;", [new_id,id])
    return new_id
    
def system_dec_todolists():
    id=system_id()
    cursor = connection.cursor()
    cursor.execute("SELECT todolists FROM system_sequences WHERE id=%s;",[id])
    new_id=cursor.fetchone()[0]-1
    cursor = connection.cursor()
    cursor.execute("UPDATE system_sequences SET todolists=%s WHERE id=%s;", [new_id,id])
    return new_id
    
def system_dec_idealists():
    id=system_id()
    cursor = connection.cursor()
    cursor.execute("SELECT idealists FROM system_sequences WHERE id=%s;",[id])
    new_id=cursor.fetchone()[0]-1
    cursor = connection.cursor()
    cursor.execute("UPDATE system_sequences SET idealists=%s WHERE id=%s;", [new_id,str(id)])
    return new_id
    
def system_dec_linklists():
    id=system_id()
    cursor = connection.cursor()
    cursor.execute("SELECT linklists FROM system_sequences WHERE id=%s;",[id])
    new_id=cursor.fetchone()[0]-1
    cursor = connection.cursor()
    cursor.execute("UPDATE system_sequences SET linklists=%s WHERE id=%s;", [new_id,str(id)])
    return new_id
    
def system_dec_notes():
    id=system_id()
    cursor = connection.cursor()
    cursor.execute("SELECT notes FROM system_sequences WHERE id=%s;",[id])
    new_id=cursor.fetchone()[0]-1
    cursor = connection.cursor()
    cursor.execute("UPDATE system_sequences SET notes=%s WHERE id=%s;", [new_id,str(id)])
    return new_id

def system_dec_sourcecodefiles():
    id=system_id()
    cursor = connection.cursor()
    cursor.execute("SELECT sourcecodefiles FROM system_sequences WHERE id=%s;",[id])
    new_count=cursor.fetchone()[0]-1
    cursor = connection.cursor()
    cursor.execute("UPDATE system_sequences SET sourcecodefiles=%s WHERE id=%s;", [new_count,id])
    return new_count

def system_dec_inputgeneratorfiles():
    id=system_id()
    cursor = connection.cursor()
    cursor.execute("SELECT inputgeneratorfiles FROM system_sequences WHERE id=%s;",[id])
    new_count=cursor.fetchone()[0]-1
    cursor = connection.cursor()
    cursor.execute("UPDATE system_sequences SET inputgeneratorfiles=%s WHERE id=%s;", [new_count,id])
    return new_count

def system_dec_inputfiles():
    id=system_id()
    cursor = connection.cursor()
    cursor.execute("SELECT inputfiles FROM system_sequences WHERE id=%s;",[id])
    new_count=cursor.fetchone()[0]-1
    cursor = connection.cursor()
    cursor.execute("UPDATE system_sequences SET inputfiles=%s WHERE id=%s;", [new_count,id])
    return new_count

def system_dec_outputfiles():
    id=system_id()
    cursor = connection.cursor()
    cursor.execute("SELECT outputfiles FROM system_sequences WHERE id=%s;",[id])
    new_count=cursor.fetchone()[0]-1
    cursor = connection.cursor()
    cursor.execute("UPDATE system_sequences SET outputfiles=%s WHERE id=%s;", [new_count,id])
    return new_count

def problem_dec_notes(problem_id):
    cursor = connection.cursor()
    cursor.execute("SELECT notes FROM system_problem WHERE id=%s;", [problem_id])
    notes=cursor.fetchone()[0]-1
    cursor = connection.cursor()
    cursor.execute("UPDATE system_problem SET notes=%s WHERE id=%s;", [notes,problem_id])

def problem_dec_ideas(user_id,problem_id):
    statistic_inc_ideas(user_id)
    cursor = connection.cursor()
    cursor.execute("SELECT ideas FROM system_problem WHERE id=%s;", [problem_id])
    ideas=cursor.fetchone()[0]-1
    cursor = connection.cursor()
    cursor.execute("UPDATE system_problem SET ideas=%s WHERE id=%s;", [ideas,problem_id])

def problem_dec_todos(user_id,problem_id):
    statistic_inc_todos(user_id)
    cursor = connection.cursor()
    cursor.execute("SELECT todos FROM system_problem WHERE id=%s;", [problem_id])
    todos=cursor.fetchone()[0]-1
    cursor = connection.cursor()
    cursor.execute("UPDATE system_problem SET todos=%s WHERE id=%s;", [todos,problem_id])

def problem_dec_links(user_id,problem_id):
    statistic_inc_links(user_id)
    id=system_id()
    cursor = connection.cursor()
    cursor.execute("SELECT links FROM system_problem WHERE id=%s;", [problem_id])
    links=cursor.fetchone()[0]-1
    cursor = connection.cursor()
    cursor.execute("UPDATE system_problem SET links=%s WHERE id=%s;", [links,problem_id])

def system_dec_projects():
    id=system_id()
    cursor = connection.cursor()
    cursor.execute("SELECT projects FROM system_sequences WHERE id=%s;",[id])
    new_count=cursor.fetchone()[0]+1
    cursor = connection.cursor()
    cursor.execute("UPDATE system_sequences SET projects=%s WHERE id=%s;", [new_count,id])
    return new_count

def system_dec_files():
    id=system_id()
    cursor = connection.cursor()
    cursor.execute("SELECT files FROM system_sequences WHERE id=%s;",[id])
    new_count=cursor.fetchone()[0]+1
    cursor = connection.cursor()
    cursor.execute("UPDATE system_sequences SET files=%s WHERE id=%s;", [new_count,id])
    return new_count

def statistic_dec_projects(user_id):
    cursor = connection.cursor()
    cursor.execute("SELECT projects FROM system_statistic WHERE user_id=%s;", [user_id])
    projects=cursor.fetchone()[0]-1
    cursor = connection.cursor()
    cursor.execute("UPDATE system_statistic SET projects=%s WHERE user_id=%s;", [projects,user_id])

def statistic_dec_files(user_id):
    cursor = connection.cursor()
    cursor.execute("SELECT files FROM system_statistic WHERE user_id=%s;", [user_id])
    files=cursor.fetchone()[0]-1
    cursor = connection.cursor()
    cursor.execute("UPDATE system_statistic SET files=%s WHERE user_id=%s;", [files,user_id])
    
def system_dec_projecttodolists():
    id=system_id()
    cursor = connection.cursor()
    cursor.execute("SELECT projecttodolists FROM system_sequences WHERE id=%s;",[id])
    new_id=cursor.fetchone()[0]-1
    cursor = connection.cursor()
    cursor.execute("UPDATE system_sequences SET projecttodolists=%s WHERE id=%s;", [new_id,id])
    return new_id
    
def system_dec_projectidealists():
    id=system_id()
    cursor = connection.cursor()
    cursor.execute("SELECT projectidealists FROM system_sequences WHERE id=%s;",[id])
    new_id=cursor.fetchone()[0]-1
    cursor = connection.cursor()
    cursor.execute("UPDATE system_sequences SET projectidealists=%s WHERE id=%s;", [new_id,str(id)])
    return new_id
    
def system_dec_projectlinklists():
    id=system_id()
    cursor = connection.cursor()
    cursor.execute("SELECT projectlinklists FROM system_sequences WHERE id=%s;",[id])
    new_id=cursor.fetchone()[0]-1
    cursor = connection.cursor()
    cursor.execute("UPDATE system_sequences SET projectlinklists=%s WHERE id=%s;", [new_id,str(id)])
    return new_id

def tagid(id,title):
    results = Tag.objects.filter(title = title)
    print(":(")
    if results.count()==0:
        new_id=system_inc_tags()
        print(new_id)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO system_tag(id,user_id,date,title) VALUES(%s,%s,%s,%s);", [new_id, id, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), title])
        print("@")
        return new_id
    else:
        return results[0].id
    
def problemtaglists_id(problem_id, new_id_tag):
    results = ProblemTagList.objects.filter(tag = new_id_tag)
    if results.count()==0:
        new_id_problemtaglist=system_inc_problemtaglists()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO system_problemtaglist(id,problem_id,tag_id) VALUES(%s,%s,%s);", [new_id_problemtaglist, problem_id, new_id_tag ])
        return new_id_problemtaglist
    else:
        return results[0].id

def add_tag_to_note(user_id,title,note_id):
    statistic_inc_tags(user_id)
    i=tagid(user_id,title)
    new_id=system_inc_taglists()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO system_taglist(id,note_id,tag_id) VALUES(%s,%s,%s);", [new_id, note_id, i])

def add_tag_to_problem(user_id,title,problem_id):
    statistic_inc_tags(user_id)
    i=tagid(user_id,title)
    new_id=system_inc_problemtaglists()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO system_problemtaglist(id,problem_id,tag_id) VALUES(%s,%s,%s);", [new_id, problem_id, i])

def add_link_to_note(user_id,name,text,note_id):
    statistic_inc_links(user_id)
    new_id=system_inc_links()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO system_link(id,user_id,name,text,date) VALUES(%s,%s,%s,%s,%s);", [new_id, user_id,name,text,datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
    id=system_inc_linklists()
    cursor.execute("INSERT INTO system_linklist(id,note_id,link_id) VALUES(%s,%s,%s);", [id, note_id, new_id])
    
def add_idea_to_note(user_id,name,text,note_id):
    statistic_inc_ideas(user_id)
    new_id=system_inc_ideas()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO system_idea(id,user_id,name,text,date) VALUES(%s,%s,%s,%s,%s);", [new_id, user_id, str(name),str(text),datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
    id=system_inc_idealists()
    cursor.execute("INSERT INTO system_idealist(id,note_id,idea_id) VALUES(%s,%s,%s);", [id, note_id, new_id])
    
def add_todo_to_note(user_id,name,text,note_id):
    statistic_inc_todos(user_id)
    new_id=system_inc_todos()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO system_todo(id,user_id,name,text,date) VALUES(%s,%s,%s,%s,%s);", [new_id, user_id, str(name),str(text),datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
    id=system_inc_todolists()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO system_todolist(id,note_id,todo_id) VALUES(%s,%s,%s);", [id, note_id, new_id])

def add_link_to_project(user_id,name,text,project_id):
    statistic_inc_links(user_id)
    new_id=system_inc_links()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO system_link(id,user_id,name,text,date) VALUES(%s,%s,%s,%s,%s);", [new_id, user_id,name,text,datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
    id=system_inc_projectlinklists()
    cursor.execute("INSERT INTO system_projectlinklist(id,project_id,link_id) VALUES(%s,%s,%s);", [id, project_id, new_id])
    
def add_idea_to_project(user_id,name,text,project_id):
    statistic_inc_ideas(user_id)
    new_id=system_inc_ideas()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO system_idea(id,user_id,name,text,date) VALUES(%s,%s,%s,%s,%s);", [new_id, user_id, str(name),str(text),datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
    id=system_inc_projectidealists()
    cursor.execute("INSERT INTO system_projectidealist(id,project_id,idea_id) VALUES(%s,%s,%s);", [id, project_id, new_id])
    
def add_todo_to_project(user_id,name,text,project_id):
    statistic_inc_todos(user_id)
    new_id=system_inc_todos()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO system_todo(id,user_id,name,text,date) VALUES(%s,%s,%s,%s,%s);", [new_id, user_id, str(name),str(text),datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
    id=system_inc_projecttodolists()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO system_projecttodolist(id,project_id,todo_id) VALUES(%s,%s,%s);", [id, project_id, new_id])
    
def delete_todo_from_note(user,id,note_id):
    statistic_dec_todos(user)
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM system_todolist WHERE todo_id=%s AND note_id=%s",[id,note_id])
    todolist=cursor.fetchone()[0]
    cursor = connection.cursor()
    cursor.execute("DELETE FROM system_todo WHERE id=%s;", [id])
    cursor.execute("DELETE FROM system_todolist WHERE id=%s;", [todolist])
    system_dec_todos()
    system_dec_todolists()
    
def delete_idea_from_note(user,id,note_id):
    statistic_dec_ideas(user)
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM system_idealist WHERE idea_id=%s AND note_id=%s",[id,note_id])
    idealist=cursor.fetchone()[0]
    cursor = connection.cursor()
    cursor.execute("DELETE FROM system_idea WHERE id=%s;", [id])
    cursor.execute("DELETE FROM system_idealist WHERE id=%s;", [idealist])
    system_dec_ideas()
    system_dec_idealists()
    
def delete_link_from_note(user,id,note_id):
    statistic_dec_links(user)
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM system_linklist WHERE link_id=%s AND note_id=%s",[id,note_id])
    linklist=cursor.fetchone()[0]
    cursor = connection.cursor()
    cursor.execute("DELETE FROM system_link WHERE id=%s;", [id])
    cursor.execute("DELETE FROM system_linklist WHERE id=%s;", [linklist])
    system_dec_links()
    system_dec_linklists()

def delete_todo_from_project(user,id,project_id):
    statistic_dec_todos(user)
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM system_projecttodolist WHERE todo_id=%s AND project_id=%s",[id,project_id])
    projecttodolist=cursor.fetchone()[0]
    cursor = connection.cursor()
    cursor.execute("DELETE FROM system_todo WHERE id=%s;", [id])
    cursor.execute("DELETE FROM system_projecttodolist WHERE id=%s;", [projecttodolist])
    system_dec_todos()
    system_dec_projecttodolists()
    
def delete_idea_from_project(user,id,project_id):
    statistic_dec_ideas(user)
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM system_projectidealist WHERE idea_id=%s AND project_id=%s",[id,project_id])
    projectidealist=cursor.fetchone()[0]
    cursor = connection.cursor()
    cursor.execute("DELETE FROM system_idea WHERE id=%s;", [id])
    cursor.execute("DELETE FROM system_projectidealist WHERE id=%s;", [projectidealist])
    system_dec_ideas()
    system_dec_projectidealists()
    
def delete_link_from_project(user,id,project_id):
    statistic_dec_links(user)
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM system_projectlinklist WHERE link_id=%s AND project_id=%s",[id,project_id])
    projectlinklist=cursor.fetchone()[0]
    cursor = connection.cursor()
    cursor.execute("DELETE FROM system_link WHERE id=%s;", [id])
    cursor.execute("DELETE FROM system_projectlinklist WHERE id=%s;", [projectlinklist])
    system_dec_links()
    system_dec_projectlinklists()
