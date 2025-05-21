from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Competition(models.Model):
    COMPETITION_TYPES = (
        ('kumite', 'Kumite'),
        ('kata', 'Kata'),
        ('individual', 'Individual'),
        ('team', 'Por Equipes'),
    )
    
    name = models.CharField(max_length=200)
    competition_type = models.CharField(max_length=20, choices=COMPETITION_TYPES)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Category(models.Model):
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=100)
    min_age = models.IntegerField(null=True, blank=True)
    max_age = models.IntegerField(null=True, blank=True)
    min_weight = models.FloatField(null=True, blank=True)  # em kg
    max_weight = models.FloatField(null=True, blank=True)  # em kg
    belt_min = models.CharField(max_length=50, null=True, blank=True)
    belt_max = models.CharField(max_length=50, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=(('male', 'Masculino'), ('female', 'Feminino'), ('mixed', 'Misto')), default='mixed')
    
    def __str__(self):
        return f"{self.name} - {self.competition.name}"

class Athlete(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='athlete_profile')
    date_of_birth = models.DateField()
    weight = models.FloatField()  # em kg
    belt = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.belt}"

class Registration(models.Model):
    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    registration_date = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('athlete', 'category')
    
    def __str__(self):
        return f"{self.athlete} - {self.category}"

class Match(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    athlete1 = models.ForeignKey(Athlete, on_delete=models.CASCADE, related_name='matches_as_athlete1')
    athlete2 = models.ForeignKey(Athlete, on_delete=models.CASCADE, related_name='matches_as_athlete2', null=True, blank=True)
    scheduled_time = models.DateTimeField()
    round = models.IntegerField()
    winner = models.ForeignKey(Athlete, on_delete=models.SET_NULL, null=True, blank=True, related_name='won_matches')
    score_athlete1 = models.IntegerField(default=0)
    score_athlete2 = models.IntegerField(default=0)
    is_completed = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.category}: {self.athlete1} vs {self.athlete2 or 'TBD'}"