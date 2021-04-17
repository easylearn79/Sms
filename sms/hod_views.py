import json
import requests
import csv
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.shortcuts import (HttpResponse,
                              get_object_or_404, redirect, render)
from django.templatetags.static import static
from django.views.decorators.csrf import csrf_exempt

from .forms import *
from .form import *
from .models import Invoice

from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.messages.views import SuccessMessageMixin

from .forms import AcademicTermForm, AcademicSessionForm, SubjectForm, CurrentSessionForm


def manage_student(request):
    students = CustomUser.objects.filter(user_type=3)
    context = {
        'students': students,
        'page_title': 'Manage Students'
    }
    return render(request, "hod_template/manage_student.html", context)


def error_404_view(request):
    return render(request, 'hod_template/404.html')


class StaffListView(ListView):
    model = Staff
    template_name = 'staff_template/home_content.html',


class LecturerListView(ListView):
    model = Lecturer
    template_name = 'lecturer_template/home_content.html',


class StudentDeleteView(DeleteView):
    model = CustomUser
    success_url = reverse_lazy('manage_student')
    template_name = "corecode/student_confirm_delete.html"


class LecturerDetailView(DetailView):
    model = CustomUser
    template_name = "lecturer_template/lecturer_details.html"

    def get_context_data(self, **kwargs):
        context = super(LecturerDetailView, self).get_context_data(**kwargs)
        return context


class LecturerDeleteView(DeleteView):
    model = CustomUser
    success_url = reverse_lazy('manage_lecturer')
    template_name = "lecturer_template/lecturer_confirm_delete.html"


class StudentDetailView(DetailView):
    model = CustomUser
    template_name = "student_template/student_detail.html"

    def get_context_data(self, **kwargs):
        context = super(StudentDetailView, self).get_context_data(**kwargs)
        return context


def admin_home(request):
    total_staff = Staff.objects.all().count()
    total_lecturer = Lecturer.objects.all().count()
    students = CustomUser.objects.all()
    total_students = Student.objects.all().count()
    subjects = Subject.objects.all()
    total_subject = subjects.count()
    total_course = Course.objects.all().count()
    total_dept = Department.objects.all().count()
    attendance_list = []
    subject_list = []
    for subject in subjects:
        attendance_count = Attendance.objects.filter(subject=subject).count()
        subject_list.append(subject.name[:7])
        attendance_list.append(attendance_count)
    context = {
        'total_dept': total_dept,
        'page_title': "Administrative Dashboard",
        'total_students': total_students,
        'total_staff': total_staff,
        'total_lecturer': total_lecturer,
        'students': students,
        'total_course': total_course,
        'total_subject': total_subject,
        'subject_list': subject_list,
        'attendance_list': attendance_list

    }
    return render(request, 'hod_template/home_content.html', context)


def add_staff(request):
    form = StaffForm(request.POST or None, request.FILES or None)
    context = {'form': form, 'page_title': 'Add Staff'}
    if request.method == 'POST':
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            address = form.cleaned_data.get('address')
            email = form.cleaned_data.get('email')
            gender = form.cleaned_data.get('gender')
            password = form.cleaned_data.get('password')
            course = form.cleaned_data.get('course')
            passport = request.FILES.get('profile_pic')
            fs = FileSystemStorage()
            filename = fs.save(passport.name, passport)
            passport_url = fs.url(filename)
            try:
                user = CustomUser.objects.create_user(email=email, password=password, user_type=2,
                                                      first_name=first_name, last_name=last_name,
                                                      profile_pic=passport_url)
                user.gender = gender
                user.address = address
                user.staff.course = course
                user.save()
                messages.success(request, "Successfully Added")
                return redirect(reverse('add_staff'))

            except Exception as e:
                messages.error(request, "Could Not Add " + str(e))
        else:
            messages.error(request, "Please fulfil all requirements")

    return render(request, 'hod_template/add_staff_template.html', context)


