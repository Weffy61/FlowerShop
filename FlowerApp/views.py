from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from FlowerApp.forms import ConsultationRequestForm
from FlowerApp.models import ConsultationRequest, Bouquet


def index(request):
    consultation_request_form = ConsultationRequestForm(request.GET)
    return render(request, 'FlowerApp/index.html', {'consultation_request_form': consultation_request_form})


def order(request):
    return render(request, 'FlowerApp/order.html')


def card(request, bouquet_id):
    bouquet = get_object_or_404(Bouquet, pk=bouquet_id)
    consultation_request_form = ConsultationRequestForm(request.GET)
    bouquet_context = {
        'name': bouquet.name,
        'price': bouquet.price,
        'compound': bouquet.compound,
        'height': bouquet.size_height,
        'width': bouquet.size_width,
        'img_path': request.build_absolute_uri(bouquet.image.url)
    }
    context = {
        'bouquet_context': bouquet_context,
        'consultation_request_form': consultation_request_form
    }

    return render(request, 'FlowerApp/card.html', context=context)


def catalog(request):
    consultation_request_form = ConsultationRequestForm(request.GET)
    bouquets = Bouquet.objects.all().order_by('pk')
    paginator = Paginator(bouquets, 6)
    page_number = request.GET.get('page', 1)
    try:
        bouquets_page = paginator.page(page_number)
    except PageNotAnInteger:
        bouquets_page = paginator.page(1)
    except EmptyPage:
        bouquets_page = paginator.page(paginator.num_pages)

    bouquet_context = [{
        'bouquet_id': bouquet.pk,
        'name': bouquet.name,
        'price': bouquet.price,
        'img_path': request.build_absolute_uri(bouquet.image.url)
    } for bouquet in bouquets_page.object_list]

    context = {
        'bouquets_page': bouquets_page,
        'bouquet_context': bouquet_context,
        'consultation_request_form': consultation_request_form
    }
    return render(request, 'FlowerApp/catalog.html', context=context)


class ConsultationRequestView(View):
    template_name = 'FlowerApp/consultation.html'

    def get(self, request):
        consultation_request_form = ConsultationRequestForm(request.GET)
        return render(request, self.template_name, {'consultation_request_form': consultation_request_form})

    def post(self, request):
        consultation_request_form = ConsultationRequestForm(request.POST)
        if consultation_request_form.is_valid():
            name = consultation_request_form.cleaned_data['name']
            phone_number = consultation_request_form.cleaned_data['phone_number']
            ConsultationRequest.objects.create(name=name, phone_number=phone_number)
            return redirect('index')
        return render(request, self.template_name, {'consultation_request_form': consultation_request_form})

