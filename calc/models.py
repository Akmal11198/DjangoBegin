from django.db import models

# Create your models here.


class User(models.Model):
    name=models.CharField(max_length=50,primary_key=True)
    password=models.CharField(max_length=20)

class Post(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    content=models.TextField(default=' ')
    genre=models.CharField(max_length=20)    

class Comment(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)    
    content=models.TextField(default=' ')
    post=models.ForeignKey(Post,on_delete=models.CASCADE)