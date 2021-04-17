from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Invoice
from .models import Student, StudentBulkUpload, CustomUser, InvoiceBulkUpload, Invoice
import os
import csv
from io import StringIO
from django.db.models.signals import post_save, post_delete




@receiver(post_save, sender=Invoice)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Invoice.objects.create(user=instance)


@receiver(post_save, sender=Invoice)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(post_save, sender=InvoiceBulkUpload)
def create_bulk_student(sender, created, instance, *args, **kwargs):
    if created:
        opened = StringIO(instance.csv_file.read().decode())
        reading = csv.DictReader(opened, delimiter=',')
        students = []
        for row in reading:
            if 'student' in row and row['student']:
                student = row['student']
                session = row['session'] if 'session' in row and row['session'] else ''
                term = row['term'] if 'term' in row and row['term'] else ''
                 dept_info = row['dept_info'] if 'dept_info' in row and row['dept_info'] else ''
                level_info = row['level_info'] if 'level_info' in row and row['level_info'] else ''
                check = Student.objects.filter(student=student).exists()
                if not check:
                    students.append(
                        Student(
                            student=student,
                            session=session,
                            term=term,
                            dept_info=dept_info,
                            level_info=level_info,
                            current_status='active'
                        )
                    )

        Student.objects.bulk_create(students)
        instance.csv_file.close()
        instance.delete()


def _delete_file(path):
    """ Deletes file from filesystem. """
    if os.path.isfile(path):
        os.remove(path)


@receiver(post_delete, sender=InvoiceBulkUpload)
def delete_csv_file(sender, instance, *args, **kwargs):
    if instance.csv_file:
        _delete_file(instance.csv_file.path)








@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        CustomUser.objects.create(user=instance)


@receiver(post_save, sender=CustomUser)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(post_save, sender=StudentBulkUpload)
def create_bulk_student(sender, created, instance, *args, **kwargs):
    if created:
        opened = StringIO(instance.csv_file.read().decode())
        reading = csv.DictReader(opened, delimiter=',')
        students = []
        for row in reading:
            if 'matric_no' in row and row['matric_no']:
                matric_no = row['matric_no']
                email = row['email'] if 'email' in row and row['email'] else ''
                phone_no = row['phone_no'] if 'phone_no' in row and row['phone_no'] else ''
                gender = (row['gender']).lower(
                ) if 'gender' in row and row['gender'] else ''
                # phone = row['mobile_number'] if 'mobile_number' in row and row['mobile_number'] else ''
                address = row['address'] if 'address' in row and row['address'] else ''
                check = Student.objects.filter(matric_no=matric_no).exists()
                if not check:
                    students.append(
                        Student(
                            matric_no=matric_no,
                            email=email,
                            phone_no=phone_no,
                            gender=gender,
                            address=address,
                            current_status='active'
                        )
                    )

        Student.objects.bulk_create(students)
        instance.csv_file.close()
        instance.delete()


def _delete_file(path):
    """ Deletes file from filesystem. """
    if os.path.isfile(path):
        os.remove(path)


@receiver(post_delete, sender=StudentBulkUpload)
def delete_csv_file(sender, instance, *args, **kwargs):
    if instance.csv_file:
        _delete_file(instance.csv_file.path)


@receiver(post_delete, sender=Student)
def delete_passport_on_delete(sender, instance, *args, **kwargs):
    if instance.passport:
        _delete_file(instance.passport.path)


@receiver(post_save, sender=Invoice)
def after_creating_invoice(sender, instance, created, **kwargs):
    if created:
        previous_inv = Invoice.objects.filter(
            student=instance.student).exclude(id=instance.id).last()
        if previous_inv:
            previous_inv.status = 'closed'
            previous_inv.save()
            instance.balance_from_previous_term = previous_inv.balance()
            instance.save()
