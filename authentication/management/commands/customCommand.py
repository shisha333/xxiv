import sys
import string
import random
from django.core.management.base import BaseCommand, CommandError
from authentication.models import User
from datetime import datetime

class Command(BaseCommand):
    help = 'Create super user'

    """ def add_arguments(self, parser):
        parser.add_argument('first_name') """
    def compare_password(self, password1, password2):
        self.password1 = password1
        self.password2 = password2
        if password1 == password2:
            return True
        else:
            return False

    def handle(self, *args, **options):
        
        first_name = last_name = gender = email = password1 = ""

        first_name = input("Enter first name:")
        last_name = input("Enter last name:")
        # gender = input("Gender male/female: ")
        email = input("Enter email: ")
        password1 = input("Enter password: ")
        password2 = input("Re-enter password:")
        
        if first_name is None:
            self.stderr.write("\n First name reuired")
            return
        if last_name is None:
            self.stderr.write("\n Last name required")
            return
        # if date_of_birth is None:
        #     self.stderr.write("\n Date of birth required")
        #     return
        # if gender is None:
        #     self.stderr.write("\n Gender required")
        #     return
        if email is None:
            self.stderr.write("\n Email is equired")
            return
        if '@' not in email:
            self.stderr.write("\n Email should contain @")
            return
        if password1 is None:
            self.stderr.write("\n Password qeuired")
            return
        if password2 is None:
            self.stderr.write("\n Password confirmaation required")
            return
        
        # ref = string.ascii_letters + string.digits
        # rndStr =  ''.join(random.SystemRandom().choice(ref) for _ in range(8))+str(datetime.now().day)+str(datetime.now().month)
        
        
        checkEmail = User.objects.filter(email=email).first()
        if checkEmail is not None:
            self.stderr.write(checkEmail.email+" Email address already exists")

        if self.compare_password(password1, password2):
            if len(password2) <= 5:
                self.stdout.write(" password should contain at least 6 characters")
            else:
                user = User(
                    email= email,
                    password= password2,
                    first_name=first_name,
                    last_name=last_name,
                )
                user.set_password(password2)
                user.is_superuser = True
                user.is_staff = True
                user.save()
                self.stdout.write("Account created successfully \n")

                self.stdout.write("============================== \n\n")
                self.stdout.write("Names: "+ first_name+ " "+ last_name +"\n")
                # self.stdout.write("Gender: "+ gender +"\n")
                # self.stdout.write("Date of birth: "+ date_of_birth +"\n")
                self.stdout.write("Email: "+ email +"\n\n")
                self.stdout.write("============================== \n")
        else:
            self.stdout.write("Password didn't match")