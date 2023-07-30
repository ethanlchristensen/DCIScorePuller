from django.db import models
from django.utils.timezone import now
from django.utils import timezone as dut

# Create your models here.
class Corp(models.Model):
    key = models.AutoField(primary_key=True)
    name = models.TextField(default="No Corp Name Provided")

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        return self

class Competition(models.Model):
    key = models.AutoField(primary_key=True)
    competition_name = models.TextField(default="No Competition Name Provided")
    competition_name_original = models.TextField(default="No Original Competition Name Provided")
    competition_date = models.DateField(default=dut.now)
    competition_date_as_string = models.TextField(default="")

    def __str__(self):
        return self.competition_name_original
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        return self

class RepPerfTotal(models.Model):
    key = models.AutoField(primary_key=True)
    rep = models.DecimalField(default=0.0, decimal_places=3, max_digits=6)
    perf = models.DecimalField(default=0.0, decimal_places=3, max_digits=6)
    total = models.DecimalField(default=0.0, decimal_places=3, max_digits=6)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        return self

    def __str__(self):
        return f"RPT-{self.key}"

class ContAchvTotal(models.Model):
    key = models.AutoField(primary_key=True)
    cont = models.DecimalField(default=0.0, decimal_places=3, max_digits=6)
    achv = models.DecimalField(default=0.0, decimal_places=3, max_digits=6)
    total = models.DecimalField(default=0.0, decimal_places=3, max_digits=6)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        return self

    def __str__(self):
        return f"CAT-{self.key}"

class GeneralEffect(models.Model):
    key = models.AutoField(primary_key=True)
    general_effect_one_one = models.ForeignKey(RepPerfTotal, on_delete=models.CASCADE, related_name="general_effect_one_one")
    general_effect_one_two = models.ForeignKey(RepPerfTotal, on_delete=models.CASCADE, related_name="general_effect_one_two", null=True)
    general_effect_two_one = models.ForeignKey(RepPerfTotal, on_delete=models.CASCADE, related_name="general_effect_two_one")
    general_effect_two_two = models.ForeignKey(RepPerfTotal, on_delete=models.CASCADE, related_name="general_effect_two_two", null=True)
    general_effect_total = models.DecimalField(default=0.0, decimal_places=3, max_digits=6)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        return self

    def __str__(self):
        return f"GeneralEffect-{self.key}"

class Visual(models.Model):
    key = models.AutoField(primary_key=True)
    visual_proficiency = models.ForeignKey(ContAchvTotal, on_delete=models.CASCADE, related_name="visual_proficiency")
    visual_analysis = models.ForeignKey(ContAchvTotal, on_delete=models.CASCADE, related_name="visual_analysis")
    color_guard = models.ForeignKey(ContAchvTotal, on_delete=models.CASCADE, related_name="color_guard")
    visual_total = models.DecimalField(default=0.0, decimal_places=3, max_digits=6)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        return self
    
    def __str__(self):
        return f"Visual-{self.key}"

class Music(models.Model):
    key = models.AutoField(primary_key=True)
    music_brass = models.ForeignKey(ContAchvTotal, on_delete=models.CASCADE, related_name="music_brass")
    music_analysis_one = models.ForeignKey(ContAchvTotal, on_delete=models.CASCADE, related_name="music_analysis_one")
    music_analysis_two = models.ForeignKey(ContAchvTotal, on_delete=models.CASCADE, related_name="music_analysis_two", null=True)
    music_percussion = models.ForeignKey(ContAchvTotal, on_delete=models.CASCADE, related_name="music_percussion")
    music_total = models.DecimalField(default=0.0, decimal_places=3, max_digits=6)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        return self
    
    def __str__(self):
        return f"Music-{self.key}"

class Show(models.Model):
    key = models.AutoField(primary_key=True)
    competition = models.ForeignKey(Competition, on_delete=models.RESTRICT, related_name="competition")
    corp = models.ForeignKey(Corp, on_delete=models.RESTRICT, related_name="corp")
    general_effect = models.ForeignKey(GeneralEffect, on_delete=models.CASCADE, related_name="general_effect")
    visual = models.ForeignKey(Visual, on_delete=models.CASCADE, related_name="visual")
    music = models.ForeignKey(Music, on_delete=models.CASCADE, related_name="music")
    total_score = models.DecimalField(default=0.0, decimal_places=3, max_digits=6)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        return self

    def __str__(self):
        return f"{self.competition.competition_name}-{self.corp.name}"

    def get_date(self):
        return self.competition.competition_date