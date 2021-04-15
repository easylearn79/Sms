from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Invoice
from .models import Student, StudentBulkUpload,CustomUser,Bouser,StudentInfo,
import os
import csv
from io import StringIO
from django.db.models.signals import post_save, post_delete




@receiver(post_save, sender=StudentBulkUpload)
def create_bulk_student(sender, created, instance, *args, **kwargs):
  if created:
    opened = StringIO(instance.csv_file.read().decode())
    reading = csv.DictReader(opened, delimiter=',')
    students = []
    for row in reading:
      if 'matric_no' in row and row['matric_no']:
        reg = row['matric_no']
        surname = row['surname'] if 'surname' in row and row['surname'] else ''
        firstname = row['firstname'] if 'firstname' in row and row['firstname'] else ''
        other_names = row['other_names'] if 'other_names' in row and row['other_names'] else ''
        gender = (row['gender']).lower(
        ) if 'gender' in row and row['gender'] else ''
        phone = row['mobile_number'] if 'mobile_number' in row and row['mobile_number'] else ''
        address = row['address'] if 'address' in row and row['address'] else ''
        check = Student.objects.filter(matric_no=reg).exists()
        if not check:
          students.append(
            Student(
                matric_no=reg,
                surname=surname,
                firstname=firstname,
                other_name=other_names,
                gender=gender,
                mobile_number=phone,
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



from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import CustomUser


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        CustomUser.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()












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

