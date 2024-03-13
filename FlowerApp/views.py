from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from FlowerApp.forms import ConsultationRequestForm, OrderForm
from FlowerApp.models import ConsultationRequest, Bouquet, Store, Order


def index(request):
    consultation_request_form = ConsultationRequestForm(request.GET)

    bouquet_context = [{
        'bouquet_id': bouquet.pk,
        'name': bouquet.name,
        'price': bouquet.price,
        'img_path': request.build_absolute_uri(bouquet.image.url)
    } for bouquet in Bouquet.objects.order_by('?')[:3]]

    store_context = [{
        'address': store.address,
        'phone': store.phone_number
    } for store in Store.objects.all()]

    context = {
        'bouquet_context': bouquet_context,
        'consultation_request_form': consultation_request_form,
        'store_context': store_context
    }

    return render(request, 'FlowerApp/index.html', context=context)


def card(request, bouquet_id):
    bouquet = get_object_or_404(Bouquet, pk=bouquet_id)
    consultation_request_form = ConsultationRequestForm(request.GET)
    request.session['bouquet_id'] = bouquet.pk
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


class OrderView(View):
    template_name = 'FlowerApp/order.html'

    def get(self, request):
        bouquet_id = request.session.get('bouquet_id')
        if not bouquet_id:
            return redirect('/')
        order_form = OrderForm(request.GET)
        context = {
            'order_form': order_form
        }
        return render(request, self.template_name, context)

    def post(self, request):
        bouquet_id = request.session.get('bouquet_id')
        if not bouquet_id:
            return redirect('/')
        bouquet = Bouquet.objects.get(pk=bouquet_id)
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            name = order_form.cleaned_data['name']
            phone_number = order_form.cleaned_data['phone_number']
            address = order_form.cleaned_data['address']
            delivery_time = order_form.cleaned_data['delivery_time']
            Order.objects.create(
                bouquet=bouquet,
                client_name=name,
                phone_number=phone_number,
                delivery_address=address,
                delivery_time=delivery_time)
            return redirect('/')
        return render(request, self.template_name, {'order_form': order_form})


def quiz(request):
    return render(request, 'FlowerApp/quiz.html')
