from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import Sum
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from .models import PokerUser, Screename, Sessions, SessionsForm, ScreenameForm
from .utils import paginate_me, user_relation


@login_required(login_url='/auth/login/')
def player_list(request):

    if request.user.user_type == '1':
        players = PokerUser.objects.filter(token=request.user.email).annotate(total_amount_won=Sum('screename__sessions__profit'))
    else:
        players = PokerUser.objects.get(email=request.user.email)
        url = reverse('screename_list', kwargs={'player_id': players.id,})
        return HttpResponseRedirect(url)

    player_list, paginator = paginate_me(request, players, 6)

    context = RequestContext(request)
    return render_to_response('poker/player_list.html', {"player_list": player_list, 'players': players,}, context_instance=context)

@login_required(login_url='/auth/login/')
def screename_list(request, player_id):

    owner = PokerUser.objects.get(id=player_id)
    if user_relation(request, owner):

        screenames = Screename.totals.filter(player__id=player_id)
        screenames_list, paginator = paginate_me(request, screenames, 15)
        context = RequestContext(request)
        return render_to_response('poker/screename_list.html', {"screenames_list": screenames_list, "screenames": screenames, "owner": owner,}, context_instance=context)
    else:
        return HttpResponseRedirect('/')

@login_required(login_url='/auth/login/')
def session_list(request, screename_id):

    owner = PokerUser.objects.get(screename__id__iexact = screename_id)
    if user_relation(request, owner):

        totals = Screename.totals.get(id=screename_id)
        sessions = totals.sessions_set.all()
        sessions_list, paginator = paginate_me(request, sessions, 15)

        context = RequestContext(request)
        return render_to_response('poker/sessions_list.html', {"sessions_list": sessions_list, "totals": totals,}, context_instance=context)
    else:
        return HttpResponseRedirect('/')

def new_screename(request, player_id):
    player = PokerUser.objects.get(id=player_id)
    screename = Screename(player = player)

    if request.method == 'POST':
        form = ScreenameForm(request.POST, instance=screename)
        if form.is_valid():
            screename.name = form.cleaned_data['name']
            screename.sites = form.cleaned_data['sites']
            screename.save()
            url = reverse('screename_list', kwargs={'player_id': request.user.id,})
            return HttpResponseRedirect(url)
    else:
        form = ScreenameForm()
    initialData = {'form': form}
    csrfContext = RequestContext(request, initialData)
    return render_to_response('poker/new_screename.html', csrfContext)

def new_session(request, screename_id):

    screename = Screename.objects.get(id=screename_id)
    session = Sessions(screename = screename)

    if request.method == 'POST':
        form = SessionsForm(request.POST, instance=session)
        if form.is_valid():
            session.date = form.cleaned_data['date']
            session.stakes = form.cleaned_data['stakes']
            session.profit = form.cleaned_data['profit']
            session.save()
            url = reverse('session_list', kwargs={'screename_id': screename_id,})
            return HttpResponseRedirect(url)
    else:
        form = SessionsForm()
    initialData = {'form': form}
    csrfContext = RequestContext(request, initialData)
    return render_to_response('poker/new_session.html', csrfContext)