def add_lecturer(request):
    form = LecturerForm(request.POST or None, request.FILES or None)
    context = {'form': form, 'page_title': 'Add Lecturer'}
    if request.method == 'POST':
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            address = form.cleaned_data.get('address')
            email = form.cleaned_data.get('email')
            gender = form.cleaned_data.get('gender')
            password = form.cleaned_data.get('password')
            course = form.cleaned_data.get('course')
            passport = request.FILES.get('profile_pic')
            fs = FileSystemStorage()
            filename = fs.save(passport.name, passport)
            passport_url = fs.url(filename)
            try:
                user = CustomUser.objects.create_user(email=email, password=password, user_type=4,
                                                      first_name=first_name, last_name=last_name,
                                                      profile_pic=passport_url)
                user.gender = gender
                user.address = address
                user.lecturer.course = course
                user.save()
                messages.success(request, "Successfully Added")
                return redirect(reverse('add_lecturer'))

            except Exception as e:
                messages.error(request, "Could Not Add " + str(e))
        else:
            messages.error(request, "Please fulfil all requirements")

    return render(request, 'hod_template/add_lecturer_template.html', context)


def add_student(request):
    forms = StudentForm(request.POST or None, request.FILES or None)
    context = {'form': forms, 'page_title': 'Add Student'}
    if request.method == 'POST':
        if forms.is_valid():
            first_name = forms.cleaned_data.get('first_name')
            last_name = forms.cleaned_data.get('last_name')
            matric_no = forms.cleaned_data.get('matric_no')
            phone_no = forms.cleaned_data.get('phone_no')
            address = forms.cleaned_data.get('address')
            email = forms.cleaned_data.get('email')
            gender = forms.cleaned_data.get('gender')
            password = forms.cleaned_data.get('password')
            dept = forms.cleaned_data.get('dept')
            course = forms.cleaned_data.get('course')
            session = forms.cleaned_data.get('session')
            term = forms.cleaned_data.get('term')
            level = forms.cleaned_data.get('level')
            passport = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(passport.name, passport)
            passport_url = fs.url(filename)
            try:
                user = CustomUser.objects.create_user(email=email, password=password, user_type=3,
                                                      first_name=first_name, matric_no=matric_no, last_name=last_name,
                                                      profile_pic=passport_url, phone_no=phone_no)
                user.gender = gender
                user.phone_no = phone_no
                user.address = address
                user.student.session = session
                user.student.course = course
                user.student.dept = dept
                user.student.level = level
                user.student.term = term
                user.level = level
                user.save()
                messages.success(request, "Successfully Added")
                return redirect(reverse('add_student'))
            except Exception as e:
                messages.error(request, "Could Not Add: " + str(e))
        else:
            messages.error(request, "Could Not Add: ")
    return render(request, 'hod_template/add_student_template.html', context)


def add_dept(request):
    form = DepartmentForm(request.POST or None)
    context = {
        'form': form,
        'page_title': 'Add Department'
    }
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data.get('name')
            fees = form.cleaned_data.get('fees')
            collage = form.cleaned_data.get('collage')
            try:
                dept = Department()
                dept.name = name
                dept.fees = fees
                dept.collage = collage
                dept.save()
                messages.success(request, "Successfully Added")
                return redirect(reverse('add_dept'))
            except:
                messages.error(request, "Could Not Add")
        else:
            messages.error(request, "Could Not Add")
    return render(request, 'hod_template/add_dept.html', context)


def edit_dept(request, dept_id):
    instance = get_object_or_404(Department, id=dept_id)
    form = DepartmentForm(request.POST or None, instance=instance)
    context = {
        'form': form,
        'dept_id': dept_id,
        'page_title': 'Edit Department'
    }
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data.get('name')
            fees = form.cleaned_data.get('fees')
            collage = form.cleaned_data.get('collage')
            try:
                dept = Department.objects.get(id=dept_id)
                dept.name = name
                dept.fees = fees
                dept.collage = collage
                dept.save()
                messages.success(request, "Successfully Updated")
            except:
                messages.error(request, "Could Not Update")
        else:
            messages.error(request, "Could Not Update")

    return render(request, 'hod_template/edit_dept.html', context)


def add_level(request):
    form = LevelForm(request.POST or None)
    context = {
        'form': form,
        'page_title': 'Add Level'
    }
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data.get('name')
            try:
                level = Level()
                level.name = name
                level.save()
                messages.success(request, "Successfully Added")
                return redirect(reverse('add_level'))
            except:
                messages.error(request, "Could Not Add")
        else:
            messages.error(request, "Could Not Add")
    return render(request, 'hod_template/add_level.html', context)


