"""student_management_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from .staff_views import InvoiceCreateView, InvoiceListView, InvoiceDeleteView, InvoiceDetailView, InvoiceUpdateView, \
    ReceiptCreateView, ReceiptUpdateView, StaffListView
from .hod_views import StudentDetailView, StudentDeleteView, LecturerDeleteView, LecturerDetailView, \
    StudentBulkUploadView, downloadcsv
from sms.EditResultView import EditResultView
from .student_views import InvoiceDetailVie, ReceiptDetailView, student_list
from .lecturer_views import LecturerListView

from . import hod_views, staff_views, student_views, views, lecturer_views

urlpatterns = [
    path("", views.login_page, name='login_page'),
    path('delete/<int:pk>/', StudentDeleteView.as_view(), name='student-delete'),
    path('<int:pk>/', StudentDetailView.as_view(), name='student-detail'),
    path('<int:pk>/delete/', LecturerDeleteView.as_view(), name='lecturer_delete'),
    path('<int:pk>/detailss/', LecturerDetailView.as_view(), name='detail'),
    path("get_attendance", views.get_attendance, name='get_attendance'),
    path("firebase-messaging-sw.js", views.showFirebaseJS, name='showFirebaseJS'),
    path("doLogin/", views.doLogin, name='user_login'),
    path("logout_user/", views.logout_user, name='user_logout'),
    path("admin/home/", hod_views.admin_home, name='admin_home'),
    path("staff/add", hod_views.add_staff, name='add_staff'),
    path("lecturer/add", hod_views.add_lecturer, name='add_lecturer'),
    path("course/add", hod_views.add_course, name='add_course'),
    path("dept/add", hod_views.add_dept, name='add_dept'),
    path("level/add", hod_views.add_level, name='add_level'),
    path("add_session/", hod_views.add_session, name='add_session'),
    path("check_email_availability", hod_views.check_email_availability, name="check_email_availability"),
    path("check_matric_no_availability/", hod_views.check_matric_no_availability, name="check_matric_no_availability"),
    path("session/manage/", hod_views.manage_session, name='manage_session'),
    path("session/edit/<int:session_id>", hod_views.edit_session, name='edit_session'),
    path("term/manage/", hod_views.manage_term, name='manage_term'),
    path("term/edit/<int:term_id>", hod_views.edit_term, name='edit_term'),
    path("add_term/", hod_views.add_term, name='add_term'),
    path("student/add/", hod_views.add_student, name='add_student'),
    path("subject/add/", hod_views.add_subject, name='add_subject'),
    path("staff/manage/", hod_views.manage_staff, name='manage_staff'),
    path("lecturer/manage/", hod_views.manage_lecturer, name='manage_lecturer'),
    path("student/manage/", hod_views.manage_student, name='manage_student'),
    path("course/manage/", hod_views.manage_course, name='manage_course'),
    path("dept/manage/", hod_views.manage_dept, name='manage_dept'),
    path("level/manage/", hod_views.manage_level, name='manage_level'),
    path("subject/manage/", hod_views.manage_subject, name='manage_subject'),
    path("staff/edit/<int:staff_id>", hod_views.edit_staff, name='edit_staff'),
    path("lecturer/edit/<int:lecturer_id>", hod_views.edit_lecturer, name='edit_lecturer'),
    path("student/edit/<int:student_id>", hod_views.edit_student, name='edit_student'),
    path("course/edit/<int:course_id>", hod_views.edit_course, name='edit_course'),
    path("dept/edit/<int:dept_id>", hod_views.edit_dept, name='edit_dept'),
    path("subject/edit/<int:subject_id>", hod_views.edit_subject, name='edit_subject'),
    path('upload/', StudentBulkUploadView.as_view(), name='student-upload'),
    path('downloadcsv/', downloadcsv, name='download-csv'),

    # Staff
    path("staff/home/", staff_views.staff_home, name='staff_home'),
    path("staff/get_students/", staff_views.get_students, name='get_students'),
    path("staff/attendance/fetch/", staff_views.get_student_attendance, name='get_student_attendance'),
    path("staff/attendance/take/", staff_views.staff_take_attendance, name='staff_take_attendance'),
    path("staff/payment/confirm/", staff_views.staff_confirm_payment, name='staff_comfirm_payment'),
    path("staff/attendance/update/", staff_views.staff_update_attendance, name='staff_update_attendance'),
    path("staff/fcmtoken/", staff_views.staff_fcmtoken, name='staff_fcmtoken'),
    path("staff/view/profile/", staff_views.staff_view_profile, name='staff_view_profile'),
    path("staff/attendance/save/", staff_views.save_attendance, name='save_attendance'),
    path("staff/attendance/update/", staff_views.update_attendance, name='update_attendance'),
    path("staff/result/edit/", EditResultView.as_view(), name='edit_student_result'),
    path('staff/result/fetch/', staff_views.fetch_student_result, name='fetch_student_result'),
    path('list/', InvoiceListView.as_view(), name='invoice-list'),

    path('create/', InvoiceCreateView.as_view(), name='invoice-create'),
    path('<int:pk>/detail/', InvoiceDetailView.as_view(), name='invoice-detail'),
    path('<int:pk>/update/', InvoiceUpdateView.as_view(), name='invoice-update'),
    path('<int:pk>/inviolate/', InvoiceDeleteView.as_view(), name='inviolate'),
    path('receipt/create', ReceiptCreateView.as_view(), name='receipt-create'),
    path('receipt/<int:pk>/update/', ReceiptUpdateView.as_view(), name='receipt-update'),
    path('current-session/', staff_views.current_session_view, name='current-session'),

    path('session/list/', staff_views.SessionListView.as_view(), name='sessions'),
    path('session/create/', staff_views.SessionCreateView.as_view(), name='session-create'),
    path('session/<int:pk>/update/',
         staff_views.SessionUpdateView.as_view(), name='session-update'),
    path('session/<int:pk>/delete/',
         staff_views.SessionDeleteView.as_view(), name='session-delete'),

    path('term/list/', staff_views.TermListView.as_view(), name='terms'),
    path('term/create/', staff_views.TermCreateView.as_view(), name='term-create'),
    path('term/<int:pk>/update/',
         staff_views.TermUpdateView.as_view(), name='term-update'),
    path('term/<int:pk>/delete/',
         staff_views.TermDeleteView.as_view(), name='term-delete'),

    # Lecturer 
    path("lecturer/home/", lecturer_views.lecturer_home, name='lecturer_home'),
    path("lecturer/get_students/", lecturer_views.get_students, name='get_students'),
    path("lecturer/attendance/fetch/", lecturer_views.get_student_attendance, name='get_student_attendance'),
    path("lecturer/attendance/take/", lecturer_views.lecturer_take_attendance, name='lecturer_take_attendance'),
    path("lecturer/attendance/update/", lecturer_views.lecturer_update_attendance, name='lecturer_update_attendance'),
    path("staff/fcmtoken/", staff_views.staff_fcmtoken, name='staff_fcmtoken'),
    path("lecturer/view/profile/", lecturer_views.lecturer_view_profile, name='lecturer_view_profile'),
    path("lecturer/attendance/save/", lecturer_views.save_attendance, name='save_attendance'),
    path("lecturer/attendance/update/", lecturer_views.update_attendance, name='update_attendance'),
    path('lecturer/result/fetch/', lecturer_views.fetch_student_result, name='fetch_student_result'),
    path("lecturer/result/edit/", EditResultView.as_view(), name='edit_student_result'),
    path("lecturer/result/add/", lecturer_views.lecturer_add_result, name='lecturer_add_result'),
    path('bulk-invoice/', hod_views.bulk_invoice, name='bulk-invoice'),

    # Student
    path('list', student_list, name='student-list'),
    path("student/view/profile/", student_views.student_view_profile, name='student_view_profile'),
    path("student/fcmtoken/", student_views.student_fcmtoken, name='student_fcmtoken'),
    path("student/home/", student_views.student_home, name='student_home'),
    path("student/view/attendance/", student_views.student_view_attendance, name='student_view_attendance'),
    path('student/view/result/', student_views.student_view_result, name='student_view_result'),
    path('student/view/receipt/', student_views.student_view_receipt, name='student_view_receipt'),
    path('student/view/invoice/', student_views.student_view_invoice, name='student_view_invoice'),
    path('<int:pk>/details/', InvoiceDetailVie.as_view(), name='invoice-details'),

]
