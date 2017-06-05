from django.contrib.auth.models import User
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render

from app.forms import ListForm, TaskForm, CommentForm
from app.functions import ok_json, bad_json
from app.models import List, Task, Comment


def views(request):

    data = {'title': 'To Do Application - My Lists'}


    if request.method == 'POST':
        if 'action' in request.POST and request.POST['action'] != '':
            action = request.POST['action']

            if action == 'create':
                    try:
                        with transaction.atomic():
                            f = ListForm(request.POST)
                            if f.is_valid():
                                name = f.cleaned_data['name']
                                priority = f.cleaned_data['priority']
                                assigned_to = f.cleaned_data['assigned_to']
                                due_date = f.cleaned_data['due_date']

                                if not name:
                                    return bad_json(message='Please enter a list name.')

                                if not priority:
                                    return bad_json(message='Please select a priority.')

                                if not assigned_to:
                                        return bad_json(message='Please select a user to assign this list.')

                                if not due_date:
                                    return bad_json(message='Please select a due date for this list.')


                                list = List(name=name, priority=priority, assigned_to=assigned_to,created_by=request.user, due_date=due_date)
                                list.save()

                                return ok_json(data={'message':'You have successfully created a list','redirect_url': '/lists'})
                            else:
                                # for field in f.errors:
                                #     error = field + ": " + field.data[0]
                                #     break
                                return bad_json(extradata={'errors':f._errors})
                    except Exception as ex:
                        return bad_json(message=ex.__str__())

            if action == 'edit':
                try:
                    with transaction.atomic():
                        f = ListForm(request.POST)
                        if f.is_valid():
                            name = f.cleaned_data['name']
                            priority = f.cleaned_data['priority']
                            assigned_to = f.cleaned_data['assigned_to']
                            due_date = f.cleaned_data['due_date']
                            list=None

                            if 'id' in request.POST and request.POST['id'] != '':
                                if List.objects.filter(id=int(request.POST['id'])).exists():
                                    list = List.objects.get(id=int(request.POST['id']))

                            if not list:
                                return bad_json(message='Please select a list to edit.')

                            if not name:
                                return bad_json(message='Please enter a list name.')

                            if not priority:
                                return bad_json(message='Please select a priority.')

                            if not assigned_to:
                                return bad_json(message='Please select a user to assign this list.')

                            if not due_date:
                                return bad_json(message='Please select a due date for this list.')


                            list.name = name
                            list.priority = priority
                            list.assigned_to = assigned_to
                            list.due_date = due_date
                            list.save()

                            return ok_json(data={'message':'You have successfully edited a list','redirect_url': '/lists'})
                        else:
                            return bad_json(extradata={'errors':f._errors})
                except Exception as ex:
                    return bad_json(message=ex.__str__())

            if action == 'add_task':
                try:
                    with transaction.atomic():
                        f = TaskForm(request.POST)
                        if f.is_valid():
                            title = f.cleaned_data['title']
                            priority = f.cleaned_data['priority']
                            assigned_to = f.cleaned_data['assigned_to']
                            due_date = f.cleaned_data['due_date']
                            note = f.cleaned_data['note']
                            list = None

                            if 'id' in request.POST and request.POST['id'] != '':
                                if List.objects.filter(id=int(request.POST['id'])).exists():
                                    list = List.objects.get(id=int(request.POST['id']))

                            if not list:
                                return bad_json(message='Please select a list to add this task to.')

                            if not title:
                                return bad_json(message='Please enter a task title.')

                            if not priority:
                                return bad_json(message='Please select a priority.')

                            if not assigned_to:
                                return bad_json(message='Please select a user to assign this task to.')

                            if not due_date:
                                return bad_json(message='Please select a due date for this task.')

                            if not note:
                                return bad_json(message='Please enter a note for this task.')

                            task = Task(list=list,title=title, priority=priority, assigned_to=assigned_to,created_by=request.user, due_date=due_date, note=note)
                            task.save()

                            return ok_json(data={'message':'You have successfully added a task','redirect_url': '/lists?action=view&id={}'.format(list.id)})
                        else:
                            # for field in f.errors:
                            #     error = field + ": " + field.data[0]
                            #     break
                            return bad_json(extradata={'errors':f._errors})
                except Exception as ex:
                    return bad_json(message=ex.__str__())

            if action == 'edit_task':
                try:
                    with transaction.atomic():
                        f = TaskForm(request.POST)
                        if f.is_valid():
                            title = f.cleaned_data['title']
                            priority = f.cleaned_data['priority']
                            assigned_to = f.cleaned_data['assigned_to']
                            due_date = f.cleaned_data['due_date']
                            note = f.cleaned_data['note']
                            task = None

                            if 'id' in request.POST and request.POST['id'] != '':
                                if Task.objects.filter(id=int(request.POST['id'])).exists():
                                    task = Task.objects.get(id=int(request.POST['id']))

                            if not task:
                                return bad_json(message='Please select a task to edit.')

                            if not title:
                                return bad_json(message='Please enter a task title.')

                            if not priority:
                                return bad_json(message='Please select a priority.')

                            if not assigned_to:
                                return bad_json(message='Please select a user to assign this task to.')

                            if not due_date:
                                return bad_json(message='Please select a due date for this task.')

                            if not note:
                                return bad_json(message='Please enter a note for this task.')

                            task.title = title
                            task.priority = priority
                            task.assigned_to = assigned_to
                            task.due_date = due_date
                            task.note = note
                            task.save()

                            return ok_json(data={'message':'You have successfully edited a task','redirect_url': '/lists?action=view&id={}'.format(task.list.id)})
                        else:
                            # for field in f.errors:
                            #     error = field + ": " + field.data[0]
                            #     break
                            return bad_json(extradata={'errors':f._errors})
                except Exception as ex:
                    return bad_json(message=ex.__str__())

            if action == 'add_comment':
                try:
                    with transaction.atomic():
                        f = CommentForm(request.POST)
                        if f.is_valid():
                            body = f.cleaned_data['body']
                            task = None

                            if 'id' in request.POST and request.POST['id'] != '':
                                if Task.objects.filter(id=int(request.POST['id'])).exists():
                                    task = Task.objects.get(id=int(request.POST['id']))

                            if not task:
                                return bad_json(message='Please select a task to add this comment to.')

                            if not body:
                                return bad_json(message='Please enter a comment for this task.')

                            comment = Comment(task=task,author=User.objects.get(id=request.user.id),body=body)
                            comment.save()

                            return ok_json(data={'message':'You have successfully added a comment','redirect_url': '/lists?action=view_task&id={}'.format(task.id)})
                        else:
                            return bad_json(extradata={'errors':f._errors})
                except Exception as ex:
                    return bad_json(message=ex.__str__())

    else:
        if 'action' in request.GET:
            if 'action' in request.GET and request.GET['action']  != '':
                action = request.GET['action']

                if action == 'create':
                    data['title'] = 'Create a new List'
                    data['form'] = ListForm()
                    return render(request, 'lists/create.html', data)

                if action == 'edit':
                    if 'id' in request.GET and request.GET['id'] != '':
                        if List.objects.filter(id=int(request.GET['id'])).exists():
                            data['list'] = list = List.objects.get(id=int(request.GET['id']))
                            data['title'] = 'Edit List: ' + list.name
                            data['form'] = ListForm(initial={'name':list.name,
                                                             'priority':list.priority,
                                                             'assigned_to':list.assigned_to,
                                                             'due_date':list.due_date})

                            return render(request, 'lists/edit.html', data)

                if action == 'view':
                    if 'id' in request.GET and request.GET['id'] != '':
                        if List.objects.filter(id=int(request.GET['id'])).exists():
                            data['list'] = list = List.objects.get(id=int(request.GET['id']))



                            data['title'] = 'Viewing List: ' + list.name
                            return render(request, 'lists/view.html', data)

                if action == 'add_task':
                    if 'id' in request.GET and request.GET['id'] != '':
                        if List.objects.filter(id=int(request.GET['id'])).exists():
                            data['list'] = list = List.objects.get(id=int(request.GET['id']))
                            data['title'] = 'Add Task to: ' + list.name
                            data['form'] = TaskForm()
                    return render(request, 'tasks/create.html', data)

                if action == 'edit_task':
                    if 'id' in request.GET and request.GET['id'] != '':
                        if Task.objects.filter(id=int(request.GET['id'])).exists():
                            data['task'] = task = Task.objects.get(id=int(request.GET['id']))
                            data['title'] = 'Edit Task for: ' + task.list.name
                            data['form'] = TaskForm(initial={'title':task.title,
                                                             'due_date':task.due_date,
                                                             'assigned_to':task.assigned_to,
                                                             'note':task.note,
                                                             'priority':task.priority})

                    return render(request, 'tasks/edit.html', data)

                if action == 'mark_complete_task':
                    if 'id' in request.GET and request.GET['id'] != '':
                        if Task.objects.filter(id=int(request.GET['id'])).exists():
                            task = Task.objects.get(id=int(request.GET['id']))
                            task.completed = True
                            task.save()
                            return HttpResponseRedirect('/lists?action=view&id={}'.format(task.list.id))
                    return HttpResponseRedirect('/lists')

                if action == 'mark_incomplete_task':
                    if 'id' in request.GET and request.GET['id'] != '':
                        if Task.objects.filter(id=int(request.GET['id'])).exists():
                            task = Task.objects.get(id=int(request.GET['id']))
                            task.completed = False
                            task.save()
                            return HttpResponseRedirect('/lists?action=view&id={}'.format(task.list.id))
                    return HttpResponseRedirect('/lists')

                if action == 'delete_task':
                    if 'id' in request.GET and request.GET['id'] != '':
                        if Task.objects.filter(id=int(request.GET['id'])).exists():
                            task = Task.objects.get(id=int(request.GET['id']))
                            list = task.list
                            task.delete()
                            return HttpResponseRedirect('/lists?action=view&id={}'.format(list.id))
                    return HttpResponseRedirect('/lists')

                if action == 'delete':
                    if 'id' in request.GET and request.GET['id'] != '':
                        if List.objects.filter(id=int(request.GET['id'])).exists():
                            list = List.objects.get(id=int(request.GET['id']))
                            list.delete()
                    return HttpResponseRedirect('/lists')

                if action == 'view_task':
                    if 'id' in request.GET and request.GET['id'] != '':
                        if Task.objects.filter(id=int(request.GET['id'])).exists():
                            data['task'] = task = Task.objects.get(id=int(request.GET['id']))



                            data['title'] = 'Viewing Task: ' + task.title
                            return render(request, 'tasks/view.html', data)

                if action == 'add_comment':
                    if 'id' in request.GET and request.GET['id'] != '':
                        if Task.objects.filter(id=int(request.GET['id'])).exists():
                            data['task'] = task = Task.objects.get(id=int(request.GET['id']))
                            data['form'] = CommentForm()


                            data['title'] = 'Comment on Task: ' + task.title
                            return render(request, 'comment/create.html', data)

    data['lists'] = List.objects.all()
    return render(request, 'lists.html', data)