def add_course(request):
    form = CourseForm(request.POST or None)
    context = {
        'form': form,
        'page_title': 'Add Course'
    }
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data.get('name')
            dept_info = form.cleaned_data.get('dept_info')
            level_info = form.cleaned_data.get('level_info')
            try:
                course = Course()
                course.name = name
                course.dept_info = dept_info
                course.level_info = level_info
                course.save()
                messages.success(request, "Successfully Added")
                return redirect(reverse('add_course'))
            except:
                messages.error(request, "Could Not Add")
        else:
            messages.error(request, "Could Not Add")
    return render(request, 'hod_template/add_course_template.html', context)


def add_subject(request):
    form = SubjectForm(request.POST or None)
    context = {
        'form': form,
        'page_title': 'Add Subject'
    }
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data.get('name')
            course = form.cleaned_data.get('course')
            staff = form.cleaned_data.get('staff')
            lecturer = form.cleaned_data.get('lecturer')
            try:
                subject = Subject()
                subject.name = name
                subject.staff = staff
                subject.lecturer = lecturer
                subject.course = course
                subject.save()
                messages.success(request, "Successfully Added")
                return redirect(reverse('add_subject'))

            except Exception as e:
                messages.error(request, "Could Not Add " + str(e))
        else:
            messages.error(request, "Fill Form Properly")

    return render(request, 'hod_template/add_subject_template.html', context)


def manage_staff(request):
    allStaff = CustomUser.objects.filter(user_type=2)
    context = {
        'allStaff': allStaff,
        'page_title': 'Manage Staff'
    }
    return render(request, "hod_template/manage_staff.html", context)


def manage_lecturer(request):
    allLecturer = CustomUser.objects.filter(user_type=4)
    context = {
        'allLecturer': allLecturer,
        'page_title': 'Manage Lecturer'
    }
    return render(request, "hod_template/manage_lecturer.html", context)


def manage_course(request):
    courses = Course.objects.all()
    context = {
        'courses': courses,
        'page_title': 'Manage Courses'
    }
    return render(request, "hod_template/manage_course.html", context)


def manage_dept(request):
    depts = Department.objects.all()
    context = {
        'depts': depts,
        'page_title': 'Manage Department'
    }
    return render(request, "hod_template/manage_dept.html", context)


def manage_level(request):
    levels = Level.objects.all()
    context = {
        'levels': levels,
        'page_title': 'Manage Level'
    }
    return render(request, "hod_template/manage_level.html", context)


def manage_subject(request):
    subjects = Subject.objects.all()
    context = {
        'subjects': subjects,
        'page_title': 'Manage Subjects'
    }
    return render(request, "hod_template/manage_subject.html", context)


def edit_staff(request, staff_id):
    staff = get_object_or_404(Staff, id=staff_id)
    form = StaffForm(request.POST or None, instance=staff)
    context = {
        'form': form,
        'staff_id': staff_id,
        'page_title': 'Edit Staff'
    }
    if request.method == 'POST':
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            address = form.cleaned_data.get('address')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            gender = form.cleaned_data.get('gender')
            password = form.cleaned_data.get('password') or None
            course = form.cleaned_data.get('course')
            passport = request.FILES.get('profile_pic') or None
            try:
                user = CustomUser.objects.get(id=staff.admin.id)
                user.username = username
                user.email = email
                if password is not None:
                    user.set_password(password)
                if passport is not None:
                    fs = FileSystemStorage()
                    filename = fs.save(passport.name, passport)
                    passport_url = fs.url(filename)
                    user.profile_pic = passport_url
                user.first_name = first_name
                user.last_name = last_name
                user.gender = gender
                user.address = address
                staff.course = course
                user.save()
                staff.save()
                messages.success(request, "Successfully Updated")
                return redirect(reverse('edit_staff', args=[staff_id]))
            except Exception as e:
                messages.error(request, "Could Not Update " + str(e))
        else:
            messages.error(request, "Please fil form properly")
    else:
        user = CustomUser.objects.get(id=staff_id)
        staff = Staff.objects.get(id=user.id)
        return render(request, "hod_template/edit_staff_template.html", context)


