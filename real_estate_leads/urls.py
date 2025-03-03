"""
URL configuration for real_estate_leads project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from leads import views  
from leads.views import ai_match_lead

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path("lead/<uuid:id>/ai-match/", ai_match_lead, name="ai_match_lead"),



    # Lead management
    path('leads/', views.lead_list, name='lead_list'), 
    path('add_lead/', views.add_lead, name='add_lead'),
    path('leads/<uuid:id>/', views.lead_detail, name='lead_detail'),
    path('lead/update/<uuid:id>/', views.update_lead, name='update-lead'),
    path('lead/delete/<uuid:id>/', views.delete_lead, name='delete-lead'),
    path('update-lead/<uuid:id>/', views.update_lead, name='update_lead'),
    path('download-leads/', views.download_leads_excel, name='download_leads_excel'),
]
