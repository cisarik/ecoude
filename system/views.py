#-*- coding: utf8 -*- 

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from models import Problem,Framework,FrameworkList,Menu,MenuList,Theme,ProblemTagList,Tag,Note,Idea,Todo,Link,Project
from forms import NoteForm,TagForm,RegistrationForm, NoteForm, TodoForm, IdeaForm, LinkForm, TagForm
from django.contrib.auth.models import User
from django.db import connection, transaction
from datetime import datetime
from system import *
import os
    
@login_required
@transaction.commit_manually
def note(request,note_id):
    edit=False
    editableedit=False
    newform=None
    newformheader=""
    editid=None
    edittype=None
    cursor = connection.cursor()
    cursor.execute("SELECT problem_id FROM system_note WHERE id=%s;", [note_id])
    problem_id=cursor.fetchone()[0]
    
    if xmlcheck_note(note_id):
        xmlinit_note(note_id)
        
    if request.GET.get('editdelete')=='true':
        if request.GET.get('edittype')=='todo':
            id=request.GET.get('editid')
            delete_todo_from_note(request.user.id,id,note_id)
            transaction.commit()
            xmlrefresh_note(note_id)
            return HttpResponseRedirect('/note/'+str(note_id))
        if request.GET.get('edittype')=='idea':
            id=request.GET.get('editid')
            delete_idea_from_note(request.user.id,id,note_id)
            transaction.commit()
            xmlrefresh_note(note_id)
            return HttpResponseRedirect('/note/'+str(note_id))
        if request.GET.get('edittype')=='link':
            id=request.GET.get('editid')
            delete_link_from_note(request.user.id,id,note_id)
            transaction.commit()
            xmlrefresh_note(note_id)
            return HttpResponseRedirect('/note/'+str(note_id))
        
    if request.GET.get('edit')=='true':
        edit=True
        if request.GET.get('todo')=='true':
            todo=Todo.objects.get(id=request.GET.get('id'))
            editid=todo.id
            newformheader="Todo"
            newform=TodoForm({'name':todo.name,'text':todo.text})
            editableedit=(todo.user.id==request.user.id)
            edittype="todo"
        if request.GET.get('idea')=='true':
            newformheader="Idea"
            idea=Idea.objects.get(id=request.GET.get('id'))
            editid=idea.id
            newform=IdeaForm({'name':idea.name,'text':idea.text})
            editableedit=(idea.user.id==request.user.id)
            edittype="idea"
        if request.GET.get('link')=='true':
            newformheader="Link"
            link=Link.objects.get(id=request.GET.get('id'))
            editid=link.id
            newform=LinkForm({'name':link.name,'text':link.text})
            editableedit=(link.user.id==request.user.id)
            edittype="link"
            
    if request.GET.get('delete')=='true':
        cursor = connection.cursor()
        cursor.execute("SELECT problem_id FROM system_note WHERE id=%s;", [note_id])
        problem_id=cursor.fetchone()[0]
        cursor = connection.cursor()
        cursor.execute("DELETE FROM system_note WHERE id=%s;", [note_id])
        transaction.commit()
        xmlrefresh_note(note_id)
        return HttpResponseRedirect('/problem/'+str(problem_id))
    
    if request.method == 'POST':
        try:
            if request.POST['edit']=='Idea':
                cursor = connection.cursor()
                cursor.execute("UPDATE system_idea SET name=%s,text=%s WHERE id=%s;",[request.POST['name'],request.POST['text'],request.POST['editid']])
                transaction.commit()
                xmlrefresh_note(note_id)
                return HttpResponseRedirect('/note/'+str(note_id))
        except:
            pass
        try:
            if request.POST['edit']=='Link':
                cursor = connection.cursor()
                print("deeeeee")
                cursor.execute("UPDATE system_link SET name=%s,text=%s WHERE id=%s;",[request.POST['name'],request.POST['text'],request.POST['editid']])
                transaction.commit()
                xmlrefresh_note(note_id)
                return HttpResponseRedirect('/note/'+str(note_id))
        except:
            pass
        try:
            if request.POST['edit']=='Todo':
                cursor = connection.cursor()
                cursor.execute("UPDATE system_todo SET name=%s,text=%s WHERE id=%s;",[request.POST['name'],request.POST['text'],request.POST['editid']])
                transaction.commit()
                xmlrefresh_note(note_id)
                return HttpResponseRedirect('/note/'+str(note_id))
        except:
            pass
        try:
            if request.POST['type']=='Link':
                add_link_to_note(request.user.id,request.POST['name'],request.POST['text'],note_id)
                problem_inc_links(request.user.id,problem_id)
                transaction.commit()
        except:
            pass
        try:
            if request.POST['type']=='Idea':
                add_idea_to_note(request.user.id,request.POST['name'],request.POST['text'],note_id)
                problem_inc_ideas(request.user.id,problem_id)
                transaction.commit()
        except:
            pass
        try:
            if request.POST['type']=='Tag':
                add_tag_to_note(request.user.id,request.POST['title'],note_id)
                transaction.commit()
        except:
            pass
        try:
            if request.POST['type']=='Todo':
                add_todo_to_note(request.user.id,request.POST['name'],request.POST['text'],note_id)
                problem_inc_todos(request.user.id,problem_id)
                transaction.commit()
        except:
            transaction.rollback()
        xmlrefresh_note(note_id)
        return HttpResponseRedirect('/note/'+str(note_id))
    else:
        form = TodoForm()
        form2 = IdeaForm()
        form3 = LinkForm()
        form4 = TagForm()
        note=Note.objects.get(id=note_id)
        form5=NoteForm({'title':note.title})
        cursor = connection.cursor()
        message = request.GET.get('sort')
        if message=='iddesc':
            cursor.execute("SELECT todo.* FROM system_todolist list, system_todo todo WHERE list.note_id=%s AND todo.id=list.todo_id ORDER BY todo.id DESC;", [note_id] )
        elif message=='idasc':
            cursor.execute("SELECT todo.* FROM system_todolist list, system_todo todo WHERE list.note_id=%s AND todo.id=list.todo_id ORDER BY todo.id ASC;", [note_id] )
        elif message=='titleasc':
            cursor.execute("SELECT todo.* FROM system_todolist list, system_todo todo WHERE list.note_id=%s AND todo.id=list.todo_id ORDER BY todo.name ASC;", [note_id] )
        elif message=='titledesc':
            cursor.execute("SELECT todo.* FROM system_todolist list, system_todo todo WHERE list.note_id=%s AND todo.id=list.todo_id ORDER BY todo.name DESC;", [note_id] )
        else:
            cursor.execute("SELECT todo.* FROM system_todolist list, system_todo todo WHERE list.note_id=%s AND todo.id=list.todo_id ORDER BY todo.id DESC;", [note_id] )
        private_todos = cursor.fetchall()
        cursor = connection.cursor()
        message = request.GET.get('sort2')
        if message=='iddesc':
            cursor.execute("SELECT idea.* FROM system_idealist list, system_idea idea WHERE list.note_id=%s AND idea.id=list.idea_id ORDER BY idea.id DESC;", [note_id] )
        elif message=='idasc':
            cursor.execute("SELECT idea.* FROM system_idealist list, system_idea idea WHERE list.note_id=%s AND idea.id=list.idea_id ORDER BY idea.id ASC;", [note_id] )
        elif message=='titleasc':
            cursor.execute("SELECT idea.* FROM system_idealist list, system_idea idea WHERE list.note_id=%s AND idea.id=list.idea_id ORDER BY idea.name ASC;", [note_id] )
        elif message=='titledesc':
            cursor.execute("SELECT idea.* FROM system_idealist list, system_idea idea WHERE list.note_id=%s AND idea.id=list.idea_id ORDER BY idea.name DESC;", [note_id] )
        else:
            cursor.execute("SELECT idea.* FROM system_idealist list, system_idea idea WHERE list.note_id=%s AND idea.id=list.idea_id ORDER BY idea.id DESC;", [note_id] )
        private_ideas = cursor.fetchall()
        cursor = connection.cursor()
        message = request.GET.get('sort2')
        if message=='iddesc':
            cursor.execute("SELECT link.* FROM system_linklist list, system_link link WHERE list.note_id=%s AND link.id=list.link_id ORDER BY link.id DESC;", [note_id] )
        elif message=='idasc':
            cursor.execute("SELECT link.* FROM system_linklist list, system_link link WHERE list.note_id=%s AND link.id=list.link_id ORDER BY link.id ASC;", [note_id] )
        elif message=='titleasc':
            cursor.execute("SELECT link.* FROM system_linklist list, system_link link WHERE list.note_id=%s AND link.id=list.link_id ORDER BY link.name ASC;", [note_id] )
        elif message=='titledesc':
            cursor.execute("SELECT link.* FROM system_linklist list, system_link link WHERE list.note_id=%s AND link.id=list.link_id ORDER BY link.name DESC;", [note_id] )
        else:
            cursor.execute("SELECT link.* FROM system_linklist list, system_link link WHERE list.note_id=%s AND link.id=list.link_id ORDER BY link.id DESC;", [note_id] )
        private_links = cursor.fetchall()
        cursor = connection.cursor()
        cursor.execute("SELECT tag.id,tag.title FROM system_taglist list, system_tag tag WHERE tag.user_id=%s AND list.note_id=%s AND tag.id=list.tag_id ORDER BY tag.title ASC;", [request.user.id,note_id] )
        private_tags = cursor.fetchall()
        cursor = connection.cursor()
        cursor.execute("SELECT title FROM system_note WHERE id=%s;", [note_id])
        tmp=cursor.fetchone()[0]
        
        cursor = connection.cursor()
        cursor.execute("SELECT title FROM system_problem WHERE id=%s;", [problem_id])
        problem=cursor.fetchone()[0]
        
        totemplate={'problem':problem,'edit':str(edit),'editid':editid,'formheader':newformheader,'editform':newform,'problem_id':problem_id,'note_problem':problem,"note_title":tmp,'tags':private_tags,'todos':private_todos,'ideas':private_ideas,'links':private_links,
        'form': form,'form2': form2,'form3': form3,'form4': form4,'form5': form5,'id':note_id,'editableedit':str(editableedit),'edittype':edittype}
        totemplate.update(system(request.user))
        return render_to_response('system/note.html', totemplate)

