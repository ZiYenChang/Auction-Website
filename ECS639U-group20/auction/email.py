from django.core.mail import send_mail
from django.http import HttpResponse

def sendSimpleEmail(email):
   res = send_mail("Welcome", "Welcome to our auction website for group 20!", "paul@polo.com", [email])
   return HttpResponse('%s'%res)
