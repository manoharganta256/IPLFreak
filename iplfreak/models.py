from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Match(models.Model):
    match_id = models.IntegerField(primary_key=True)
    season = models.IntegerField()
    city = models.CharField(max_length=64, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    team1 = models.CharField(max_length=64, null=True, blank=True)
    team2 = models.CharField(max_length=64, null=True, blank=True)
    toss_winner = models.CharField(max_length=64, null=True, blank=True)
    toss_decision = models.IntegerField()  # 1 - bat, 2 - field
    result = models.CharField(max_length=10, null=True, blank=True)
    dl_applied = models.BooleanField()
    winner = models.CharField(max_length=64, null=True, blank=True)
    win_by_runs = models.IntegerField()
    win_by_wickets = models.IntegerField()
    player_of_the_match = models.CharField(max_length=64, null=True, blank=True)
    venue = models.CharField(max_length=64, null=True, blank=True)
    umpire1 = models.CharField(max_length=64, null=True, blank=True)
    umpire2 = models.CharField(max_length=64, null=True, blank=True)

    def __str__(self):
        return str(self.match_id)


class Deliveries(models.Model):
    match_id = models.ForeignKey(Match, on_delete=models.CASCADE)
    innings = models.IntegerField()
    batting_team = models.CharField(max_length=64, null=True, blank=True)
    bowling_team = models.CharField(max_length=64, null=True, blank=True)
    over = models.IntegerField()
    ball = models.IntegerField()
    batsman = models.CharField(max_length=64, null=True, blank=True)
    non_striker = models.CharField(max_length=64, null=True, blank=True)
    bowler = models.CharField(max_length=64, null=True, blank=True)
    is_super_over = models.BooleanField(default=0)
    wide_runs = models.IntegerField(default=0)
    bye_runs = models.IntegerField(default=0)
    legbye_run = models.IntegerField(default=0)
    noball_runs = models.IntegerField(default=0)
    penalty_runs = models.IntegerField(default=0)
    batsman_runs = models.IntegerField(default=0)
    extra_runs = models.IntegerField(default=0)
    totals = models.IntegerField(default=0)
    player_dismissed = models.CharField(max_length=64, null=True, blank=True)
    # todo: change dismissal max_length
    dismissal_kind = models.CharField(max_length=16, null=True, blank=True)
    fielder = models.CharField(max_length=16, null=True, blank=True)

    def __str__(self):
        return '{0}-{1}'.format(self.match_id, self.innings)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures', blank=True)

    def __str__(self):
        return self.user.username