def edit_lecturer(request, lecturer_id):
    lecturer = get_object_or_404(Lecturer, id=lecturer_id)
    form = LecturerForm(request.POST or None, instance=lecturer)
    context = {
        'form': form,
        'lecturer_id': lecturer_id,
        'page_title': 'Edit Lecturer'
    }
    if request.method == 'POST':
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            address = form.cleaned_data.get('address')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            gender = form.cleaned_data.get('gender')
            password = form.cleaned_data.get('password') or None
            course = form.cleaned_data.get('course')
            passport = request.FILES.get('profile_pic') or None
            try:
                user = CustomUser.objects.get(id=lecturer.admin.id)
                user.username = username
                user.email = email
                if password is not None:
                    user.set_password(password)
                if passport is not None:
                    fs = FileSystemStorage()
                    filename = fs.save(passport.name, passport)
                    passport_url = fs.url(filename)
                    user.profile_pic = passport_url
                user.first_name = first_name
                user.last_name = last_name
                user.gender = gender
                user.address = address
                lecturer.course = course
                user.save()
                lecturer.save()
                messages.success(request, "Successfully Updated")
                return redirect(reverse('edit_lecturer', args=[lecturer_id]))
            except Exception as e:
                messages.error(request, "Could Not Update " + str(e))
        else:
            messages.error(request, "Please fil form properly")
    else:
        user = CustomUser.objects.get(id=lecturer_id)
        lecturer = Lecturer.objects.get(id=user.id)
        return render(request, "hod_template/edit_staff_template.html", context)


def edit_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    form = StudentForm(request.POST or None, instance=student)
    context = {
        'form': form,
        'student_id': student_id,
        'page_title': 'Edit Student'
    }
    if request.method == 'POST':
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            address = form.cleaned_data.get('address')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            gender = form.cleaned_data.get('gender')
            phone_no = form.cleaned_data.get('phone_no')
            password = form.cleaned_data.get('password') or None
            course = form.cleaned_data.get('course')
            session = form.cleaned_data.get('session')
            passport = request.FILES.get('profile_pic') or None
            try:
                user = CustomUser.objects.get(id=student.admin.id)
                if passport != None:
                    fs = FileSystemStorage()
                    filename = fs.save(passport.name, passport)
                    passport_url = fs.url(filename)
                    user.profile_pic = passport_url
                user.username = username
                user.email = email
                if password != None:
                    user.set_password(password)
                user.first_name = first_name
                user.last_name = last_name
                student.session = session
                user.gender = gender
                user.phone_no = phone_no
                user.address = address
                student.course = course
                user.save()
                student.save()
                messages.success(request, "Successfully Updated")
                return redirect(reverse('edit_student', args=[student_id]))
            except Exception as e:
                messages.error(request, "Could Not Update " + str(e))
        else:
            messages.error(request, "Please Fill Form Properly!")
    else:
        return render(request, "hod_template/edit_student_template.html", context)


def edit_course(request, course_id):
    instance = get_object_or_404(Course, id=course_id)
    form = CourseForm(request.POST or None, instance=instance)
    context = {
        'form': form,
        'course_id': course_id,
        'page_title': 'Edit Course'
    }
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data.get('name')
            try:
                course = Course.objects.get(id=course_id)
                course.name = name
                course.save()
                messages.success(request, "Successfully Updated")
            except:
                messages.error(request, "Could Not Update")
        else:
            messages.error(request, "Could Not Update")

    return render(request, 'hod_template/edit_course_template.html', context)


def edit_subject(request, subject_id):
    instance = get_object_or_404(Subject, id=subject_id)
    form = SubjectForm(request.POST or None, instance=instance)
    context = {
        'form': form,
        'subject_id': subject_id,
        'page_title': 'Edit Subject'
    }
    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data.get('name')
            course = form.cleaned_data.get('course')
            staff = form.cleaned_data.get('staff')
            lecturer = form.cleaned_data.get('lecturer')

            try:
                subject = Subject.objects.get(id=subject_id)
                subject.name = name
                subject.staff = staff
                subject.lecturer = lecturer
                subject.course = course
                subject.save()
                messages.success(request, "Successfully Updated")
                return redirect(reverse('edit_subject', args=[subject_id]))
            except Exception as e:
                messages.error(request, "Could Not Add " + str(e))
        else:
            messages.error(request, "Fill Form Properly")
    return render(request, 'hod_template/edit_subject_template.html', context)


