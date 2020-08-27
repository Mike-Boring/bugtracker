from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib.auth import login, logout, authenticate
# from django.contrib.auth.decorators import login_required

from homepage.forms import LoginForm, AddTicketForm

from homepage.models import Ticket

# Create your views here.


def index(request):
    return render(request, "index.html")


def ticket_detail_view(request, ticket_id):
    my_ticket = Ticket.objects.filter(id=ticket_id).first()
    return render(request, "ticket_detail.html", {"ticket": my_ticket})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data.get(
                "username"), password=data.get("password"))
            if user:
                login(request, user)
                return HttpResponseRedirect(request.GET.get('next', reverse("homepage")))

    form = LoginForm()
    return render(request, "generic_form.html", {"form": form})


def add_ticket_view(request):
    if request.method == "POST":
        form = AddTicketForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            new_ticket = Ticket.objects.create(
                title=data.get('title'),
                description=data.get('description'),
                user_filed=request.user.username
            )
            return HttpResponseRedirect(reverse("ticketview", args=[new_ticket.id]))

    form = AddTicketForm()
    return render(request, "generic_form.html", {"form": form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("homepage"))
