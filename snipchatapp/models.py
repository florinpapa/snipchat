from django.db import models

class Users(models.Model):
  def __str__(self):
    return self.username
  name = models.CharField(max_length=50)
  username = models.CharField(max_length=15)

class Snippets(models.Model):
  def __str__(self):
    return self.identifier
  code = models.TextField()
  history = models.CharField(max_length="255", null=True)
  revision = models.IntegerField(default=0)
  user = models.ForeignKey(Users)
  identifier = models.CharField(max_length=10)
  pub_date = models.DateTimeField('date published')

class Comments(models.Model):
  def __str__(self):
    return self.comment
  comment = models.TextField()
  user = models.ForeignKey(Users)
  pub_date = models.DateTimeField('date published')
  row = models.CharField(max_length=3, default="0")
  snippet = models.ForeignKey(Snippets)
