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
    progress_tickets = Ticket.objects.filter(
        status='In Progress').order_by('post_date').reverse()
    completed_tickets = Ticket.objects.filter(
        status='Done').order_by('post_date').reverse()
    invalid_tickets = Ticket.objects.filter(
        status='Invalid').order_by('post_date').reverse()

    return render(request, "index.html", {"new_tickets": new_tickets, "progress_tickets": progress_tickets, "completed_tickets": completed_tickets, "invalid_tickets": invalid_tickets})


def ticket_detail_view(request, ticket_id):
    my_ticket = Ticket.objects.filter(id=ticket_id).first()
    return render(request, "ticket_detail.html", {"ticket": my_ticket})


def user_detail_view(request, user_id):
    selected_user = MyUser.objects.filter(id=user_id).first()
    user_filed_tickets = Ticket.objects.filter(
        user_filed=selected_user).order_by('post_date').reverse()
    user_assigned_tickets = Ticket.objects.filter(
        user_assigned=selected_user).order_by('post_date').reverse()
    user_completed_tickets = Ticket.objects.filter(
        user_completed=selected_user).order_by('post_date').reverse()

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
    edit_ticket = Ticket.objects.filter(id=ticket_id).first()
    if request.method == "POST":
        form = AddTicketForm(request.POST, instance=edit_ticket)
        form.save()
        return HttpResponseRedirect(reverse("ticketview", args=[edit_ticket.id]))

    form = AddTicketForm(instance=edit_ticket)
    return render(request, "generic_form.html", {"form": form})


@login_required
def ticket_action_view(request, ticket_id, action_id):
    edit_ticket = Ticket.objects.filter(id=ticket_id).first()
    if action_id == 'assign':
        edit_ticket.user_assigned = request.user.username
        edit_ticket.status = 'In Progress'
        edit_ticket.save()

        return HttpResponseRedirect(reverse("ticketview", args=[edit_ticket.id]))

    if action_id == 'done':
        edit_ticket.user_assigned = 'None'
        edit_ticket.status = 'Done'
        edit_ticket.user_completed = request.user.username
        edit_ticket.save()

        return HttpResponseRedirect(reverse("ticketview", args=[edit_ticket.id]))

    if action_id == 'invalid':
        edit_ticket.user_assigned = 'None'
        edit_ticket.status = 'Invalid'
        edit_ticket.user_completed = request.user.username
        edit_ticket.save()

        return HttpResponseRedirect(reverse("ticketview", args=[edit_ticket.id]))

    if action_id == 'unassign':
        edit_ticket.user_assigned = 'None'
        edit_ticket.status = 'New'
        edit_ticket.user_completed = 'None'
        edit_ticket.save()

        return HttpResponseRedirect(reverse("ticketview", args=[edit_ticket.id]))

    if action_id == 'reopen':
        edit_ticket.user_assigned = request.user.username
        edit_ticket.status = 'In Progress'
        edit_ticket.save()

        return HttpResponseRedirect(reverse("ticketview", args=[edit_ticket.id]))

    return HttpResponseRedirect(reverse("ticketview", args=[edit_ticket.id]))


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("homepage"))
