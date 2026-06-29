from django.urls import path, include
from . import views
urlpatterns = [
     #path('',views.home_fun,name='home'),
     path('',views.login_fun,name='login'),
     path('register/',views.register_fun,name='register'),
     path('logout/',views.logout_fun,name='logout'),
     path('home/',views.home_fun,name='home'),
     path('add_task/',views.add_task_fun,name='add_task'),
     path('display_all_tasks/',views.display_all_tasks_fun,name='display_all_tasks'),
     path('edit_task/<int:task_id>/',views.edit_task_fun,name='edit_task'),
     path('delete_task/<int:task_id>/',views.delete_task_fun,name='delete_task'),
     path('qr_code/<int:task_id>/',views.qr_code_fun,name='qr_code'),
]