@login_required
@transaction.commit_manually
def notes(request,problem_id):
    if xmlcheck_notes(problem_id):
        xmlinit_notes(problem_id)
    if request.GET.get('edit')=='true':
        cursor = connection.cursor()
        cursor.execute("SELECT id,title,description,template FROM system_problem WHERE id=%s;", [problem_id] )
        problems = cursor.fetchall()
        cursor = connection.cursor()
        cursor.execute("SELECT t.title FROM system_problemtaglist l , system_tag t WHERE problem_id=%s AND t.id=l.tag_id;",[problem_id])
        problem_tags_titles=cursor.fetchall()
        tags=''
        for title in problem_tags_titles:
            print(title[0])
            tags+=title[0]+' '
        tags=tags[:-1]
        totemplate={'problems':problems,'tags':tags}
        return render_to_response('system/editproblem.html', totemplate)
    
    if request.GET.get('delete')=='true':
        cursor = connection.cursor()
        cursor.execute("DELETE FROM system_problem WHERE id=%s;", [problem_id])
        transaction.commit()
        xmlrefresh_problems()
        system_dec_problems()
        statistic_inc_problems(request.user.id)
        return HttpResponseRedirect('/problems/')
    
    if request.method == 'POST':
        try:
            if request.POST['type']=='editProblem':
                title=request.POST['title']
                description=request.POST['description']
                tags=request.POST['tags'].split(' ')
                for x in tags:
                        new_id_tag=tagid(request.user.id,x)
                        new_id_problemtaglist=problemtaglists_id(problem_id, new_id_tag)
                f=codecs.open("templates/"+str(request.POST['template']),'w','utf-8')
                f.write(request.POST['textarea'])
                f.close()
                cursor = connection.cursor()
                date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cursor.execute("UPDATE system_problem SET date=%s,description=%s,title=%s WHERE id=%s;", [date,description,title,problem_id])
                xmlrefresh_problems()
                transaction.commit()
                return HttpResponseRedirect('/problem/'+str(problem_id))
        except:
            pass
        
        form = NoteForm(request.POST)
        print(problem_id)
        if form.is_valid():
            user_id=request.user.id
            title=request.POST['title']
            tags=request.POST['tags'].split(' ')
            statistic_inc_notes(user_id)
            new_id=system_inc_notes()
            cursor = connection.cursor()
            cursor.execute("INSERT INTO system_note(id,user_id,problem_id,title,date) VALUES(%s,%s,%s,%s,%s);", [new_id, user_id, problem_id,str(title),datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
            problem_inc_notes(problem_id)
            for x in tags:
                add_tag_to_note(user_id,x,new_id)
            transaction.commit()
            xmlrefresh_notes(problem_id)
            return HttpResponseRedirect('/note/'+str(new_id))
    else:
        form = NoteForm()
        problem=Problem.objects.get(id=problem_id)
        cursor = connection.cursor()
        message = request.GET.get('sort')
        if message=='iddesc':
            cursor.execute("SELECT id,title,user_id,date FROM system_note WHERE problem_id=%s ORDER BY id DESC;", [problem_id] )
        elif message=='idasc':
            cursor.execute("SELECT id,title,user_id,date FROM system_note WHERE problem_id=%s ORDER BY id ASC;", [problem_id] )
        elif message=='titleasc':
            cursor.execute("SELECT id,title,user_id,date FROM system_note WHERE problem_id=%s ORDER BY title ASC;", [problem_id] )
        elif message=='titledesc':
            cursor.execute("SELECT id,title,user_id,date FROM system_note WHERE problem_id=%s ORDER BY title DESC;", [problem_id] )
        else:
            cursor.execute("SELECT id,title,user_id,date FROM system_note WHERE problem_id=%s ORDER BY id DESC;", [problem_id] )
        notes = cursor.fetchall()
        cursor = connection.cursor()
        cursor.execute("SELECT title FROM system_problem WHERE id=%s;", [problem_id])
        cat_title=cursor.fetchone()[0]
        cursor = connection.cursor()
        cursor.execute("SELECT l.tag_id,t.title FROM system_problemtaglist l , system_tag t WHERE problem_id=%s AND t.id=l.tag_id;",[problem_id])
        problem_tags=cursor.fetchall()

        
        cursor = connection.cursor()
        cursor.execute("SELECT user_id FROM system_problem WHERE id=%s;", [problem_id])
        problem_user_id=cursor.fetchone()[0]
        editable=(problem_user_id==request.user.id)
        cursor.execute("SELECT template FROM system_problem WHERE id=%s;", [problem_id])
        template=cursor.fetchone()[0]
        totemplate={'notes':notes,'form': form,'id':problem_id,'cat_title':cat_title,'tags':problem_tags,'editable':str(editable),'template':template}
        totemplate.update(system(request.user))
        return render_to_response('system/notes.html', totemplate)

	
@login_required
@transaction.commit_manually
def tag(request,tag_id):
	if request.GET.get('delete')=='true':
		cursor = connection.cursor()
		cursor.execute("DELETE FROM system_tag WHERE id=%s;", [tag_id])
		transaction.commit()
		return HttpResponseRedirect('/')
	if request.method == 'POST':
		title=request.POST['title']
		cursor = connection.cursor()
		cursor.execute("UPDATE system_tag SET title=%s WHERE id=%s;", [request.POST['title'],tag_id])
		transaction.commit()
		return HttpResponseRedirect('/')
	else:
		cursor = connection.cursor()
		cursor.execute("SELECT title FROM system_tag WHERE id=%s;",[tag_id])
		tag=cursor.fetchone()[0]
		cursor = connection.cursor()
		message = request.GET.get('sort3')
		if message=='iddesc':
			cursor.execute("SELECT DISTINCT e.id,e.user_id,e.date,e.description,e.title,e.template,e.notes,e.links,e.ideas,e.todos FROM system_problem e, system_problemtaglist list, system_tag tag WHERE tag.id=%s AND list.tag_id=tag.id AND e.id=list.problem_id ORDER BY e.id DESC;",[tag_id])
		elif message=='idasc':
			cursor.execute("SELECT DISTINCT e.id,e.user_id,e.date,e.description,e.title,e.template,e.notes,e.links,e.ideas,e.todos FROM system_problem e, system_problemtaglist list, system_tag tag WHERE tag.id=%s AND list.tag_id=tag.id AND e.id=list.problem_id ORDER BY e.id ASC;",[tag_id])
		elif message=='titleasc':
			cursor.execute("SELECT DISTINCT e.id,e.user_id,e.date,e.description,e.title,e.template,e.notes,e.links,e.ideas,e.todos FROM system_problem e, system_problemtaglist list, system_tag tag WHERE tag.id=%s AND list.tag_id=tag.id AND e.id=list.problem_id ORDER BY e.title ASC;",[tag_id])
		elif message=='titledesc':
			cursor.execute("SELECT DISTINCT e.id,e.user_id,e.date,e.description,e.title,e.template,e.notes,e.links,e.ideas,e.todos FROM system_problem e, system_problemtaglist list, system_tag tag WHERE tag.id=%s AND list.tag_id=tag.id AND e.id=list.problem_id ORDER BY e.title DESC;",[tag_id])
		else:
			cursor.execute("SELECT DISTINCT e.id,e.user_id,e.date,e.description,e.title,e.template,e.notes,e.links,e.ideas,e.todos FROM system_problem e, system_problemtaglist list, system_tag tag WHERE tag.id=%s AND list.tag_id=tag.id AND e.id=list.problem_id ORDER BY e.id DESC;",[tag_id])
		problems = cursor.fetchall()
		cursor = connection.cursor()
		message = request.GET.get('sort')
		if message=='iddesc':
			cursor.execute("SELECT DISTINCT n.id,n.title,n.user_id,n.date FROM system_note n, system_taglist list, system_tag tag WHERE tag.id=%s AND list.tag_id=tag.id AND n.id=list.note_id ORDER BY n.id DESC;",[tag_id])
		elif message=='idasc':
			cursor.execute("SELECT DISTINCT n.id,n.title,n.user_id,n.date FROM system_note n, system_taglist list, system_tag tag WHERE tag.id=%s AND list.tag_id=tag.id AND n.id=list.note_id ORDER BY n.id ASC;",[tag_id])
		elif message=='titleasc':
			cursor.execute("SELECT DISTINCT n.id,n.title,n.user_id,n.date FROM system_note n, system_taglist list, system_tag tag WHERE tag.id=%s AND list.tag_id=tag.id AND n.id=list.note_id ORDER BY n.title ASC;",[tag_id])
		elif message=='titledesc':
			cursor.execute("SELECT DISTINCT n.id,n.title,n.user_id,n.date FROM system_note n, system_taglist list, system_tag tag WHERE tag.id=%s AND list.tag_id=tag.id AND n.id=list.note_id ORDER BY n.title DESC;",[tag_id])
		else:
			cursor.execute("SELECT DISTINCT n.id,n.title,n.user_id,n.date FROM system_note n, system_taglist list, system_tag tag WHERE tag.id=%s AND list.tag_id=tag.id AND n.id=list.note_id ORDER BY n.id DESC;",[tag_id])
		notes = cursor.fetchall()
		cursor = connection.cursor()
		cursor.execute("SELECT user_id FROM system_tag WHERE id=%s;", [tag_id])
		user_id=cursor.fetchone()[0]
		editable=(user_id==request.user.id)
		tagform=TagForm({'title':tag})
		totemplate={'id':tag_id,'tag':tag,'tagform':tagform,'problems':problems,'notes':notes,'editable':str(editable)}
		totemplate.update(system(request.user))
		return render_to_response('system/tag.html',totemplate)

@login_required
@transaction.commit_manually
def problemtag(request,tag_id):
	if request.GET.get('delete')=='true':
		cursor = connection.cursor()
		cursor.execute("DELETE FROM system_tag WHERE id=%s;", [tag_id])
		transaction.commit()
		print("what?")
		return HttpResponseRedirect('/')
	if request.method == 'POST':
		title=request.POST['title']
		cursor = connection.cursor()
		cursor.execute("UPDATE system_tag SET title=%s WHERE id=%s;", [request.POST['title'],tag_id])
		transaction.commit()
		print("w?")
		return HttpResponseRedirect('/')
	else:
		cursor = connection.cursor()
		cursor.execute("SELECT title FROM system_tag WHERE id=%s;",[tag_id])
		tag=cursor.fetchone()[0]
		cursor = connection.cursor()
		message = request.GET.get('sort3')
		if message=='iddesc':
			cursor.execute("SELECT DISTINCT e.id,e.user_id,e.date,e.description,e.title,e.template,e.notes,e.links,e.ideas,e.todos FROM system_problem e, system_problemtaglist list, system_tag tag WHERE tag.id=%s AND list.tag_id=tag.id AND e.id=list.problem_id ORDER BY e.id DESC;",[tag_id])
		elif message=='idasc':
			cursor.execute("SELECT DISTINCT e.id,e.user_id,e.date,e.description,e.title,e.template,e.notes,e.links,e.ideas,e.todos FROM system_problem e, system_problemtaglist list, system_tag tag WHERE tag.id=%s AND list.tag_id=tag.id AND e.id=list.problem_id ORDER BY e.id ASC;",[tag_id])
		elif message=='titleasc':
			cursor.execute("SELECT DISTINCT e.id,e.user_id,e.date,e.description,e.title,e.template,e.notes,e.links,e.ideas,e.todos FROM system_problem e, system_problemtaglist list, system_tag tag WHERE tag.id=%s AND list.tag_id=tag.id AND e.id=list.problem_id ORDER BY e.title ASC;",[tag_id])
		elif message=='titledesc':
			cursor.execute("SELECT DISTINCT e.id,e.user_id,e.date,e.description,e.title,e.template,e.notes,e.links,e.ideas,e.todos FROM system_problem e, system_problemtaglist list, system_tag tag WHERE tag.id=%s AND list.tag_id=tag.id AND e.id=list.problem_id ORDER BY e.title DESC;",[tag_id])
		else:
			cursor.execute("SELECT DISTINCT e.id,e.user_id,e.date,e.description,e.title,e.template,e.notes,e.links,e.ideas,e.todos FROM system_problem e, system_problemtaglist list, system_tag tag WHERE tag.id=%s AND list.tag_id=tag.id AND e.id=list.problem_id ORDER BY e.id DESC;",[tag_id])
		problems = cursor.fetchall()
		
		cursor = connection.cursor()
		cursor.execute("SELECT user_id FROM system_tag WHERE id=%s;", [tag_id])
		user_id=cursor.fetchone()[0]
		editable=(user_id==request.user.id)
		tagform=TagForm({'title':tag})
		totemplate={'id':tag_id,'tag':tag,'tagform':tagform,'problems':problems,'editable':str(editable)}
		totemplate.update(system(request.user))
		return render_to_response('system/problemtag.html',totemplate)
		
	
@login_required
@transaction.commit_manually
def editproblem(request,problem_id):
	if request.GET.get('delete')=='true':
		cursor = connection.cursor()
		cursor.execute("DELETE FROM system_problem WHERE id=%s;", [problem_id])
		transaction.commit()
		xmlrefresh_problemlists(problem_id)
		return HttpResponseRedirect('/projects')
	if request.method == 'POST':
		title=request.POST['title']
		date=parsedatestr(request.POST['date'])
		description=request.POST['description']
		tags=request.POST['tags'].split(' ')
		for x in tags:
			new_id_tag=tagid(request.user.id,x)
			new_id_problemtaglist=problemtaglists_id(problem_id, new_id_tag)
		f=codecs.open("templates/"+str(request.POST['template']),'w','utf-8')
		f.write(request.POST['addproblem'])
		f.close()
		cursor = connection.cursor()
		print("update")
		cursor.execute("UPDATE system_problem SET date=%s,description=%s,title=%s WHERE id=%s;", [date,description,title,problem_id])
		transaction.commit()
		xmlrefresh_problemlists(problem_id)
		return HttpResponseRedirect('/problem/'+str(problem_id))
	else:
		cursor = connection.cursor()
		cursor.execute("SELECT id,user_id,date,description,title,template,notes,links,ideas,todos FROM system_problem WHERE id=%s;",[problem_id])
		problems=cursor.fetchall()
		cursor = connection.cursor()
		cursor.execute("SELECT DISTINCT t.title FROM system_problemtaglist l,system_tag t WHERE l.problem_id=%s AND t.id=l.tag_id;",[problem_id])
		tags=cursor.fetchall()
		strtags=""
		for tag in tags:
			strtags+=str(tag[0])+' '
		cursor = connection.cursor()
		cursor.execute("SELECT date FROM system_problem WHERE id=%s;",[problem_id])
		datetime=cursor.fetchone()[0]
		date=parsedatestr(datetime.strftime("%Y-%m-%d %H:%M:%S"))
		totemplate={'id':problem_id,'problems':problems,'tags':strtags,'date':date}
		totemplate.update(system(request.user))
		return render_to_response('system/editproblem.html',totemplate)

@login_required
@transaction.commit_manually
def problem(request,problem_id):
    if request.GET.get('delete')=='true':
        return HttpResponseRedirect('/editproblem/'+str(problem_id)+'?delete=true')
    if request.method == 'POST':
        if request.POST['type']=='Tag':
            add_tag_to_problem(request.user.id,request.POST['title'],problem_id)
            transaction.commit()
            return HttpResponseRedirect('/problem/'+str(problem_id))
        if request.POST['type']=='Project':
            form = ProjectForm(request.POST)
            if form.is_valid():
                cursor = connection.cursor()
                cursor.execute("SELECT a.id FROM system_problem f, system_framework a WHERE f.id=%s AND a.name=f.title;", [problem_id])
                framework_id=cursor.fetchone()[0]
                new=add_project(request.user.id,request.POST['title'],framework_id)
                transaction.commit()
                return HttpResponseRedirect('/project/'+str(new))
    else:
        cursor = connection.cursor()
        cursor.execute("SELECT user_id FROM system_problem WHERE id=%s;", [problem_id])
        user_id=cursor.fetchone()[0]
        editable=(user_id==request.user.id)
        cursor = connection.cursor()
        cursor.execute("SELECT title FROM system_problem WHERE id=%s;", [problem_id])
        cat_title=cursor.fetchone()[0]
        cursor = connection.cursor()
        cursor.execute("SELECT template FROM system_problem WHERE id=%s;", [problem_id])
        cat_template=cursor.fetchone()[0]
        cursor = connection.cursor()
        cursor.execute("SELECT tag.id,tag.title FROM system_tag tag, system_problemtaglist l WHERE l.problem_id=%s AND tag.id=l.tag_id ORDER BY tag.title DESC;", [problem_id] )
        private_tags = cursor.fetchall()
        form4=TagForm()
        cursor = connection.cursor()
        cursor.execute("SELECT a.id FROM system_problem f, system_framework a WHERE f.id=%s AND a.name=f.title;", [problem_id])
        framework_id=cursor.fetchone()[0]
        form = ProjectForm()
        cursor = connection.cursor()
        message = request.GET.get('sort')
        if message=='iddesc':
                cursor.execute("SELECT * FROM system_project WHERE framework_id=%s ORDER BY id DESC;",[framework_id])
        elif message=='idasc':
                cursor.execute("SELECT * FROM system_project WHERE framework_id=%s ORDER BY id ASC;",[framework_id])
        elif message=='titleasc':
                cursor.execute("SELECT * FROM system_project WHERE framework_id=%s ORDER BY title ASC;",[framework_id])
        elif message=='titledesc':
                cursor.execute("SELECT * FROM system_project WHERE framework_id=%s ORDER BY title DESC;",[framework_id])
        else:
                cursor.execute("SELECT * FROM system_project WHERE framework_id=%s ORDER BY id DESC;",[framework_id])	
        projects = cursor.fetchall()
        totemplate={'projects':projects,'form':form,'editable':str(editable),'form4':form4,'id':problem_id,'cat_title':cat_title,'tags':private_tags,'template':cat_template}
        totemplate.update(system(request.user))
        return render_to_response('system/problem.html', totemplate)


@login_required
@transaction.commit_manually
def problems(request):
    if xmlcheck_problems():
        xmlinit_problems()
    
    if request.method == 'POST':
        try:
            if request.POST['type']=="Problem":
                title=None
                date=None
                tags=None
                addproblem=None
                if request.POST['addproblem']!='':
                    addproblem=request.POST['addproblem']
                else:
                    addproblem="Empty"
                if request.POST['title']!="":
                    title=request.POST['title']
                else:
                    title="No title"
                if request.POST['description']!="":
                    description=request.POST['description']
                else:
                    description="no description"
                if request.POST['tags']!="":
                    tags=request.POST['tags'].split(' ')
                else:
                    tags=("Other",)
                date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                id=request.user.id
                text=addproblem
                new_problem_id=system_inc_problems()
                template="templates/problems/"+str(new_problem_id)+".html"
                subor=open(template,'w')
                template=template.replace("templates/",'')
                subor.write(text)
                subor.close()
                cursor=connection.cursor()
                cursor.execute("INSERT INTO system_problem(id,user_id,date,description,title,template,notes,links,ideas,todos) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);", [new_problem_id, id, date,description,title,template,0,0,0,0])
                for x in tags:
                    new_id_tag=tagid(id,x)
                    results = ProblemTagList.objects.filter(tag = new_id_tag)
                    if results.count()==0:
                        new_id_problemtaglist=system_inc_problemtaglists()
                        cursor = connection.cursor()
                        cursor.execute("INSERT INTO system_problemtaglist(id,problem_id,tag_id) VALUES(%s,%s,%s);", [new_id_problemtaglist, new_problem_id, new_id_tag ])
                xmlrefresh_problems()
                statistic_inc_problems(request.user.id)
                transaction.commit()
                return HttpResponseRedirect('/problem/'+str(new_problem_id))
        except:
            transaction.rollback()
    
        
    message = request.GET.get('sort')
    cursor = connection.cursor()
    if message=='iddesc':
            cursor.execute("SELECT id,user_id,date,description,title,template,notes,links,ideas,todos FROM system_problem ORDER BY id DESC;")
    elif message=='idasc':
            cursor.execute("SELECT id,user_id,date,description,title,template,notes,links,ideas,todos FROM system_problem ORDER BY id ASC;")
    elif message=='titleasc':
            cursor.execute("SELECT id,user_id,date,description,title,template,notes,links,ideas,todos FROM system_problem ORDER BY title ASC;")
    elif message=='titledesc':
            cursor.execute("SELECT id,user_id,date,description,title,template,notes,links,ideas,todos FROM system_problem ORDER BY title DESC;")
    else:
            cursor.execute("SELECT id,user_id,date,description,title,template,notes,links,ideas,todos FROM system_problem ORDER BY id DESC;")
    problems= cursor.fetchall()
    totemplate={'problems':problems,'showform':"False"}
    totemplate.update(system(request.user))
    return render_to_response('system/problems.html', totemplate)

@login_required
@transaction.commit_manually
def settings(request):
    if request.method == 'POST':
        try:
            if request.POST['type']=="Priority":
                cursor = connection.cursor()
                cursor.execute("SELECT id FROM system_prioritylist WHERE user_id=%s;",[request.user.id])
                prioritylist_id=cursor.fetchone()[0]
                priority=request.POST['slider-value']
                cursor = connection.cursor()
                cursor.execute("UPDATE system_prioritylist SET priority=%s WHERE id=%s;", [priority,prioritylist_id])
                transaction.commit()
            if request.POST['type']=="TimelineOn":
                cursor = connection.cursor()
                cursor.execute("SELECT id FROM system_timelinelist WHERE user_id=%s;",[request.user.id])
                timelinelist_id=cursor.fetchone()[0]
                cursor = connection.cursor()
                cursor.execute("UPDATE system_timelinelist SET show=1 WHERE id=%s;", [timelinelist_id])
                transaction.commit()
            if request.POST['type']=="TimelineOff":
                cursor = connection.cursor()
                cursor.execute("SELECT id FROM system_timelinelist WHERE user_id=%s;",[request.user.id])
                timelinelist_id=cursor.fetchone()[0]
                cursor = connection.cursor()
                cursor.execute("UPDATE system_timelinelist SET show=0 WHERE id=%s;", [timelinelist_id])
                transaction.commit()
            if request.POST['type']=="Frameworks":
                favorite=request.POST['param1']
                favorite=favorite.replace("&"," ")
                list=favorite.split(' ')
                if list!=[u'']:
                    for framework in list:
                        framework=framework.replace("thelist1[]=","")
                        cursor = connection.cursor()
                        cursor.execute("SELECT id FROM system_framework WHERE name=%s;",[framework])
                        framework_id=cursor.fetchone()[0]
                        activate(request.user.id,framework_id)
                others=request.POST['param2']
                others=others.replace("&"," ")
                list2=others.split(' ')
                if list2!=[u'']:
                    for framework in list2:
                        framework=framework.replace("thelist2[]=","")
                        cursor = connection.cursor()
                        cursor.execute("SELECT id FROM system_framework WHERE name=%s;",[framework])
                        framework_id=cursor.fetchone()[0]
                        deactivate(request.user.id,framework_id)
                transaction.commit()
            if request.POST['type']=="Theme":
                cursor = connection.cursor()
                theme=request.POST['themesdropdown']
                cursor.execute("SELECT id FROM system_theme WHERE name=%s;",[theme])
                theme_id=cursor.fetchone()[0]
                cursor = connection.cursor()
                cursor.execute("SELECT id FROM system_themelist WHERE user_id=%s;",[request.user.id])
                themelist_id=cursor.fetchone()[0]
                cursor = connection.cursor()
                cursor.execute("UPDATE system_themelist SET theme_id=%s WHERE id=%s;", [theme_id,themelist_id])
                transaction.commit()
            if request.POST['type']=="ChartStyle":
                cursor = connection.cursor()
                cursor.execute("SELECT id FROM system_chartstylelist WHERE user_id=%s;",[request.user.id])
                chartstyle_id=cursor.fetchone()[0]
                cursor = connection.cursor()
                cursor.execute("UPDATE system_chartstylelist SET chartstyle=%s WHERE id=%s;", [request.POST['chartstylesdropdown'],chartstyle_id])
                transaction.commit()
            if request.POST['type']=="ChartTheme":
                cursor = connection.cursor()
                cursor.execute("SELECT id FROM system_chartthemelist WHERE user_id=%s;",[request.user.id])
                charttheme_id=cursor.fetchone()[0]
                cursor = connection.cursor()
                cursor.execute("UPDATE system_chartthemelist SET charttheme=%s WHERE id=%s;", [request.POST['chartthemesdropdown'],charttheme_id])
                transaction.commit()
            return HttpResponseRedirect('/')
        except:
            transaction.rollback()
            return HttpResponseRedirect('/')
    else:
        totemplate={}
        totemplate.update(system(request.user))
        transaction.commit()
        return render_to_response('system/home.html', totemplate)

@login_required
def statistics(request):
    cursor=connection.cursor()
    cursor.execute("SELECT tags,notes,links,ideas,todos,problems,projects,files FROM system_statistic WHERE user_id=%s;",[request.user.id])
    userstats = cursor.fetchall()
    
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM system_sequences;")
    system_id=cursor.fetchone()[0]
    
    cursor = connection.cursor()
    cursor.execute("SELECT tags,notes,links,ideas,todos,problems,projects,sourcecodefiles FROM system_sequences WHERE id=%s;",[system_id])
    totalstats = cursor.fetchall()
    totemplate={'userstats':userstats,'totalstats':totalstats,'user':request.user.username}
    totemplate.update(system(request.user))
    return render_to_response('system/statistics.html', totemplate)

def signup(request):
    if request.method == 'POST':
            form=RegistrationForm(request.POST)
            form.signup(request.POST['username'],request.POST['email'],request.POST['password1'],request.POST['password2'])
            if form.is_valid():
                transaction.commit()
                return HttpResponseRedirect('/accounts/login')
            else:
                totemplate={'form':form}
                totemplate.update(system(request.user))
                return render_to_response('system/signup.html', totemplate)
        
    form=RegistrationForm()
    totemplate={'form':form}
    totemplate.update(system(request.user))
    return render_to_response('system/signup.html', totemplate)

def solution(request,inputfile_id,framework_id):
    cursor = connection.cursor()
    cursor.execute("SELECT o.fitness FROM system_outputfile o WHERE o.inputfile_id=%s AND o.framework_id=%s ORDER BY o.id ASC;",[inputfile_id,framework_id])
    outputfiles = cursor.fetchall()
    
    sum=0
    i=0
    for output in outputfiles:
        sum+=output[0]
        i+=1
    average=sum/i
    
    cursor = connection.cursor()
    cursor.execute("SELECT o.id,o.fitness FROM system_outputfile o WHERE o.inputfile_id=%s AND o.framework_id=%s ORDER BY o.fitness ASC;",[inputfile_id,framework_id])
    orderedoutputfiles = cursor.fetchall()
    
    cursor = connection.cursor()
    cursor.execute("SELECT f.name FROM system_framework f WHERE f.id=%s;",[framework_id])
    frameworkname = cursor.fetchone()[0]
    
    cursor = connection.cursor()
    cursor.execute("SELECT f.problem_id FROM system_inputfile f WHERE f.id=%s;",[inputfile_id])
    problem_id = cursor.fetchone()[0]
    
    cursor = connection.cursor()
    cursor.execute("SELECT p.title FROM system_problem p WHERE p.id=%s;",[problem_id])
    problemtitle = cursor.fetchone()[0]
    
    totemplate={'outputfiles':outputfiles,'frameworkname':frameworkname,'orderedoutputfiles':orderedoutputfiles,'inputfileid':inputfile_id,'frameworkid':framework_id,'problemid':problem_id,'problemtitle':problemtitle,'average':average}
    totemplate.update(system(request.user))
    return render_to_response('system/solution.html', totemplate)

def solutions(request,problem_id,framework_id):
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT i.id FROM system_problem p,system_project j,system_framework f,system_inputfile i WHERE i.problem_id=p.id AND j.framework_id=f.id AND j.problem_id=p.id AND f.id=%s;",[framework_id])
    inputfiles = cursor.fetchall()
    
    cursor = connection.cursor()
    cursor.execute("SELECT f.name FROM system_framework f WHERE f.id=%s;",[framework_id])
    frameworkname = cursor.fetchone()[0]
    
    cursor = connection.cursor()
    cursor.execute("SELECT p.title FROM system_problem p WHERE p.id=%s;",[problem_id])
    problemtitle = cursor.fetchone()[0]
    
    totemplate={'inputfiles':inputfiles,'frameworkname':frameworkname,'problemtitle':problemtitle,'frameworkid':framework_id}
    totemplate.update(system(request.user))
    return render_to_response('system/frameworkinputfiles.html', totemplate)


@transaction.commit_manually
def ide(request,problem_id,project_id):
    openedide=None
    openedtemplate=None
    openedname=None
    openedid=None
    openedide=None
    frameworkid=None
    frameworkname=None
    frameworkdir=None
    frameworkextension=None
    frameworkcoding=None
    frameworkrundirectly=None
    buildcommand=None
    buildparameters=None
    runcommand=None
    beforeruncommands=None
    
    if request.GET.get('opened')=='true':
        openedide=True
    else:
        openedide=False
    
    cursor = connection.cursor()
    cursor.execute("SELECT title FROM system_problem WHERE id=%s;",[problem_id])
    problem_title=cursor.fetchone()[0]
    totemplate={'problem_title':problem_title,'problem_id':problem_id,'project_id':project_id}
    
    if (project_id!='0'):
        totemplate.update({'problem_id':problem_id})
        cursor = connection.cursor()
        cursor.execute("SELECT user_id FROM system_project WHERE id=%s;",[project_id])
        project_user_id=cursor.fetchone()[0]
        editable=(request.user.id==project_user_id)
        totemplate.update({'editable':editable})
        cursor = connection.cursor()
        cursor.execute("SELECT public FROM system_project WHERE id=%s;",[project_id])
        project_public=cursor.fetchone()[0]
        totemplate.update({'public':project_public})
        cursor = connection.cursor()
        cursor.execute("SELECT runnable FROM system_project WHERE id=%s;",[project_id])
        project_runnable=cursor.fetchone()[0]
        totemplate.update({'runnable':str(project_runnable)})
        openedide=True
        cursor = connection.cursor()
        cursor.execute("SELECT f.id,f.name,f.dir,f.extension,f.coding,f.rundirectly,f.buildcommand,f.buildparameters,f.runcommand,f.beforeruncommands FROM system_framework f, system_project p WHERE f.id=p.framework_id AND p.id=%s;",[project_id])
        framework = cursor.fetchone()
        frameworkid=framework[0]
        frameworkname=framework[1]
        frameworkdir=framework[2]
        frameworkextension=framework[3]
        frameworkcoding=framework[4]
        frameworkrundirectly=framework[5]
        buildcommand=framework[6]
        buildparameters=framework[7]
        runcommand=framework[8]
        beforeruncommands=framework[9]
        
    if request.GET.get('makerunnable')=='true':
        cursor = connection.cursor()
        cursor.execute("UPDATE system_project SET runnable=1 WHERE id=%s;", [project_id])
        transaction.commit()
        return HttpResponseRedirect('/ide/'+problem_id+'/'+project_id)
        
    if request.GET.get('build')=='true':
        cursor.execute("SELECT priority FROM system_prioritylist WHERE user_id=%s",[request.user.id])
        priority = cursor.fetchone()[0]
        cd=frameworkdir+"/"+str(project_id)
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM system_sourcecodefile WHERE project_id=%s;",[project_id])
        sourcecodefiles = cursor.fetchall()
        files=""
        for sourcecodefile in sourcecodefiles:
            files+=sourcecodefile[0]
            files+="."+frameworkextension+" "
        totemplate.update({'openedide':"False",'buildcommand':buildcommand,'buildparameters':buildparameters,"priority":priority,"cd":cd,"files":files})
        return render_to_response('ide/build.html', totemplate)
        
    cursor = connection.cursor()
    cursor.execute("SELECT link.id,link.name FROM system_projectlinklist list, system_link link WHERE list.project_id=%s AND link.id=list.link_id ORDER BY link.id DESC;", [project_id] )
    links = cursor.fetchall()
    cursor = connection.cursor()
    cursor.execute("SELECT todo.id,todo.name FROM system_projecttodolist list, system_todo todo WHERE list.project_id=%s AND todo.id=list.todo_id ORDER BY todo.id DESC;", [project_id] )
    todos = cursor.fetchall()
    cursor = connection.cursor()
    cursor.execute("SELECT idea.id,idea.name FROM system_projectidealist list, system_idea idea WHERE list.project_id=%s AND idea.id=list.idea_id ORDER BY idea.id DESC;", [project_id] )
    ideas = cursor.fetchall()
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM system_inputfile WHERE problem_id=%s;",[problem_id])
    inputfiles = cursor.fetchall()
    totemplate.update({'openedide':str(openedide),'frameworkextension':frameworkextension,'frameworkrundirectly':str(frameworkrundirectly),'inputfiles':inputfiles})
    cursor = connection.cursor()
    cursor.execute("SELECT id,name FROM system_inputgeneratorfile WHERE problem_id=%s;", [problem_id] )
    inputgenerators = cursor.fetchall()
    totemplate.update({'links':links,'ideas':ideas,'todos':todos,'inputgenerators':inputgenerators})
    
    if request.method == 'POST':
        
        if request.POST['type']=="viewSolution":
            outputid=request.POST['outputid']
            fitness=request.POST['fitness']
            cursor = connection.cursor()
            cursor.execute("SELECT template FROM system_outputfile WHERE id=%s;", [outputid])
            template=cursor.fetchone()[0]
            cursor = connection.cursor()
            cursor.execute("UPDATE system_outputfile SET fitness=%s WHERE id=%s;",[fitness,outputid])
            transaction.commit()
            cursor = connection.cursor()
            cursor.execute("SELECT id,name FROM system_sourcecodefile WHERE project_id=%s;",[project_id])
            sourcecodefiles = cursor.fetchall()
            totemplate.update({'sourcecodefiles':sourcecodefiles,'openedsourcecode':"False",'template':template})
            return render_to_response('ide/viewsolution.html', totemplate)
        
        if request.POST['type']=="runInputGeneratorFile":
            newid=system_inc_inputfiles()
            template="inputs/"+str(newid)+".in"
            f=codecs.open("/ecoude/"+template,'w','utf-8')
            f.write(request.POST['input'])
            f.flush()
            f.close()
            cursor = connection.cursor()
            cursor.execute("INSERT INTO system_inputfile(id,template,problem_id) VALUES(%s,%s,%s);", [newid, template, problem_id])
            newoutid=system_inc_outputfiles()
            templateout="outputs/"+str(newoutid)+".out"
            cursor = connection.cursor()
            cursor.execute("INSERT INTO system_outputfile(id,fitness,template,inputfile_id,solved,framework_id) VALUES(%s,0,%s,%s,0,%s);", [newoutid, templateout, newid,frameworkid])
            g=codecs.open("/ecoude/"+templateout,'w','utf-8')
            g.close()
            cursor.execute("SELECT priority FROM system_prioritylist WHERE user_id=%s",[request.user.id])
            priority = cursor.fetchone()[0]
            cd=frameworkdir+"/"+str(project_id)
            cursor = connection.cursor()
            cursor.execute("SELECT chartstyle FROM system_chartstylelist WHERE user_id=%s",[request.user.id])
            chartstyle = cursor.fetchone()[0]
            cursor = connection.cursor()
            cursor.execute("SELECT charttheme FROM system_chartthemelist WHERE user_id=%s",[request.user.id])
            charttheme = cursor.fetchone()[0]
            transaction.commit()
            if request.POST['rund']=="True":
                cursor.execute("SELECT name FROM system_sourcecodefile WHERE id=%s;",[request.POST['fileid']])
                sourcecodename = cursor.fetchone()[0]
                runcommand+=" "+str(sourcecodename)+"."+str(frameworkextension)
            totemplate.update({'openedide':"False",'runcommand':runcommand,'beforeruncommands':beforeruncommands,"priority":priority,"cd":cd,"input":"/ecoude/"+template,"output":"/ecoude/"+templateout,"outputid":newoutid,"chartstyle":chartstyle,"charttheme":charttheme})
            return render_to_response('ide/run.html', totemplate)
        
        if request.POST['type']=="testInputGeneratorFile":
            totemplate.update({'testinput':request.POST['input']})
            cursor = connection.cursor()
            cursor.execute("SELECT id,name FROM system_sourcecodefile WHERE project_id=%s;",[project_id])
            sourcecodefiles = cursor.fetchall()
            totemplate.update({'sourcecodefiles':sourcecodefiles})
            return render_to_response('ide/testedinputgeneratorfile.html', totemplate)
            
        if request.POST['type']=="newInputGeneratorFile":
            name=request.POST['name']
            new_id=system_inc_inputgeneratorfiles()
            template="inputgeneratorfiles/"+str(new_id)
            f=codecs.open("/ecoude/"+template,'w','utf-8')
            f.close()
            cursor = connection.cursor()
            cursor.execute("INSERT INTO system_inputgeneratorfile(id,name,template,problem_id,user_id) VALUES(%s,%s,%s,%s,%s);", [new_id, name,template,problem_id,request.user.id])
            transaction.commit()
            return HttpResponseRedirect('/ide/'+str(problem_id)+'/'+str(project_id)+"?openinputgeneratorfile=true&id="+str(new_id))
            
        if request.POST['type']=="renameInputGeneratorFile":
            cursor = connection.cursor()
            cursor.execute("UPDATE system_inputgeneratorfile SET name=%s WHERE id=%s;",[request.POST['name'],request.POST['id']])
            transaction.commit()
            return HttpResponseRedirect('/ide/'+str(problem_id)+'/'+str(project_id)+'?opensourcecodefile=true&id='+str(request.POST['id']))
        
        if request.POST['type']=="renameProject":
            cursor = connection.cursor()
            cursor.execute("UPDATE system_project SET title=%s WHERE id=%s;",[request.POST['name'],project_id])
            transaction.commit()
            return HttpResponseRedirect('/ide/'+str(problem_id)+'/'+str(project_id))
        
        if request.POST['type']=="renameSourceCode":
            cursor = connection.cursor()
            cursor.execute("UPDATE system_sourcecodefile SET name=%s WHERE id=%s;",[request.POST['name'],request.POST['id']])
            transaction.commit()
            return HttpResponseRedirect('/ide/'+str(problem_id)+'/'+str(project_id)+'?opensourcecodefile=true&id='+str(request.POST['id']))
        
        if request.POST['type']=="changeSourceCode":
            return HttpResponseRedirect('/ide/'+str(problem_id)+'/'+str(project_id)+'?opensourcecodefile=true&id='+str(request.POST['sourcecodefile']))
            
        if request.POST['type']=="Link":
            add_link_to_project(request.user.id,request.POST['name'],request.POST['text'],project_id)
            transaction.commit()
            
        if request.POST['type']=="Idea":
            add_idea_to_project(request.user.id,request.POST['name'],request.POST['text'],project_id)
            transaction.commit()
            
        if request.POST['type']=="Todo":
            add_todo_to_project(request.user.id,request.POST['name'],request.POST['text'],project_id)
            transaction.commit()
            
        if request.POST['type']=='editIdea':
            cursor = connection.cursor()
            cursor.execute("UPDATE system_idea SET name=%s,text=%s WHERE id=%s;",[request.POST['name'],request.POST['text'],request.POST['editid']])
            transaction.commit()
            return HttpResponseRedirect('/ide/'+problem_id+'/'+project_id)
        
        if request.POST['type']=='editLink':
            cursor = connection.cursor()
            cursor.execute("UPDATE system_link SET name=%s,text=%s WHERE id=%s;",[request.POST['name'],request.POST['text'],request.POST['editid']])
            transaction.commit()
            return HttpResponseRedirect('/ide/'+problem_id+'/'+project_id)
        
        if request.POST['type']=='editTodo':
            cursor = connection.cursor()
            cursor.execute("UPDATE system_todo SET name=%s,text=%s WHERE id=%s;",[request.POST['name'],request.POST['text'],request.POST['editid']])
            transaction.commit()
            return HttpResponseRedirect('/ide/'+problem_id+'/'+project_id)
        
        if request.POST['type']=="Project":
            title=request.POST['title']
            framework_id=request.POST['framework']
            cursor = connection.cursor()
            cursor.execute("SELECT f.dir FROM system_framework f WHERE f.id=%s;",[framework_id])
            frameworkdir = cursor.fetchone()[0]
            statistic_inc_projects(request.user.id)
            new_id=system_inc_projects()
            cursor = connection.cursor()
            cursor.execute("SELECT f.rundirectly FROM system_framework f WHERE f.id=%s;",[framework_id])
            frameworkrundirectly=cursor.fetchone()[0]
            cursor.execute("INSERT INTO system_project(id,title,framework_id,problem_id,runnable,public,user_id) VALUES(%s,%s,%s,%s,%s,%s,%s);", [new_id, title,framework_id,problem_id,frameworkrundirectly,0,request.user.id])
            os.mkdir("/ecoude/"+str(frameworkdir)+"/"+str(new_id))
            transaction.commit()
            return HttpResponseRedirect('/ide/'+str(problem_id)+'/'+str(new_id)+'?newsourcecodefile=true')
        
        if request.POST['type']=="NewSourceCodeFile":
            title=request.POST['name']
            statistic_inc_files(request.user.id)
            template=str(project_id)+"/"+str(title)+"."+str(frameworkextension)
            new_id=system_inc_sourcecodefiles()
            cursor = connection.cursor()
            cursor.execute("INSERT INTO system_sourcecodefile(id,name,template,project_id) VALUES(%s,%s,%s,%s);", [new_id, title,template,project_id])
            f=codecs.open("/ecoude/"+str(frameworkdir)+"/"+template,'w',frameworkcoding)
            f.close()
            transaction.commit()
            return HttpResponseRedirect('/ide/'+str(problem_id)+'/'+str(project_id)+'?opensourcecodefile=true&id='+str(new_id))
        
        if request.POST['type']=="SourceCodeFile":
            cursor = connection.cursor()
            cursor.execute("SELECT template FROM system_sourcecodefile WHERE id=%s;",[request.POST['id']])
            template=cursor.fetchone()[0]
            f=codecs.open("/ecoude/"+str(frameworkdir)+"/"+template,'w',frameworkcoding)
            f.write(request.POST['template'])
            f.close()
            return HttpResponseRedirect('/ide/'+str(problem_id)+'/'+str(project_id)+'?opensourcecodefile=true&id='+request.POST['id'])
        
        if request.POST['type']=="InputGeneratorFile":
            cursor = connection.cursor()
            cursor.execute("SELECT template FROM system_inputgeneratorfile WHERE id=%s;",[request.POST['id']])
            template=cursor.fetchone()[0]
            f=codecs.open("/ecoude/"+template,'w','utf-8')
            f.write(request.POST['template'])
            f.close()
            return HttpResponseRedirect('/ide/'+str(problem_id)+'/'+str(project_id)+'?openinputgeneratorfile=true&id='+request.POST['id'])
            
    if request.GET.get('run')=='true':
        newid=request.GET.get('id')
        cursor = connection.cursor()
        cursor.execute("SELECT template FROM system_inputfile WHERE id=%s;", [newid])
        template=cursor.fetchone()[0]
        newoutid=system_inc_outputfiles()
        templateout="outputs/"+str(newoutid)+".out"
        cursor = connection.cursor()
        cursor.execute("INSERT INTO system_outputfile(id,fitness,template,inputfile_id,solved,framework_id) VALUES(%s,0,%s,%s,0,%s);", [newoutid, templateout, newid,frameworkid])
        g=codecs.open("/ecoude/"+templateout,'w','utf-8')
        g.close()
        cursor.execute("SELECT priority FROM system_prioritylist WHERE user_id=%s",[request.user.id])
        priority = cursor.fetchone()[0]
        cd=frameworkdir+"/"+str(project_id)
        cursor = connection.cursor()
        cursor.execute("SELECT chartstyle FROM system_chartstylelist WHERE user_id=%s",[request.user.id])
        chartstyle = cursor.fetchone()[0]
        cursor = connection.cursor()
        cursor.execute("SELECT charttheme FROM system_chartthemelist WHERE user_id=%s",[request.user.id])
        charttheme = cursor.fetchone()[0]
        transaction.commit()
        if request.GET.get('rundirectly')=='true':
                cursor.execute("SELECT name FROM system_sourcecodefile WHERE id=%s;",[request.GET.get('fileid')])
                sourcecodename = cursor.fetchone()[0]
                runcommand+=" "+str(sourcecodename)+"."+str(frameworkextension)
        totemplate.update({'openedide':"False",'runcommand':runcommand,'beforeruncommands':beforeruncommands,"priority":priority,"cd":cd,"input":"/ecoude/"+template,"output":"/ecoude/"+templateout,"outputid":newoutid,"chartstyle":chartstyle,"charttheme":charttheme})
        return render_to_response('ide/run.html', totemplate)
    
    if request.GET.get('projects')=='true':
        cursor = connection.cursor()
        cursor.execute("SELECT id,name FROM system_framework;")
        frameworks=cursor.fetchall()
        totemplate.update({'frameworks':frameworks})
        cursor = connection.cursor()
        cursor.execute("SELECT id,title FROM system_project WHERE problem_id=%s AND public=1;",[problem_id])
        public=cursor.fetchall()
        cursor = connection.cursor()
        cursor.execute("SELECT id,title FROM system_project WHERE problem_id=%s AND user_id=%s AND public=0;",[problem_id,request.user.id])
        private=cursor.fetchall()
        totemplate.update({'public':public})
        totemplate.update({'private':private})
        return render_to_response('ide/projects.html', totemplate)

    if request.GET.get('newinputgeneratorfile')=='true':
        return render_to_response('ide/newinputgeneratorfile.html', totemplate)
    
    if request.GET.get('openinputgeneratorfile')=='true':
        id=request.GET.get('id')
        cursor = connection.cursor()
        cursor.execute("SELECT template FROM system_inputgeneratorfile WHERE id=%s;", [id])
        template=cursor.fetchone()[0]
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM system_inputgeneratorfile WHERE id=%s;", [id])
        name=cursor.fetchone()[0]
        cursor = connection.cursor()
        cursor.execute("SELECT user_id FROM system_inputgeneratorfile WHERE id=%s;", [id])
        user_id=cursor.fetchone()[0]
        editableinputgenerator=(request.user.id==user_id)
        cursor = connection.cursor()
        cursor.execute("SELECT id,name FROM system_sourcecodefile WHERE project_id=%s;",[project_id])
        sourcecodefiles = cursor.fetchall()
        cursor = connection.cursor()
        cursor.execute("SELECT id,name FROM system_inputgeneratorfile WHERE problem_id=%s AND id!=%s;", [problem_id,id] )
        inputgenerators = cursor.fetchall()
        totemplate.update({'openedid':id,'openedtemplate':template,'inputgenerator':"True",'sourcecodefiles':sourcecodefiles,'openedgeneratorid':id,'openedgeneratorname':name,'inputgenerators':inputgenerators,'editableinputgenerator':str(editableinputgenerator)})
        return render_to_response('ide/openinputgeneratorfile.html', totemplate)
    
    if request.GET.get('testinputgenerator')=='true':
        id=request.GET.get('id')
        cursor = connection.cursor()
        cursor.execute("SELECT template FROM system_inputgeneratorfile WHERE id=%s;", [id])
        template=cursor.fetchone()[0]
        totemplate.update({'testinputgenerator':"True",'template':template})
        return render_to_response('ide/testinputgeneratorfile.html', totemplate)
    
    if request.GET.get('runinputgenerator')=='true':
        id=request.GET.get('id')
        cursor = connection.cursor()
        cursor.execute("SELECT template FROM system_inputgeneratorfile WHERE id=%s;", [id])
        template=cursor.fetchone()[0]
        rund=None
        fileid=None
        if request.GET.get('rundirectly')=='true':
            rund="True"
            fileid=request.GET.get('fileid')
        else:
            rund="False"
        totemplate.update({'runinputgenerator':"True",'template':template,'generatorid':id,'rund':rund,'fileid':fileid})
        return render_to_response('ide/runinputgenerator.html', totemplate)
    
    if request.GET.get('make_public')=='true':
        cursor = connection.cursor()
        cursor.execute("UPDATE system_project SET public=1 WHERE id=%s;", [project_id])
        transaction.commit()
        return HttpResponseRedirect('/ide/'+problem_id+'/'+project_id)
    
    if request.GET.get('make_private')=='true':
        cursor = connection.cursor()
        cursor.execute("UPDATE system_project SET public=0 WHERE id=%s;", [project_id])
        transaction.commit()
        return HttpResponseRedirect('/ide/'+problem_id+'/'+project_id)
    
    if request.GET.get('deletelink')=='true':
        delete_link_from_project(request.user.id,request.GET.get('id'),project_id)
        transaction.commit()
        return HttpResponseRedirect('/ide/'+problem_id+'/'+project_id)
    
    if request.GET.get('deleteidea')=='true':
        delete_idea_from_project(request.user.id,request.GET.get('id'),project_id)
        transaction.commit()
        return HttpResponseRedirect('/ide/'+problem_id+'/'+project_id)
    
    if request.GET.get('deletetodo')=='true':
        delete_todo_from_project(request.user.id,request.GET.get('id'),project_id)
        transaction.commit()
        return HttpResponseRedirect('/ide/'+problem_id+'/'+project_id)
    
    if request.GET.get('showlink')=='true':
        link_id=request.GET.get('id')
        cursor = connection.cursor()
        cursor.execute("SELECT user_id,name,text FROM system_link WHERE id=%s;", [link_id])
        link=cursor.fetchone()
        form = LinkForm({'name':link[1],'text':link[2]})
        editablelink=(link[0]==request.user.id)
        totemplate.update({'form':form,'editablelink':str(editablelink),'id':link_id})
        return render_to_response('ide/showlink.html', totemplate)
    
    if request.GET.get('showidea')=='true':
        idea_id=request.GET.get('id')
        cursor = connection.cursor()
        cursor.execute("SELECT user_id,name,text FROM system_idea WHERE id=%s;", [idea_id])
        idea=cursor.fetchone()
        form = IdeaForm({'name':idea[1],'text':idea[2]})
        editableidea=(idea[0]==request.user.id)
        totemplate.update({'form':form,'editableidea':str(editableidea),'id':idea_id})
        return render_to_response('ide/showidea.html', totemplate)
    
    if request.GET.get('showtodo')=='true':
        todo_id=request.GET.get('id')
        cursor = connection.cursor()
        cursor.execute("SELECT user_id,name,text FROM system_todo WHERE id=%s;", [todo_id])
        todo=cursor.fetchone()
        form = TodoForm({'name':todo[1],'text':todo[2]})
        editabletodo=(todo[0]==request.user.id)
        totemplate.update({'form':form,'editabletodo':str(editabletodo),'id':todo_id})
        return render_to_response('ide/showtodo.html', totemplate)
        
    if request.GET.get('newlink')=='true':
        form = LinkForm()
        totemplate.update({'form':form})
        return render_to_response('ide/addlink.html', totemplate)
    
    if request.GET.get('newidea')=='true':
        form = IdeaForm()
        totemplate.update({'form':form})
        return render_to_response('ide/addidea.html', totemplate)
    
    if request.GET.get('newtodo')=='true':
        form = TodoForm()
        totemplate.update({'form':form})
        return render_to_response('ide/addtodo.html', totemplate)
    
    if request.GET.get('newsourcecodefile')=='true':
        return render_to_response('ide/newsourcecodefile.html', totemplate)
    
    if request.GET.get('opensourcecodefile')=='true':
        sourcecodefile_id=request.GET.get('id')
        cursor = connection.cursor()
        cursor.execute("SELECT id,name,template FROM system_sourcecodefile WHERE id=%s;",[sourcecodefile_id])
        sourcecodefile=cursor.fetchone()
        openedtemplate=sourcecodefile[2]
        openedname=sourcecodefile[1]
        openedid=sourcecodefile[0]
        cursor = connection.cursor()
        cursor.execute("SELECT id,name FROM system_sourcecodefile WHERE project_id=%s AND id!=%s;",[project_id,openedid])
        sourcecodefiles = cursor.fetchall()
        totemplate.update({'openedid':openedid,'openedname':openedname,'openedtemplate':str(frameworkdir)+"/"+openedtemplate,'sourcecodefiles':sourcecodefiles,'openedsourcecode':"True"})
        return render_to_response('ide/openfile.html', totemplate)
    
    if request.GET.get('renamesourcecodefile')=='true':
        sourcecodefile_id=request.GET.get('id')
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM system_sourcecodefile WHERE id=%s;",[sourcecodefile_id])
        sourcecodefilename=cursor.fetchone()[0]
        totemplate.update({'openedid':sourcecodefile_id,'name':sourcecodefilename,'openedsourcecode':"True"})
        return render_to_response('ide/renamesourcecodefile.html', totemplate)
    
    if request.GET.get('renameinputgeneratorfile')=='true':
        inputgeneratorfile_id=request.GET.get('id')
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM system_inputgeneratorfile WHERE id=%s;",[inputgeneratorfile_id])
        inputgeneratorfilename=cursor.fetchone()[0]
        cursor = connection.cursor()
        cursor.execute("SELECT id,name FROM system_sourcecodefile WHERE project_id=%s;",[project_id])
        sourcecodefiles = cursor.fetchall()
        totemplate.update({'openedid':inputgeneratorfile_id,'name':inputgeneratorfilename,'inputgenerator':"True",'sourcecodefiles':sourcecodefiles})
        return render_to_response('ide/renameinputgeneratorfile.html', totemplate)
    
    if request.GET.get('deletesourcecodefile')=='true':
        sourcecodefile_id=request.GET.get('id')
        cursor = connection.cursor()
        cursor.execute("SELECT template FROM system_sourcecodefile WHERE id=%s;",[sourcecodefile_id])
        template=cursor.fetchone()[0]
        cursor.execute("DELETE FROM system_sourcecodefile WHERE id=%s;", [sourcecodefile_id])
        os.remove("/ecoude/"+str(frameworkdir)+"/"+template)
        system_dec_sourcecodefiles()
        transaction.commit()
        return HttpResponseRedirect('/ide/'+problem_id+'/'+project_id)
    
    if request.GET.get('deleteinputgeneratorfile')=='true':
        inputgeneratorfile_id=request.GET.get('id')
        cursor = connection.cursor()
        cursor.execute("SELECT template FROM system_inputgeneratorfile WHERE id=%s;",[inputgeneratorfile_id])
        template=cursor.fetchone()[0]
        cursor.execute("DELETE FROM system_inputgeneratorfile WHERE id=%s;", [inputgeneratorfile_id])
        os.remove("/ecoude/"+template)
        system_dec_inputgeneratorfiles()
        transaction.commit()
        return HttpResponseRedirect('/ide/'+problem_id+'/'+project_id)
    
    if request.GET.get('deleteproject')=='true':
        cursor = connection.cursor()
        cursor.execute("DELETE FROM system_project WHERE id=%s;", [project_id])
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM system_sourcecodefile WHERE project_id=%s;",[project_id])
        sourcecodefiles = cursor.fetchall()
        print(sourcecodefiles)
        for sourcecodefile in sourcecodefiles:
            cursor = connection.cursor()
            cursor.execute("SELECT template FROM system_sourcecodefile WHERE id=%s;",[sourcecodefile[0]])
            template=cursor.fetchone()[0]
            cursor.execute("DELETE FROM system_sourcecodefile WHERE id=%s;", [sourcecodefile[0]])
            os.remove("/ecoude/"+str(frameworkdir)+"/"+template)
            system_dec_sourcecodefiles()
        transaction.commit()
        return HttpResponseRedirect('/ide/'+problem_id+'/0?projects=true')
    
    if request.GET.get('newproject')=='true':
        cursor = connection.cursor()
        cursor.execute("SELECT id,name FROM system_framework;")
        frameworks=cursor.fetchall()
        totemplate.update({'frameworks':frameworks})
        return render_to_response('ide/newproject.html', totemplate)
    
    if request.GET.get('renameproject')=='true':
        cursor = connection.cursor()
        cursor.execute("SELECT title FROM system_project WHERE id=%s;",[project_id])
        projectname=cursor.fetchone()[0]
        totemplate.update({'name':projectname})
        return render_to_response('ide/renameproject.html', totemplate)
    
    cursor = connection.cursor()
    cursor.execute("SELECT id,name FROM system_sourcecodefile WHERE project_id=%s;",[project_id])
    sourcecodefiles = cursor.fetchall()
    totemplate.update({'sourcecodefiles':sourcecodefiles,'openedsourcecode':"False"})
    return render_to_response('ide/ide.html', totemplate)

def output(request,outputfile_id):
    cursor = connection.cursor()
    cursor.execute("SELECT template,fitness FROM system_outputfile WHERE id=%s;", [outputfile_id])
    file = cursor.fetchone()
    template=file[0]
    fitness=file[1]
    totemplate={'inputfile_id':request.GET.get('inputfile_id'),'framework_id':request.GET.get('framework_id'),'template':template,'fitness':fitness}
    totemplate.update(system(request.user))
    return render_to_response('system/output.html', totemplate)

def about(request):
    totemplate={}
    totemplate.update(system(request.user))
    return render_to_response('system/about.html', totemplate)

def home(request):
    totemplate={}
    totemplate.update(system(request.user))
    return render_to_response('system/home.html', totemplate)
