from django.views import View
from django.shortcuts import render
from django.db.models import Sum, Count
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from iplfreak.models import Match, Deliveries, UserProfile
from iplfreak.forms import LoginForm, SignupForm, UserProfileForm


# Create your views here.
def season_details(request, year):
    context = dict()

    matches = Match.objects.filter(season=year)
    seasons = Match.objects.values('season').order_by('-season').distinct()

    context['matches'] = matches
    context['seasons'] = seasons
    context['year'] = year

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
            return HttpResponseRedirect('/seasons/2017/')

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
    context['points_table'] = Match.objects.filter(season=year).values('winner').annotate(
        total=Count('winner')).order_by('-total')

    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        context['profile_pic'] = user_profile.profile_picture

    context['year'] = year
    return render(request, 'iplfreak/points_table.html', context)
