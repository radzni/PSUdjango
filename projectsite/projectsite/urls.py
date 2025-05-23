"""
URL configuration for projectsite project.

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
from django.urls import path, re_path
from studentorg import views  
from django.contrib.auth import views as auth_views
from studentorg.views import (
    HomePageView, OrganizationList, OrganizationCreateView, 
    OrganizationUpdateView, OrganizationDeleteView, CollegeList, 
    CollegeCreateView, CollegeUpdateView, CollegeDeleteView, StudentList, 
    StudentCreateView, StudentUpdateView, StudentDeleteView, ProgramList, 
    ProgramCreateView, ProgramUpdateView, ProgramDeleteView, OrgaMemberList, 
    OrgaMemberCreateView, OrgaMemberUpdateView, OrgaMemberDeleteView, ChartView,
    GetOrgMembersPerYear, StudentViewByOrg, StudentViewByProg, OrganizationCountByCollegeView, StudentCountByCollegeView
)



urlpatterns = [  
    path("admin/", admin.site.urls),  
    path('', HomePageView.as_view(), name="home"),

    path('charts/', ChartView.as_view(), name='charts'),
    path('student_count_by_program/', StudentViewByProg, name='student_count_by_program'),
    path('student-distribution-by-organization/', StudentViewByOrg, name='student_distribution_by_organization'),
    path('org-members-per-year/', GetOrgMembersPerYear, name='org_members_per_year'),
    path('organization_count_by_college/', OrganizationCountByCollegeView, name='organization_count_by_college'),
    path('student_count_by_college/', StudentCountByCollegeView, name='student_count_by_college'),

    

    path('organization_list', OrganizationList.as_view(), name='organization-list'),
    path('organization_list/add', OrganizationCreateView.as_view(), name='organization-add'),
    path('organization_list/<pk>', OrganizationUpdateView.as_view(), name='organization-update'),
    path('organization_list/<pk>/delete', OrganizationDeleteView.as_view(), name='organization-delete'),
    
    path('student_list', StudentList.as_view(), name='student-list'),
    path('student_list/add', StudentCreateView.as_view(), name='student-add'),
    path('student_list/<pk>', StudentUpdateView.as_view(), name='student-update'),
    path('student_list/<pk>/delete', StudentDeleteView.as_view(), name='student-delete'),

    path('orgmember_list', OrgaMemberList.as_view(), name='orgmember-list'),
    path('orgmember_list/add', OrgaMemberCreateView.as_view(), name='orgmember-add'),
    path('orgmember_list/<pk>', OrgaMemberUpdateView.as_view(), name='orgmember-update'),
    path('orgmember_list/<pk>/delete', OrgaMemberDeleteView.as_view(), name='orgmember-delete'),

    path('college_list', CollegeList.as_view(), name='college-list'),
    path('college_list/add', CollegeCreateView.as_view(), name='college-add'),
    path('college_list/<pk>', CollegeUpdateView.as_view(), name='college-update'),
    path('college_list/<pk>/delete', CollegeDeleteView.as_view(), name='college-delete'),

    path('program_list', ProgramList.as_view(), name='program-list'),
    path('program_list/add', ProgramCreateView.as_view(), name='program-add'),
    path('program_list/<pk>', ProgramUpdateView.as_view(), name='program-update'),
    path('program_list/<pk>/delete', ProgramDeleteView.as_view(), name='program-delete'),
    re_path(r'^login/$', auth_views.LoginView.as_view(  
        template_name='login.html'), name='login'),  
    re_path(r'^logout$', auth_views.LogoutView.as_view(), name='logout'),  
]  
