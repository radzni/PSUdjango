from django.shortcuts import render
from typing import Any
from django.db.models.query import QuerySet 
from django.db.models import Q

from django.views.generic.list import ListView  
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from studentorg.models import Organization, Student, OrgMember, College, Program  
from studentorg.forms import OrganizationForm, StudentForm, OrgMemberForm, CollegeForm, ProgramForm

from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from django.db import connection  
from django.http import JsonResponse  
from django.db.models.functions import ExtractMonth  

from django.db.models import *
from django.db.models.functions import TruncYear
from django.db.models import Count  
from datetime import datetime 


@method_decorator(login_required, name='dispatch')

class HomePageView(ListView):  
    model = Organization
    context_object_name = 'home'  
    template_name = "home.html"

class ChartView(ListView):  
    template_name = 'chart.html'  

    def get_context_data(self, **kwargs):  
        context = super().get_context_data(**kwargs)  
        return context  
    
    def get_queryset(self, *args, **kwargs):  
        pass  

def ChartDashboardView(request):
    return render(request, 'chart.html')

def StudentViewByProg(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT p.prog_name, COUNT(s.id) as student_count
            FROM studentorg_program p
            LEFT JOIN studentorg_student s ON s.program_id = p.id
            GROUP BY p.prog_name
        """)
        data = cursor.fetchall()

    response_data = [{"prog_name": row[0], "student_count": row[1]} for row in data]
    return JsonResponse(response_data, safe=False)


def StudentViewByOrg(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT o.name, COUNT(DISTINCT om.id)
            FROM studentorg_organization o
            LEFT JOIN studentorg_orgmember om ON om.organization_id = o.id
            GROUP BY o.id
        """)
        data = cursor.fetchall()

    response_data = [{"name": row[0], "student_count": row[1]} for row in data]
    return JsonResponse(response_data, safe=False)


def GetOrgMembersPerYear(request):
    members_per_year = OrgMember.objects.annotate(year=TruncYear('date_joined')) \
                                 .values('year') \
                                 .annotate(count=Count('id')) \
                                 .order_by('year') \
                                 .values('year', 'count')

    data = list(members_per_year)
    return JsonResponse(data, safe=False)


def StudentCountByCollegeView(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT c.college_name, COUNT(s.id) AS student_count
            FROM studentorg_college c
            LEFT JOIN studentorg_program p ON p.college_id = c.id
            LEFT JOIN studentorg_student s ON s.program_id = p.id
            GROUP BY c.college_name
        """)
        data = cursor.fetchall()

    response_data = [{"college_name": row[0], "student_count": row[1]} for row in data]
    return JsonResponse(response_data, safe=False)

def OrganizationCountByCollegeView(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT c.college_name, COUNT(o.id) as org_count
            FROM studentorg_college c
            LEFT JOIN studentorg_organization o ON o.college_id = c.id
            GROUP BY c.college_name
        """)
        data = cursor.fetchall()
    
    response_data = [{"college_name": row[0], "org_count": row[1]} for row in data]
    return JsonResponse(response_data, safe=False)

#########################################################################################################

class OrganizationDeleteView(DeleteView):  
    model = Organization  
    template_name = 'org_del.html'  
    success_url = reverse_lazy('organization-list')  

class StudentDeleteView(DeleteView):  
    model = Student  
    template_name = 'student_del.html'  
    success_url = reverse_lazy('student-list')

class OrgaMemberDeleteView(DeleteView):  
    model = OrgMember  
    template_name = 'orgmember_del.html'  
    success_url = reverse_lazy('orgmember-list')

class CollegeDeleteView(DeleteView):  
    model = College  
    template_name = 'college_del.html'  
    success_url = reverse_lazy('college-list')

class ProgramDeleteView(DeleteView):  
    model = Program  
    template_name = 'program_del.html'  
    success_url = reverse_lazy('program-list')



class OrganizationUpdateView(UpdateView):  
    model = Organization  
    form_class = OrganizationForm  
    template_name = 'org_edit.html'  
    success_url = reverse_lazy('organization-list')  

