from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    date_of_birth = models.DateField('Date of Birth')
    profile_image = models.ImageField(default='default.jpg', upload_to='profile_images/')
    city = models.CharField(max_length=100)
    REQUIRED_FIELDS = ['date_of_birth', 'email']

    def __str__(self):
        """
        Display as the object name when printing the object
        """
        return self.username

    def to_dict(self):
        """
        Use this to return a dictionary of the User object
        """
        return{
            'id': self.id,
            'date_of_birth': self.date_of_birth,
            'city': self.city,
            'username' : self.username,
            'email' : self.email,
            'profile_image' : self.profile_image.url,
        }

class Item(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=800)
    deadline = models.DateTimeField('End bid time')
    starting_price = models.DecimalField(max_digits = 6, decimal_places=2)
    picture = models.ImageField(upload_to='item_images', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """
        Display the object name when printing the object
        """
        return self.title

    def to_dict(self):
        """
        Use this to return a dictionary of the Item object
        """
        return{
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'deadline': self.deadline,
            'starting_price': self.starting_price,
            'picture': self.picture.url,
            'user': self.user.id,
        }

class Answer(models.Model):
    answer_body = models.CharField(max_length=800)
    answer_time = models.DateTimeField('Date Answered')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """
        Display as the object name when printing the object
        """
        return self.answer_body

    def to_dict(self):
        """
        Use this to return a dictionary of the Answer object
        """
        return{
            'id': self.id,
            'answer_body': self.answer_body,
            'answer_time': self.answer_time,
            'user': self.user.username,
        }

class Question(models.Model):
    question_body = models.CharField(max_length = 800)
    question_time = models.DateTimeField('Date Questioned')
    answer= models.OneToOneField(Answer, on_delete=models.CASCADE, blank=True, null=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """
        Display the object name when printing the object
        """
        return self.question_body

    def to_dict(self):
        """
        Use this to return a dictionary of the Question object
        """
        if self.answer is None:
            return{
                'id': self.id,
                'question_body': self.question_body,
                'question_time': self.question_time,
                'item': self.item.id,
                'user': self.user.username,
            }
        else:
            return{
            'id': self.id,
            'question_body': self.question_body,
            'question_time': self.question_time,
            'answer': self.answer.answer_body,
             'item': self.item.id,
             'user': self.user.username,
            }
        


class Bid(models.Model):
    bid_amount = models.DecimalField(max_digits = 6, decimal_places=2)
    bid_time = models.DateTimeField('Bid submitted')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __int__(self):
        """
        Display the object name when printing the object
        """
        return self.id

    def to_dict(self):
        """
        Use this to return a dictionary of the Bid object
        """
        return{
            'id': self.id,
            'bid_amount': self.bid_amount,
            'bid_time': self.bid_time,
            'item': self.item.id,
            'user': self.user.username,
        }