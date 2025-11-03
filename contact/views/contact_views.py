from django.shortcuts import render
from contact.models import Contact
# from django.http import Http404
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator

def index(request):
    # contacts = Contact.objects.filter(show=True).order_by('-id')[0:10]
    contacts = Contact.objects.all().filter(show=True).order_by('-id')

    paginator = Paginator(contacts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        # 'contacts': contacts,
        'site_title': 'Contatos - ',
        'page_obj': page_obj
    }

    return render(
        request,
        'contact/index.html',
        context
    )

def search(request):
    search_value = request.GET.get('q').strip()

    if search_value:
        contacts = Contact.objects.filter(show=True).filter(Q(first_name__icontains=search_value)
                                                            | Q(last_name__icontains=search_value)
                                                            | Q(email__icontains=search_value)
                                                            | Q(phone__icontains=search_value)
                                                            ).order_by('-id')
    else:
        contacts = Contact.objects.filter(show=True).order_by('-id')
    # contacts = Contact.objects.filter(show=True).order_by('-id')[0:10]

    paginator = Paginator(contacts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'site_title': 'Search - ',
        'search_value': search_value
    }

    return render(
        request,
        'contact/index.html',
        context
    )

def contact(request, contact_id):
    # single_contact = Contact.objects.filter(pk=contact_id).first()

    # if single_contact is None:
    #     raise Http404('Contact not found')
    single_contact = get_object_or_404(Contact, pk=contact_id, show=True)

    site_title = f'{single_contact.first_name} {single_contact.last_name}'

    context = {
        'contact': single_contact,
        'site_title': f'{site_title} - ',
    }

    return render(
        request,
        'contact/contact.html',
        context
    )
