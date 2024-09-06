from aidiet import urls
from home import views
from django.contrib import admin
from django.urls import path

urlpatterns = [
    # path('admin/', admin.site.urls),
   path("", views.signup, name='signup'),
    path("login/", views.login, name='login'),
    path("login/process/", views.process_login, name='process'),
    path("home/", views.home, name='home'),
    path("home/AddNewBook/",views.AddNewBook,name="AddNewBook"),
    path('mark_as_completed/<book_id>/',views.MarkAsCompleted,name="MarkAsCompleted"),
    path('home/Recommend/',views.Recommended,name="Recommended")
    # url(r'^fitbit/', include('fitapp.urls')),
]