class StudentUpdateView(UpdateView):  
    model = Student  
    form_class = StudentForm  
    template_name = 'student_edit.html'  
    success_url = reverse_lazy('student-list')

class OrgaMemberUpdateView(UpdateView):  
    model = OrgMember  
    form_class = OrgMemberForm  
    template_name = 'orgmember_edit.html'  
    success_url = reverse_lazy('orgmember-list')

class CollegeUpdateView(UpdateView):  
    model = College  
    form_class = CollegeForm  
    template_name = 'college_edit.html'  
    success_url = reverse_lazy('college-list')

class ProgramUpdateView(UpdateView):  
    model = Program  
    form_class = ProgramForm  
    template_name = 'program_edit.html'  
    success_url = reverse_lazy('program-list')



class OrganizationCreateView(CreateView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'org_add.html'
    success_url = reverse_lazy('organization-list')

class StudentCreateView(CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'student_add.html'
    success_url = reverse_lazy('student-list')

class OrgaMemberCreateView(CreateView):
    model = OrgMember
    form_class = OrgMemberForm
    template_name = 'orgmember_add.html'
    success_url = reverse_lazy('orgmember-list')

class CollegeCreateView(CreateView):
    model = College
    form_class = CollegeForm
    template_name = 'college_add.html'
    success_url = reverse_lazy('college-list')

class ProgramCreateView(CreateView):
    model = Program
    form_class = ProgramForm
    template_name = 'program_add.html'
    success_url = reverse_lazy('program-list')


class OrganizationList(ListView):  
    model = Organization  
    context_object_name = 'organization'  
    template_name = "org_list.html"
    paginate_by = 15  
    def get_queryset(self, *args, **kwargs):
        qs = super(OrganizationList, self).get_queryset(*args, **kwargs)
        if self.request.GET.get("q") is not None:
            query = self.request.GET.get('q')
            qs = qs.filter(Q(name__icontains=query) | Q(description__icontains=query))
        return qs

class StudentList(ListView):  
    model = Student  
    context_object_name = 'student'  
    template_name = "student_list.html"
    paginate_by = 15  
    def get_queryset(self, *args, **kwargs):
        qs = super(StudentList, self).get_queryset(*args, **kwargs)
        if self.request.GET.get("q") is not None:
            query = self.request.GET.get('q')
            qs = qs.filter(
                Q(firstname__icontains=query) | 
                Q(lastname__icontains=query) |
                Q(student_id__icontains=query)
            )
        return qs


class OrgaMemberList(ListView):  
    model = OrgMember  
    context_object_name = 'orgmember'  
    template_name = "orgmember_list.html"
    paginate_by = 15
    def get_queryset(self, *args, **kwargs):
        qs = super(OrgaMemberList, self).get_queryset(*args, **kwargs)
        if self.request.GET.get("q"):
            query = self.request.GET.get('q')
            qs = qs.filter(
                Q(student__firstname__icontains=query) |
                Q(student__lastname__icontains=query) |
                Q(organization__name__icontains=query) |
                Q(date_joined__icontains=query)  # If you want to search by date
            )
        return qs

class CollegeList(ListView):
    model = College  
    context_object_name = 'college'  
    template_name = "college_list.html"
    paginate_by = 15
    def get_queryset(self, *args, **kwargs):
        qs = super(CollegeList, self).get_queryset(*args, **kwargs)
        if self.request.GET.get("q") is not None:
            query = self.request.GET.get('q')
            qs = qs.filter(Q(college_name__icontains=query)) 
        return qs

class ProgramList(ListView):
    model = Program  
    context_object_name = 'program'  
    template_name = "program_list.html"
    paginate_by = 15
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)  # More Pythonic super() call
        query = self.request.GET.get("q")
        
        if query:
            qs = qs.filter(
                Q(prog_name__icontains=query) | 
                Q(college__college_name__icontains=query)  # Adjusted field reference
            ).distinct()
        return qs


# Create your views here.
