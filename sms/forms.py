from django import forms
from django.forms.widgets import DateInput, TextInput
from django.forms import inlineformset_factory, modelformset_factory

from .models import *

InvoiceItemFormset = inlineformset_factory(
    Invoice, InvoiceItem, fields=['description', 'amount'], extra=1, can_delete=True)

InvoiceReceiptFormSet = inlineformset_factory(
    Invoice, Receipt, fields=('amount_paid', 'date_paid', 'comment'), extra=0, can_delete=True
)

Invoices = modelformset_factory(Invoice, exclude=(), extra=4)


class FormSettings(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormSettings, self).__init__(*args, **kwargs)
        # Here make some changes such as:
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'


class CustomUserForm(FormSettings):
    matric_no = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    gender = forms.ChoiceField(choices=[('M', 'Male'), ('F', 'Female')])
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    address = forms.CharField(widget=forms.Textarea)
    password = forms.CharField(widget=forms.PasswordInput)
    widget = {
        'password': forms.PasswordInput(),
    }
    profile_pic = forms.ImageField()

    def __init__(self, *args, **kwargs):
        super(CustomUserForm, self).__init__(*args, **kwargs)

        if kwargs.get('instance'):
            instance = kwargs.get('instance').admin.__dict__
            self.fields['password'].required = False
            for field in CustomUserForm.Meta.fields:
                self.fields[field].initial = instance.get(field)
            if self.instance.pk is not None:
                self.fields['password'].widget.attrs['placeholder'] = "Fill this only if you wish to update password"

    def clean_email(self):
        formEmail = self.cleaned_data['email'].lower()
        if self.instance.pk is None:  # Insert
            if CustomUser.objects.filter(email=formEmail).exists():
                raise forms.ValidationError(
                    "The given email is already registered")
        else:  # Update
            dbEmail = self.Meta.model.objects.get(
                id=self.instance.pk).admin.email.lower()
            if dbEmail != formEmail:  # There has been changes
                if CustomUser.objects.filter(email=formEmail).exists():
                    raise forms.ValidationError("The given email is already registered")

        return formEmail

    def clean_matric_no(self, *args, **kwargs):
        formMatric_No = self.cleaned_data['matric_no']
        if self.instance.pk is None:  # Insert
            if CustomUser.objects.filter(matric_no=formMatric_No).exists():
                raise forms.ValidationError(
                    "The given Matric_No is already registered")
        else:  # Update
            dbformMatric_No = self.Meta.model.objects.get(
                id=self.instance.pk).admin.matric_no
            if dbformMatric_No != formMatric_No:  # There has been changes
                if CustomUser.objects.filter(matric_no=formMatric_No).exists():
                    raise forms.ValidationError("The given Matric_No is already registered")

        return formMatric_No

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'gender', 'password', 'profile_pic', 'address', 'matric_no']


class StudentForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Student
        fields = CustomUserForm.Meta.fields + \
                 ['course', 'session', 'dept', 'level', 'term']


class AdminForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(AdminForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Admin
        fields = CustomUserForm.Meta.fields


class StaffForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(StaffForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Staff
        fields = CustomUserForm.Meta.fields + \
                 ['first_name', 'last_name', 'email', 'gender', 'password', 'profile_pic', 'address', 'course']


class LecturerForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(LecturerForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Lecturer
        fields = CustomUserForm.Meta.fields + \
                 ['course']


class CourseForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)

    class Meta:
        fields = ['name']
        model = Course


class DepartmentForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(DepartmentForm, self).__init__(*args, **kwargs)

    class Meta:
        fields = ['name']
        model = Department


class LevelForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(LevelForm, self).__init__(*args, **kwargs)

    class Meta:
        fields = ['name']
        model = Level


class SubjectForm(FormSettings):

    def __init__(self, *args, **kwargs):
        super(SubjectForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Subject
        fields = ['name', 'staff', 'lecturer', 'course']


class AcademicSessionForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(AcademicSessionForm, self).__init__(*args, **kwargs)

    class Meta:
        model = AcademicSession
        fields = '__all__'


class AcademicTermForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(AcademicTermForm, self).__init__(*args, **kwargs)

    class Meta:
        model = AcademicTerm
        fields = '__all__'


class LeaveReportStaffForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(LeaveReportStaffForm, self).__init__(*args, **kwargs)

    class Meta:
        model = LeaveReportStaff
        fields = ['date', 'message']
        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
        }


class FeedbackStaffForm(FormSettings):

    def __init__(self, *args, **kwargs):
        super(FeedbackStaffForm, self).__init__(*args, **kwargs)

    class Meta:
        model = FeedbackStaff
        fields = ['feedback']


class LeaveReportStudentForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(LeaveReportStudentForm, self).__init__(*args, **kwargs)

    class Meta:
        model = LeaveReportStudent
        fields = ['date', 'message']
        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
        }


class FeedbackStudentForm(FormSettings):

    def __init__(self, *args, **kwargs):
        super(FeedbackStudentForm, self).__init__(*args, **kwargs)

    class Meta:
        model = FeedbackStudent
        fields = ['feedback']


class StudentEditForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(StudentEditForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Student
        fields = CustomUserForm.Meta.fields + \
                 ['first_name', 'last_name', 'email', 'gender', 'password', 'profile_pic', 'address']


class StaffEditForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(StaffEditForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Staff
        fields = CustomUserForm.Meta.fields


class LecturerEditForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(LecturerEditForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Lecturer
        fields = CustomUserForm.Meta.fields


class EditResultForm(FormSettings):
    session_list = AcademicSession.objects.all()
    session_year = forms.ModelChoiceField(
        label="Session Year", queryset=session_list, required=True)

    def __init__(self, *args, **kwargs):
        super(EditResultForm, self).__init__(*args, **kwargs)

    class Meta:
        model = StudentResult
        fields = ['session_year', 'subject', 'student', 'test', 'exam']


from django.forms import inlineformset_factory, modelformset_factory
from django.forms import ModelForm, modelformset_factory

from .models import AcademicSession, AcademicTerm
from .models import Invoice, InvoiceItem, Receipt

InvoiceItemFormset = inlineformset_factory(
    Invoice, InvoiceItem, fields=['description', 'amount'], extra=1, can_delete=True)

InvoiceReceiptFormSet = inlineformset_factory(
    Invoice, Receipt, fields=('amount_paid', 'date_paid', 'comment', 'bank_name', 'branch', 'mode_of_payment'), extra=0,
    can_delete=True
)

Invoices = modelformset_factory(Invoice, exclude=(), extra=4)


class AcademicSessionForm(ModelForm):
    prefix = 'Academic Session'

    class Meta:
        model = AcademicSession
        fields = ['name', 'current']


class AcademicTermForm(ModelForm):
    prefix = 'Academic Term'

    class Meta:
        model = AcademicTerm
        fields = ['name', 'current']


class CurrentSessionForm(forms.Form):
    current_session = forms.ModelChoiceField(queryset=AcademicSession.objects.all(),
                                             help_text='Click <a href="/session/create/?next=current-session/">here'
                                                       '</a> to add new session')
    current_term = forms.ModelChoiceField(queryset=AcademicTerm.objects.all(),
                                          help_text='Click <a href="/term/create/?next=current-session/">here</a> to '
                                                    'add new term')
