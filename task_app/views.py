from django.shortcuts import render,redirect
from .models import Task
from .forms import Createnewuser_form
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required 

# Create your views here.
############################RegisterStart################################
def register_fun(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        form_reg=Createnewuser_form()
        if request.method=="POST":
            form_reg=Createnewuser_form(request.POST)
            if form_reg.is_valid():
                user=form_reg.save()
                username=form_reg.cleaned_data.get('username') or user.username
                group=Group.objects.get(name='user')
                user.groups.add(group)
                messages.success(request,f'{username} Created Successfully')
                return redirect('/')
    context={'form_reg_key':form_reg}  
    return render(request,'pages/register.html',context)
#%%%%%%%%%%%%%%%%%%%%%%%$$$$RegisterEnd$$$$%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#

#%%%%%%%%%%%%%%%%%%%%%%%$$$$$$$$%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#
#---------------------------LoginStart--------------------------------#
def login_fun(request):
    if request.user.is_authenticated:
        return redirect('/home')
    else:
        username=request.POST.get("usernamehtml")
        password=request.POST.get("passwordhtml")
        user=authenticate(request,username=username,password=password)
        if user:
            login(request,user)
            return redirect('/home')
        else:
            messages.info(request,'Username or Password is incorrect')

    context={}  
    return render(request,'pages/login.html',context)
#-------------------_______%LoginEnd%_______------------------------#
############################################################

############################################################
#---------------------------LogoutStart--------------------------------#
def logout_fun(request):
    logout(request)
    return redirect('/')
#-------------------_______%LogoutEnd%_______------------------------#
###########################################################

@login_required(login_url='/')
def home_fun(request):
    return render(request,'pages/home.html')
#-------------------$$$_______%CRUD%_______$$$------------------------#
#$$$$$_____%%%%%_____########################_____%%%%%_____$$$$$#
#-------------------_______%Add_New_Task%_______------------------------#
###########################################################
def add_task_fun(request):
    if request.method=="POST":
        title=request.POST.get('titlehtml')
        description=request.POST.get('descriptionhtml')
        status=request.POST.get('statushtml')
        date_completed=request.POST.get('date_completedhtml')
        Task.objects.create(user=request.user,title=title,description=description,status=status,date_completed=date_completed)
        messages.success(request,'Task Added Successfully')
        return redirect('/home')
    return render(request,'pages/add_task.html')
###########################################################
#-------------------_______%display_all_tasks%_______------------------------#
###########################################################
def display_all_tasks_fun(request):
    tasks=Task.objects.filter(user=request.user)
    context={'all_tasks_key':tasks}
    return render(request,'pages/display_all_tasks.html',context)
#-------------------_______%Edit_Task%_______------------------------#
###########################################################
def edit_task_fun(request,task_id):
    task=Task.objects.get(id=task_id)
    if request.method=="POST":
        task.title=request.POST.get('titlehtml')
        task.description=request.POST.get('descriptionhtml')
        task.status=request.POST.get('statushtml')
        task.date_completed=request.POST.get('date_completedhtml')
        task.save()
        messages.success(request,'Task Updated Successfully')
        return redirect('/display_all_tasks')
    context={'edit_task_key':task}
    return render(request,'pages/edit_task.html',context)
#-------------------_______%Delete_Task%_______------------------------#
###########################################################
def delete_task_fun(request,task_id):
    task=Task.objects.get(id=task_id)
    if request.method=="POST":
        task.delete()
        return redirect('/display_all_tasks')
    messages.success(request,'Task Deleted Successfully')
    return render(request,'pages/delete_task.html')
#-------------------_______%qr_code%_______------------------------#
###########################################################
def qr_code_fun(request,task_id):
    task=Task.objects.get(id=task_id)
    context={'qr_code_key':task}
    return render(request,'pages/qr_code.html',context)
