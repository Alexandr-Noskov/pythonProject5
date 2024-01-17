from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from main.models import Courses


@shared_task
def notify_subscriptions_about_course_update(course_id):
    cours = Courses.objects.get(pk=course_id)
    sublist = []
    for sub in cours.subscription_set.all():
        sublist.append(sub.owner.email)

    send_mail("Your subscription on site.",
              f"Update information about your subscription.",
              settings.EMAIL_HOST_USER,
              sublist,
              fail_silently=False)