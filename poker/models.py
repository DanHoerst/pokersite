from django.db import models
from django.forms import ModelForm
from django.conf import settings
from django.db.models import Sum
from django.contrib.auth.models import AbstractUser


class TotalsScreenameManager(models.Manager):
    def get_query_set(self):
        return super(TotalsScreenameManager, self).get_query_set().annotate(total_amount_won=Sum('sessions__profit'))

class PokerUser(AbstractUser):
    poker_relate = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
    token = models.EmailField(null=True, blank=True)
    USER_CHOICES = (
        ('1', 'Staker'),
        ('2', 'Horse')
    )
    user_type = models.CharField(choices=USER_CHOICES, max_length=10)

class Screename(models.Model):
    SITE_CHOICES = (
        ('FTP', 'Full Tilt Poker'),
        ('Stars', 'Pokerstars'),
        ('UB', 'Ultimate Bet'),
        ('Other', 'Other'),
        )
    player = models.ForeignKey(PokerUser)
    sites = models.CharField(choices=SITE_CHOICES, max_length=10)
    name = models.CharField(null=True, blank=True, max_length=40)

    objects = models.Manager()
    totals = TotalsScreenameManager()

class Sessions(models.Model):
    date = models.DateTimeField('Date Played')
    STAKE_CHOICES = (
        ('.10/.25', '25 NL'),
        ('.25/.50', '50 NL'),
        ('.50/1.00', '100 NL'),
        ('1/2', '200 NL'),
        ('2/4', '400 NL'),
        ('3/6', '600 NL'),
        ('4/8', '800 NL'),
        ('5/10', '1000 NL'),
        ('10/20', '2000 NL'),
        ('15/30', '3000 NL'),
        ('20/40', '4000 NL'),
        ('25/50', '5000 NL'),
        ('30/60', '6000 NL'),
        ('40/80', '8000 NL'),
        ('50/100', '10000 NL'),
        ('100/200', '20000 NL'),
        ('200/400', '40000 NL'),
        ('250/500', '50000 NL'),
        ('300/600', '60000 NL'),
        ('400/800', '80000 NL'),
        ('500/1000', '100000 NL'),
        )
    stakes = models.CharField(choices=STAKE_CHOICES, max_length=10)
    screename = models.ForeignKey(Screename)
    profit = models.DecimalField(max_digits=12, decimal_places=2)


class ScreenameForm(ModelForm):
    class Meta:
        model = Screename
        exclude = ('player',)

class SessionsForm(ModelForm):
    class Meta:
        model = Sessions
        exclude = ('screename',)