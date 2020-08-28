from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from homepage.forms import LoginForm, AddTicketForm
from myuser.models import MyUser
from homepage.models import Ticket

# Create your views here.


def index(request):
    new_tickets = Ticket.objects.filter(
        status='New').order_by('post_date').reverse()
    progress_tickets = Ticket.objects.filter(status='InProgress')
    completed_tickets = Ticket.objects.filter(status='Done')
    invalid_tickets = Ticket.objects.filter(status='Invalid')

    return render(request, "index.html", {"new_tickets": new_tickets, "progress_tickets": progress_tickets, "completed_tickets": completed_tickets, "invalid_tickets": invalid_tickets})


def ticket_detail_view(request, ticket_id):
    my_ticket = Ticket.objects.filter(id=ticket_id).first()
    return render(request, "ticket_detail.html", {"ticket": my_ticket})


def user_detail_view(request, user_id):
    selected_user = MyUser.objects.filter(id=user_id).first()
    user_filed_tickets = Ticket.objects.filter(user_filed=selected_user)
    user_assigned_tickets = Ticket.objects.filter(user_assigned=selected_user)
    user_completed_tickets = Ticket.objects.filter(
        user_completed=selected_user)

    return render(request, "user_detail.html", {"selected_user": selected_user, "filed_tickets": user_filed_tickets, "assigned_tickets": user_assigned_tickets, "completed_tickets": user_completed_tickets})


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


@login_required
def add_ticket_view(request):
    if request.method == "POST":
        form = AddTicketForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            new_ticket = Ticket.objects.create(
                title=data.get('title'),
                description=data.get('description'),
                user_filed=request.user
            )
            # breakpoint()
            return HttpResponseRedirect(reverse("ticketview", args=[new_ticket.id]))

    form = AddTicketForm()
    return render(request, "generic_form.html", {"form": form})


@login_required
def ticket_edit_view(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
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

    data = {
        "title": ticket.title,
        "description": ticket.description
    }
    form = AddTicketForm(initial=data)
    return render(request, "generic_form.html", {"form": form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("homepage"))
