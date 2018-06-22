from django.db import models


class User(models.Model):
    user_name = models.CharField(max_length=20, primary_key=True)
    password = models.CharField(max_length=20)
    email_address = models.CharField(max_length=40, unique=True)
    register_date = models.DateTimeField()

    def __str__(self):
        return self.user_name


def check_type(password, email_address):
    check_result = {'valid': True}
    if len(password) <= 6:
        check_result['valid'] = False
        check_result['content'] = 'The password is less than 6 words'
    at_index = email_address.find('@')
    dot_index = email_address.find('.')
    if at_index == -1 or dot_index == -1 or at_index >= dot_index-1:
        check_result['valid'] = False
        check_result['content'] = 'The format of the email is invalid'
    return check_result




