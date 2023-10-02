"""
URL configuration for TRANSIMIS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from TRANSMIS import views
from TRANSMIS.views import group_list, group_create, SEMCMentoringCoaching

urlpatterns = [
    path('', group_list, name='group_list'), 
    path('admin/', admin.site.urls),
    path('groups/', group_list, name='group_list'),
    path('groups/<int:pk>/', views.group_detail, name='group_detail'),
    path('groups/create/', views.group_create, name='group_create'),
    path('groups/<int:pk>/update/', views.group_update, name='group_update'),
    path('groups/<int:pk>/delete/', views.group_delete, name='group_delete'),
    
    path('beneficiaries/', views.beneficiary_list, name='beneficiary_list'),
    path('beneficiaries/<int:pk>/', views.beneficiary_detail, name='beneficiary_detail'),
    path('beneficiaries/create/<int:pk>/', views.beneficiary_create, name='beneficiary_create'),
    path('beneficiaries/<int:pk>/update/', views.beneficiary_update, name='beneficiary_update'),
    path('beneficiaries/<int:pk>/delete/', views.beneficiary_delete, name='beneficiary_delete'),

    path('beneficiaries/<int:pk>/semc_mentoring_coaching/create/', views.semc_mentoring_coaching_create, name='semc_mentoring_coaching_create'),
    path('semc_mentoring_coaching/<int:pk>/update/', views.semc_mentoring_coaching_update, name='semc_mentoring_coaching_update'),
    path('semc_mentoring_coaching/<int:pk>/delete/', views.semc_mentoring_coaching_delete, name='semc_mentoring_coaching_delete'),


    path('beneficiaries/<int:pk>/semccommunityparticipation/create/', views.semccommunityparticipation_create, name='semccommunityparticipation_create'),
    path('semccommunityparticipation/<int:pk>/update/', views.semccommunityparticipation_update, name='semccommunityparticipation_update'),
    path('semccommunityparticipation/<int:pk>/delete/', views.semccommunityparticipation_delete, name='semccommunityparticipation_delete'),

    path('beneficiaries/<int:pk>/semcsbcc/create/', views.semcsbcc_create, name='semcsbcc_create'),
    path('semcsbcc/<int:pk>/update/', views.semcsbcc_update, name='semcsbcc_update'),
    path('semcsbcc/<int:pk>/delete/', views.semcsbcc_delete, name='semcsbcc_delete'),

    path('beneficiaries/<int:pk>/spgfa/create/', views.spgfa_create, name='spgfa_create'),
    path('spgfa/<int:pk>/update/', views.spgfa_update, name='spgfa_update'),
    path('spgfa/<int:pk>/delete/', views.spgfa_delete, name='spgfa_delete'),

    path('beneficiaries/<int:pk>/spnutricash/create/', views.spnutricash_create, name='spnutricash_create'),
    path('spnutricash/<int:pk>/update/', views.spnutricash_update, name='spnutricash_update'),
    path('spnutricash/<int:pk>/delete/', views.spnutricash_delete, name='spnutricash_delete'),

    path('beneficiaries/<int:pk>/spsage/create/', views.spsage_create, name='spsage_create'),
    path('spsage/<int:pk>/update/', views.spsage_update, name='spsage_update'),
    path('spsage/<int:pk>/delete/', views.spsage_delete, name='spsage_delete'),

    path('beneficiaries/<int:pk>/lpdonfarm/create/', views.lpdonfarm_create, name='lpdonfarm_create'),
    path('lpdonfarm/<int:pk>/update/', views.lpdonfarm_update, name='lpdonfarm_update'),
    path('lpdonfarm/<int:pk>/delete/', views.lpdonfarm_delete, name='lpdonfarm_delete'),

    path('beneficiaries/<int:pk>/lpdofffarm/create/', views.lpdofffarm_create, name='lpdofffarm_create'),
    path('lpdofffarm/<int:pk>/update/', views.lpdofffarm_update, name='lpdofffarm_update'),
    path('lpdofffarm/<int:pk>/delete/', views.lpdofffarm_delete, name='lpdofffarm_delete'),

    path('beneficiaries/<int:pk>/lpdnonfarm/create/', views.lpdnonfarm_create, name='lpdnonfarm_create'),
    path('lpdnonfarm/<int:pk>/update/', views.lpdnonfarm_update, name='lpdnonfarm_update'),
    path('lpdnonfarm/<int:pk>/delete/', views.lpdnonfarm_delete, name='lpdnonfarm_delete'),

    path('beneficiaries/<int:pk>/dfi/create/', views.dfi_create, name='dfi_create'),
    path('dfi/<int:pk>/update/', views.dfi_update, name='dfi_update'),
    path('dfi/<int:pk>/delete/', views.dfi_delete, name='dfi_delete'),


]

