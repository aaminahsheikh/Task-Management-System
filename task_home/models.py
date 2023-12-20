from django.db import models

from task_home.base.base_model import BaseModel


# Create your models here.
class User(BaseModel):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.username


class Task(BaseModel):
    STATUS_CHOICES = [
        ('New', 'New'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    due_date = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='assigned_tasks')

    def __str__(self):
        return self.title


class Team(BaseModel):
    name = models.CharField(max_length=255)
    members = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="teams")

    def __str__(self):
        return self.name
