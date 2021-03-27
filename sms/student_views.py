import json
import math
from datetime import datetime

from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import (HttpResponseRedirect, get_object_or_404,
                              redirect, render)
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from django.views.generic import ListView, DetailView, DetailView

from .forms import *
from .models import *


def student_home(request):
    receipts = Receipt.objects.filter()
    invoice = Invoice.objects.filter()
    student = get_object_or_404(Student, admin=request.user)
    total_subject = Subject.objects.filter(course=student.course).count()
    subjects = Subject.objects.filter(course=student.course)
    context = {
        'receipts':receipts,
        'invoice':invoice,
        'total_subject': total_subject,
        'subjects': subjects,
        'page_title': 'Student Homepage'

    }
    return render(request, 'student_template/home_content.html', context)


@ csrf_exempt
def student_view_attendance(request):
    student = get_object_or_404(Student, admin=request.user)
    if request.method != 'POST':
        course = get_object_or_404(Course, id=student.course.id)
        context = {
            'subjects': Subject.objects.filter(course=course),
            'page_title': 'View Attendance'
        }
        return render(request, 'student_template/student_view_attendance.html', context)
    else:
        subject_id = request.POST.get('subject')
        start = request.POST.get('start_date')
        end = request.POST.get('end_date')
        try:
            subject = get_object_or_404(Subject, id=subject_id)
            start_date = datetime.strptime(start, "%Y-%m-%d")
            end_date = datetime.strptime(end, "%Y-%m-%d")
            attendance = Attendance.objects.filter(
                date__range=(start_date, end_date), subject=subject)
            attendance_reports = AttendanceReport.objects.filter(
                attendance__in=attendance, student=student)
            json_data = []
            for report in attendance_reports:
                data = {
                    "date":  str(report.attendance.date),
                    "status": report.status
                }
                json_data.append(data)
            return JsonResponse(json.dumps(json_data), safe=False)
        except Exception as e:
            return None



def student_view_result(request):
    student = get_object_or_404(Student, admin=request.user)
    results = StudentResult.objects.filter(student=student)
    context = {
        'results': results,
        'page_title': "View Result"
    }
    return render(request, "student_template/student_view_result.html", context)



def student_view_receipt(request):
    student = get_object_or_404(Student, admin=request.user)
    receipts = Receipt.objects.filter(student=student)
    context = {
        'receipts': receipts,
        'page_title': "View Receipt"
    }
    return render(request, "student_template/student_view_receipt.html", context)



def student_view_invoice(request):
    student = get_object_or_404(Student, admin=request.user)
    invoices = Invoice.objects.filter(student=student)
    context = {
        'invoices': invoices,
        'page_title': "invoice"
    }
    return render(request,"student_template/student_view_invoice.html", context)


def student_view_profile(request):
    student = get_object_or_404(Student, admin=request.user)
    form = StudentEditForm(request.POST or None, request.FILES or None,
                           instance=student)
    context = {'form': form,
               'page_title': 'View/Edit Profile'
               }
    if request.method == 'POST':
        try:
            if form.is_valid():
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                password = form.cleaned_data.get('password') or None
                address = form.cleaned_data.get('address')
                gender = form.cleaned_data.get('gender')
                passport = request.FILES.get('profile_pic') or None
                admin = student.admin
                if password != None:
                    admin.set_password(password)
                if passport != None:
                    fs = FileSystemStorage()
                    filename = fs.save(passport.name, passport)
                    passport_url = fs.url(filename)
                    admin.profile_pic = passport_url
                admin.first_name = first_name
                admin.last_name = last_name
                admin.address = address
                admin.gender = gender
                admin.save()
                student.save()
                messages.success(request, "Profile Updated!")
                return redirect(reverse('student_view_profile'))
            else:
                messages.error(request, "Invalid Data Provided")
        except Exception as e:
            messages.error(request, "Error Occured While Updating Profile " + str(e))

    return render(request, "student_template/student_view_profile.html", context)


@csrf_exempt
def student_fcmtoken(request):
    token = request.POST.get('token')
    student_user = get_object_or_404(CustomUser, id=request.user.id)
    try:
        student_user.fcm_token = token
        student_user.save()
        return HttpResponse("True")
    except Exception as e:
        return HttpResponse("False")
    
    
    
    
class InvoiceDetailVie(DetailView):
    model = Invoice
    fields = '__all__'
    template_name = 'invoice_details.html'

    def get_context_data(self, **kwargs):
        context = super(InvoiceDetailVie, self).get_context_data(**kwargs)
        context['receipts'] = Receipt.objects.filter(invoice=self.object)
        context['items'] = InvoiceItem.objects.filter(invoice=self.object)
        return context
    
    
class ReceiptDetailView(DetailView):
    model = Receipt
    fields = '__all__'
    template_name = 'invoice_details.html'

    def get_context_data(self, **kwargs):
        context = super(InvoiceDetailVie, self).get_context_data(**kwargs)
        context['receipts'] = Receipt.objects.filter(invoice=self.object)
        context['page_title'] = 'student'
        return context
    
    
    
    
def student_list(request):
    students = Student.objects.all()
    return render(request, 'student_template/student_list.html', {"students":students})











