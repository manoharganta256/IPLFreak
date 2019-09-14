from django.views import View
from django.shortcuts import render
from django.db.models import Sum, Count
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from math import floor
from iplfreak.models import Match, Deliveries, UserProfile
from iplfreak.forms import LoginForm, SignupForm, UserProfileForm


# Create your views here.
def index(request):
    return HttpResponseRedirect('/seasons/2019/')


def season_details(request, year):
    context = dict()

    matches = Match.objects.filter(season=year)[::-1]
    seasons = Match.objects.values('season').order_by('-season').distinct()
    special_matches = matches[:4]
    matches = matches[4:]

    context['matches'] = matches
    context['special_matches'] = special_matches
    context['seasons'] = seasons
    context['year'] = year
    context['total_matches'] = len(matches)

    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        context['profile_pic'] = user_profile.profile_picture

    return render(request, 'iplfreak/season_details.html', context)


@login_required()
def match_details(request, year, match_id):
    context = dict()

    match = Match.objects.get(match_id=match_id)
    deliveries = Deliveries.objects.filter(match_id=match_id).values('batting_team', 'bowling_team')

    context['match'] = match
    context['year'] = year
    context['extras'] = sum(
        extra['extra_runs'] for extra in Deliveries.objects.filter(match_id=match_id).values('extra_runs'))

    context['team_1'] = deliveries[0]['batting_team']
    context['team_2'] = deliveries[0]['bowling_team']

    context['team_1_deliveries'] = Deliveries.objects.filter(match_id=match_id, innings=1)
    context['team_2_deliveries'] = Deliveries.objects.filter(match_id=match_id, innings=2)

    context['top_batsmen_1'] = Deliveries.objects.filter(match_id=match_id, innings=1).values('batsman').annotate(
        total=Sum('batsman_runs')).order_by('-total')[:3]
    context['top_batsmen_2'] = Deliveries.objects.filter(match_id=match_id, innings=2).values('batsman').annotate(
        total=Sum('batsman_runs')).order_by('-total')[:3]

    context['top_bowler_1'] = Deliveries.objects.filter(match_id=match_id, innings=1).exclude(
        player_dismissed=None).values('bowler').annotate(total=Count('bowler')).order_by('-total')[:3]
    context['top_bowler_2'] = Deliveries.objects.filter(match_id=match_id, innings=2).exclude(
        player_dismissed=None).values('bowler').annotate(total=Count('bowler')).order_by('-total')[:3]

    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        context['profile_pic'] = user_profile.profile_picture

    return render(request, 'iplfreak/match_details.html', context)


class LoginController(View):
    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/seasons/2019/')

        login_form = LoginForm()
        return render(request, 'iplfreak/login.html', {
            'login_form': login_form
        })

    def post(self, request):
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            user = authenticate(
                request,
                username=login_form.cleaned_data['username'],
                password=login_form.cleaned_data['password']
            )

            if user is not None:
                login(request, user)
            else:
                messages.error(request, "Invalid Credentials")
        else:
            print(login_form.errors)

        return HttpResponseRedirect('/login/')


class SignupController(View):
    def get(self, request):
        signup_form = SignupForm()
        user_profile_form = UserProfileForm()
        return render(request, 'iplfreak/signup.html', {
            'signup_form': signup_form,
            'user_profile_form': user_profile_form
        })

    def post(self, request):
        signup_form = SignupForm(request.POST)
        user_profile_form = UserProfileForm(request.POST, request.FILES)

        if signup_form.is_valid() and user_profile_form.is_valid():
            new_user = User.objects.create_user(**signup_form.cleaned_data)

            user_profile_form = user_profile_form.save(commit=False)
            user_profile_form.user = User.objects.get(username=request.POST['username'])

            if not request.FILES:
                user_profile_form.profile_picture = 'profile_pictures/nopic.png'

            user_profile_form.save()

            login(request, user=new_user)
            return HttpResponseRedirect('/seasons/2019/')
        else:
            print(signup_form.errors, user_profile_form.errors)

        signup_form = SignupForm()
        return render(request, 'iplfreak/signup.html', {
            'signup_form': signup_form,
            'user_profile_form': user_profile_form
        })


@login_required()
def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/login/')


def points_table(request, year):
    context = dict()
    matches = Match.objects.filter(season=year)[::-1][4:] # removed non-league matches

    table = dict()
    for match in matches:
        if match.team1 not in table:
            table[match.team1] = 0

        if match.team2 not in table:
            table[match.team2] = 0

        if match.result == 'normal':
            table[match.winner] += 2
        else:
            table[match.team1] += 1
            table[match.team2] += 1

    context['points_table'] = sorted(table.items(), key=lambda x: x[1], reverse=True)

    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        context['profile_pic'] = user_profile.profile_picture

    context['year'] = year
    return render(request, 'iplfreak/points_table.html', context)


@login_required()
def teams(request, year):
    context = dict()
    context['teams'] = Match.objects.filter(season=year).values('team1').distinct()
    context['year'] = year

    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        context['profile_pic'] = user_profile.profile_picture

    return render(request, 'iplfreak/teams.html', context)


@login_required()
def team_details(request, year, team_name):
    context = dict()
    context['year'] = year
    context['team_name'] = team_name

    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        context['profile_pic'] = user_profile.profile_picture

    played = Match.objects.filter(Q(season=year) & (Q(team1=team_name) | Q(team2=team_name))).count()
    won = Match.objects.filter(Q(season=year) & Q(winner=team_name)).count()

    context['win_percentage'] = floor((won / played) * 100)
    context['played'] = played
    context['won'] = won

    context['best_players'] = Match.objects.filter(Q(season=year) & (Q(winner=team_name))).values('player_of_the_match').annotate(total=Count('player_of_the_match')).order_by('-total')
    context['recent_matches'] = Match.objects.filter(Q(season=year) & (Q(team1=team_name) | Q(team2=team_name)))[:3]
    context['best_batsman'] = Deliveries.objects.filter(Q(match_id__season=year) & Q(batting_team=team_name)).values('batsman').annotate(total=Count('batsman_runs')).order_by('-total')[:5]
    context['best_bowlers'] = Deliveries.objects.filter(Q(match_id__season=year) & Q(bowling_team=team_name)).exclude(player_dismissed__exact='').values('bowler').annotate(total=Count('player_dismissed')).order_by('-total')[:5]

    return render(request, 'iplfreak/team_details.html', context)
