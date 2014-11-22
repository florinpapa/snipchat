from django.db import models

class Users(models.Model):
  def __str__(self):
    return self.username
  name = models.CharField(max_length=50)
  username = models.CharField(max_length=15)

class Comments(models.Model):
  def __str__(self):
    return self.comment
  comment = models.TextField()
  user = models.ForeignKey(Users)
  pub_date = models.DateTimeField('date published')

class Snippets(models.Model):
  def __str__(self):
    return self.identifier
  code = models.TextField()
  revision = models.IntegerField(default=0)
  user = models.ForeignKey(Users)
  comments = models.ForeignKey(Comments, blank=True, null=True)
  identifier = models.CharField(max_length=10)
  pub_date = models.DateTimeField('date published')