def add_session(request):
    form = AcademicSessionForm(request.POST or None)
    context = {'form': form, 'page_title': 'Add Session'}
    if request.method == 'POST':
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Session Created")
                return redirect(reverse('add_session'))
            except Exception as e:
                messages.error(request, 'Could Not Add ' + str(e))
        else:
            messages.error(request, 'Fill Form Properly ')
    return render(request, "hod_template/add_session_template.html", context)


def manage_session(request):
    sessions = AcademicSession.objects.all()
    context = {'sessions': sessions, 'page_title': 'Manage Sessions'}
    return render(request, "hod_template/manage_session.html", context)


def add_term(request):
    form = AcademicTermForm(request.POST or None)
    context = {'form': form, 'page_title': 'Add Term'}
    if request.method == 'POST':
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Session Created")
                return redirect(reverse('add_term'))
            except Exception as e:
                messages.error(request, 'Could Not Add ' + str(e))
        else:
            messages.error(request, 'Fill Form Properly ')
    return render(request, "hod_template/add_term.html", context)


def manage_term(request):
    terms = AcademicTerm.objects.all()
    context = {'terms': terms, 'page_title': 'Manage Term'}
    return render(request, "hod_template/manage_term.html", context)


def edit_term(request, term_id):
    instance = get_object_or_404(AcademicTerm, id=term_id)
    form = AcademicTermForm(request.POST or None, instance=instance)
    context = {'form': form, 'term_id': term_id,
               'page_title': 'Edit Term'}
    if request.method == 'POST':
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Session Updated")
                return redirect(reverse('edit_term', args=[term_id]))
            except Exception as e:
                messages.error(
                    request, "Session Could Not Be Updated " + str(e))
                return render(request, "hod_template/edit_term.html", context)
        else:
            messages.error(request, "Invalid Form Submitted ")
            return render(request, "hod_template/edit_term.html", context)

    else:
        return render(request, "hod_template/edit_term.html", context)


def edit_session(request, session_id):
    instance = get_object_or_404(AcademicSession, id=session_id)
    form = AcademicSessionForm(request.POST or None, instance=instance)
    context = {'form': form, 'session_id': session_id,
               'page_title': 'Edit Session'}
    if request.method == 'POST':
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Session Updated")
                return redirect(reverse('edit_session', args=[session_id]))
            except Exception as e:
                messages.error(
                    request, "Session Could Not Be Updated " + str(e))
                return render(request, "hod_template/edit_session_template.html", context)
        else:
            messages.error(request, "Invalid Form Submitted ")
            return render(request, "hod_template/edit_session_template.html", context)

    else:
        return render(request, "hod_template/edit_session_template.html", context)


@csrf_exempt
def check_email_availability(request):
    email = request.POST.get("email")
    try:
        user = CustomUser.objects.filter(email=email).exists()
        if user:
            return HttpResponse(True)
        return HttpResponse(False)
    except Exception as e:
        return HttpResponse(False)


@csrf_exempt
def check_matric_no_availability(request):
    matric_no = request.POST.get("matric_no")
    try:
        user = CustomUser.objects.filter(matric_no=matric_no).exists()
        if user:
            return HttpResponse(True)
        return HttpResponse(False)
    except Exception as e:
        return HttpResponse(False)


@csrf_exempt
def student_feedback_message(request):
    if request.method != 'POST':
        feedbacks = FeedbackStudent.objects.all()
        context = {
            'feedbacks': feedbacks,
            'page_title': 'Student Feedback Messages'
        }
        return render(request, 'hod_template/student_feedback_template.html', context)
    else:
        feedback_id = request.POST.get('id')
        try:
            feedback = get_object_or_404(FeedbackStudent, id=feedback_id)
            reply = request.POST.get('reply')
            feedback.reply = reply
            feedback.save()
            return HttpResponse(True)
        except Exception as e:
            return HttpResponse(False)


