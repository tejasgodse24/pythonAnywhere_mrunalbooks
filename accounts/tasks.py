from celery import shared_task
from time import sleep
from accounts.models import Profile, Membership_Details, MembershipType
from django.db.models import Q
from datetime import datetime

@shared_task
def check_membership_status():
    membership_details = Membership_Details.objects.filter(is_active = True)
    for detail in membership_details:
        if detail.end_date < datetime.now().date():
            detail.is_active = False
            profile_obj = detail.user.profile
            normal_membership = MembershipType.objects.get(name = 'normal')
            profile_obj.login_type = normal_membership
            detail.save()
            profile_obj.save()
            return "status chenged"
    return "called"




    # users = Profile.objects.filter(
    #     Q(is_email_verified = True) & 
    #     (Q(login_type__name = 'prime') | Q(login_type__name = 'dealer'))
    #     )
    



