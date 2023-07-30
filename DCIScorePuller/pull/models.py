from django.db import models

# Create your models here.
class Corp(models.Model):
    key = models.AutoField(primary_key=True)
    name = models.TextField(default="No Corp Name Provided")

class Show(models.Model):
    key = models.AutoField(primary_key=True)
    competition_name = models.TextField(default="No Show Name Provided")
    corp = models.ForeignKey(Corp, on_delete=models.RESTRICT)
    general_effect_total = models.DecimalField(default=0.0)
    visual_total = models.DecimalField(default=0.0)
    music_total = models.DecimalField(default=0.0)