@csrf_exempt
def staff_feedback_message(request):
    if request.method != 'POST':
        feedbacks = FeedbackStaff.objects.all()
        context = {
            'feedbacks': feedbacks,
            'page_title': 'Staff Feedback Messages'
        }
        return render(request, 'hod_template/staff_feedback_template.html', context)
    else:
        feedback_id = request.POST.get('id')
        try:
            feedback = get_object_or_404(FeedbackStaff, id=feedback_id)
            reply = request.POST.get('reply')
            feedback.reply = reply
            feedback.save()
            return HttpResponse(True)
        except Exception as e:
            return HttpResponse(False)


@csrf_exempt
def view_staff_leave(request):
    if request.method != 'POST':
        allLeave = LeaveReportStaff.objects.all()
        context = {
            'allLeave': allLeave,
            'page_title': 'Leave Applications From Staff'
        }
        return render(request, "hod_template/staff_leave_view.html", context)
    else:
        id = request.POST.get('id')
        status = request.POST.get('status')
        if (status == '1'):
            status = 1
        else:
            status = -1
        try:
            leave = get_object_or_404(LeaveReportStaff, id=id)
            leave.status = status
            leave.save()
            return HttpResponse(True)
        except Exception as e:
            return False


@csrf_exempt
def view_student_leave(request):
    if request.method != 'POST':
        allLeave = LeaveReportStudent.objects.all()
        context = {
            'allLeave': allLeave,
            'page_title': 'Leave Applications From Students'
        }
        return render(request, "hod_template/student_leave_view.html", context)
    else:
        id = request.POST.get('id')
        status = request.POST.get('status')
        if (status == '1'):
            status = 1
        else:
            status = -1
        try:
            leave = get_object_or_404(LeaveReportStudent, id=id)
            leave.status = status
            leave.save()
            return HttpResponse(True)
        except Exception as e:
            return False


def admin_view_attendance(request):
    subjects = Subject.objects.all()
    sessions = AcademicSession.objects.all()
    context = {
        'subjects': subjects,
        'sessions': sessions,
        'page_title': 'View Attendance'
    }

    return render(request, "hod_template/admin_view_attendance.html", context)


@csrf_exempt
def get_admin_attendance(request):
    subject_id = request.POST.get('subject')
    session_id = request.POST.get('session')
    attendance_date_id = request.POST.get('attendance_date_id')
    try:
        subject = get_object_or_404(Subject, id=subject_id)
        session = get_object_or_404(AcademicSession, id=session_id)
        attendance = get_object_or_404(
            Attendance, id=attendance_date_id, session=session)
        attendance_reports = AttendanceReport.objects.filter(
            attendance=attendance)
        json_data = []
        for report in attendance_reports:
            data = {
                "status": str(report.status),
                "name": str(report.student)
            }
            json_data.append(data)
        return JsonResponse(json.dumps(json_data), safe=False)
    except Exception as e:
        return None


def admin_view_profile(request):
    admin = get_object_or_404(Admin, admin=request.user)
    form = AdminForm(request.POST or None, request.FILES or None,
                     instance=admin)
    context = {'form': form,
               'page_title': 'View/Edit Profile'
               }
    if request.method == 'POST':
        try:
            if form.is_valid():
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                password = form.cleaned_data.get('password') or None
                passport = request.FILES.get('profile_pic') or None
                custom_user = admin.admin
                if password is not None:
                    custom_user.set_password(password)
                if passport is not None:
                    fs = FileSystemStorage()
                    filename = fs.save(passport.name, passport)
                    passport_url = fs.url(filename)
                    custom_user.profile_pic = passport_url
                custom_user.first_name = first_name
                custom_user.last_name = last_name
                custom_user.save()
                messages.success(request, "Profile Updated!")
                return redirect(reverse('admin_view_profile'))
            else:
                messages.error(request, "Invalid Data Provided")
        except Exception as e:
            messages.error(request, "Error Occurred While Updating Profile " + str(e))
    return render(request, "hod_template/admin_view_profile.html", context)


