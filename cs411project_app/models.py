from django.db import models

class UserActivity(models.Model):
    user_email = models.EmailField()
    result = models.JSONField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_email} - {self.date_created}"
