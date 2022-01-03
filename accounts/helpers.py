import random
from django.core.cache import cache

def send_otp_to_email(email, user_obj):
    if cache.get(email):
        return False, cache.ttl(email)
    try:
        otp_to_send = random.randint(100000, 999999)
        cache.set(email, otp_to_send, timeout=60)
        user_obj.otp = otp_to_send
        user_obj.save()
        return True, 0
    except Exception as e:
        print(e)