def admin_notify_staff(request):
    staff = CustomUser.objects.filter(user_type=2)
    context = {
        'page_title': "Send Notifications To Staff",
        'allStaff': staff
    }
    return render(request, "hod_template/staff_notification.html", context)


def admin_notify_student(request):
    student = CustomUser.objects.filter(user_type=3)
    context = {
        'page_title': "Send Notifications To Students",
        'students': student
    }
    return render(request, "hod_template/student_notification.html", context)


@csrf_exempt
def send_student_notification(request):
    id = request.POST.get('id')
    message = request.POST.get('message')
    student = get_object_or_404(Student, admin_id=id)
    try:
        url = "https://fcm.googleapis.com/fcm/send"
        body = {
            'notification': {
                'title': "Student Management System",
                'body': message,
                'click_action': reverse('student_view_notification'),
                'icon': static('dist/img/AdminLTELogo.png')
            },
            'to': student.admin.fcm_token
        }
        headers = {'Authorization':
                       'key=AAAA3Bm8j_M:APA91bElZlOLetwV696SoEtgzpJr2qbxBfxVBfDWFiopBWzfCfzQp2nRyC7_A2mlukZEHV4g1AmyC6P_HonvSkY2YyliKt5tT3fe_1lrKod2Daigzhb2xnYQMxUWjCAIQcUexAMPZePB',
                   'Content-Type': 'application/json'}
        data = requests.post(url, data=json.dumps(body), headers=headers)
        notification = NotificationStudent(student=student, message=message)
        notification.save()
        return HttpResponse("True")
    except Exception as e:
        return HttpResponse("False")


@csrf_exempt
def send_staff_notification(request):
    id = request.POST.get('id')
    message = request.POST.get('message')
    staff = get_object_or_404(Staff, admin_id=id)
    try:
        url = "https://fcm.googleapis.com/fcm/send"
        body = {
            'notification': {
                'title': "Student Management System",
                'body': message,
                'click_action': reverse('staff_view_notification'),
                'icon': static('dist/img/AdminLTELogo.png')
            },
            'to': staff.admin.fcm_token
        }
        headers = {'Authorization':
                       'key=AAAA3Bm8j_M:APA91bElZlOLetwV696SoEtgzpJr2qbxBfxVBfDWFiopBWzfCfzQp2nRyC7_A2mlukZEHV4g1AmyC6P_HonvSkY2YyliKt5tT3fe_1lrKod2Daigzhb2xnYQMxUWjCAIQcUexAMPZePB',
                   'Content-Type': 'application/json'}
        data = requests.post(url, data=json.dumps(body), headers=headers)
        notification = NotificationStaff(staff=staff, message=message)
        notification.save()
        return HttpResponse("True")
    except Exception as e:
        return HttpResponse("False")


class ReceiptCreateView(CreateView):
    model = Receipt
    fields = ['amount_paid', 'date_paid', 'comment', 'bank_name', 'branch', 'mode_of_payment', 'receipt_id']
    success_url = 'list'
    template_name = 'hod_template/receipt_form.html'

    def form_valid(self, form):
        obj = form.save(commit=False)
        invoice = Invoice.objects.get(pk=self.request.GET['invoice'])
        obj.invoice = invoice
        obj.save()
        return redirect('list')

    def get_context_data(self, **kwargs):
        context = super(ReceiptCreateView, self).get_context_data(**kwargs)
        invoice = Invoice.objects.get(pk=self.request.GET['invoice'])
        context['invoice'] = invoice
        return context


class ReceiptUpdateView(UpdateView):
    model = Receipt
    fields = ['amount_paid', 'date_paid', 'comment', 'bank_name', 'branch', 'mode_of_payment']
    success_url = reverse_lazy('invoice-list')


class SessionListView(SuccessMessageMixin, ListView):
    model = AcademicSession
    template_name = 'corecode/session_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AcademicSessionForm()
        return context


class SessionCreateView(SuccessMessageMixin, CreateView):
    model = AcademicSession
    form_class = AcademicSessionForm
    template_name = 'corecode/mgt_form.html'
    success_url = reverse_lazy('sessions')
    success_message = 'New session successfully added'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add new session'
        return context


