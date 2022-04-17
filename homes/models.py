from django.db import models

class Home(models.Model):
    """Custom Home Model"""
    home_id = models.BigAutoField(primary_key=True)