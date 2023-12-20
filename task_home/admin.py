from django.contrib import admin
from task_home.models import User, Task, Team

# Register your models here.
admin.site.register(User)
admin.site.register(Task)
admin.site.register(Team)