class SessionUpdateView(SuccessMessageMixin, UpdateView):
    model = AcademicSession
    form_class = AcademicSessionForm
    success_url = reverse_lazy('sessions')
    success_message = 'Session successfully updated.'
    template_name = 'corecode/mgt_form.html'

    def form_valid(self, form):
        obj = self.object
        if obj.current == False:
            terms = AcademicSession.objects.filter(
                current=True).exclude(name=obj.name).exists()
            if not terms:
                messages.warning(self.request, 'You must set a session to current.')
                return redirect('session-list')
        return super().form_valid(form)


class SessionDeleteView(DeleteView):
    model = AcademicSession
    success_url = reverse_lazy('sessions')
    template_name = 'corecode/core_confirm_delete.html'
    success_message = "The session {} has been deleted with all its attached content"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.current == True:
            messages.warning(request, 'Cannot delete session as it is set to current')
            return redirect('sessions')
        messages.success(self.request, self.success_message.format(obj.name))
        return super(SessionDeleteView, self).delete(request, *args, **kwargs)


class TermListView(ListView):
    model = AcademicTerm
    template_name = 'hod_template/manage_term.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AcademicTermForm()
        return context


class TermCreateView(CreateView):
    model = AcademicTerm
    form_class = AcademicTermForm
    template_name = 'corecode/mgt_form.html'
    success_url = reverse_lazy('terms')
    success_message = 'New term successfully added'


class TermUpdateView(UpdateView):
    model = AcademicTerm
    form_class = AcademicTermForm
    success_url = reverse_lazy('terms')
    success_message = 'Term successfully updated.'
    template_name = 'hod_template/manage_term.html'

    def form_valid(self, form):
        obj = self.object
        if obj.current == False:
            terms = AcademicTerm.objects.filter(current=True).exclude(name=obj.name).exists()
            if not terms:
                messages.warning(self.request, 'You must set a term to current.')
                return redirect('term')
        return super().form_valid(form)


class TermDeleteView(DeleteView):
    model = AcademicTerm
    success_url = reverse_lazy('terms')
    template_name = 'corecode/core_confirm_delete.html'
    success_message = "The term {} has been deleted with all its attached content"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.current:
            messages.warning(request, 'Cannot delete term as it is set to current')
            return redirect('terms')
        messages.success(self.request, self.success_message.format(obj.name))
        return super(TermDeleteView, self).delete(request, *args, **kwargs)


def current_session_view(request):
    """ Current SEssion and Term """
    if request.method == 'POST':
        form = CurrentSessionForm(request.POST)
        if form.is_valid():
            session = form.cleaned_data['current_session']
            term = form.cleaned_data['current_term']
            AcademicSession.objects.filter(name=session).update(current=True)
            AcademicSession.objects.exclude(name=session).update(current=False)
            AcademicTerm.objects.filter(name=term).update(current=True)
            AcademicTerm.objects.exclude(name=term).update(current=False)

        else:
            form = CurrentSessionForm(initial={
                "current_session": AcademicSession.objects.filter(current=True),
                "current_term": AcademicTerm.objects.filter(current=True)
            })

        return render(request, 'corecode/current_session.html', {"form": form})


def bulk_invoice(request):
    return render(request, 'corecode/bulk_invoice.html')


class StudentBulkUploadView(CreateView):
    model = StudentBulkUpload
    template_name = 'corecode/students_upload.html'
    fields = ['csv_file']
    success_url = reverse_lazy('manage_student')
    success_message = 'Successfully uploaded students'


def downloadcsv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="student_template.csv"'

    writer = csv.writer(response)
    writer.writerow(['matric_no', 'surname',
                     'firstname', 'email', 'phone_no', 'gender', 'created_at', 'address'])

    return response


class InvoiceBulkUpload(CreateView):
    model = InvoiceBulkUpload
    template_name = 'corecode/bulk_invoice.html'
    fields = ['csv_file']
    success_url = reverse_lazy('invoice-list')
    success_message = 'Successfully uploaded Invoice'


def downloadcv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="student_invoice.csv"'

    writer = csv.writer(response)
    writer.writerow(['student', 'session',
                     'term', 'dept_info', 'level_info'])

    return response
