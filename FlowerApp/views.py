import random

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from FlowerApp.forms import ConsultationRequestForm, OrderForm
from FlowerApp.models import ConsultationRequest, Bouquet, Store, Order, BouquetCategory, Budget
from FlowerApp.service import create_payment_order


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
            return redirect('index')
        bouquet = Bouquet.objects.get(pk=bouquet_id)
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            name = order_form.cleaned_data['name']
            phone_number = order_form.cleaned_data['phone_number']
            address = order_form.cleaned_data['address']
            delivery_time = order_form.cleaned_data['delivery_time']
            new_order = Order.objects.create(
                bouquet=bouquet,
                client_name=name,
                phone_number=phone_number,
                delivery_address=address,
                delivery_time=delivery_time)
            request.session.pop('bouquet_id', None)
            payment_url = create_payment_order(amount=bouquet.price, order_num=new_order.pk)
            return redirect(payment_url)
        return render(request, self.template_name, {'order_form': order_form})


def quiz(request):
    bouquet_categories = BouquetCategory.objects.all()
    return render(request, 'FlowerApp/quiz.html', {'bouquet_categories': bouquet_categories})


def quiz_step(request):
    category_name = request.POST.get('category_name')
    request.session['category_name'] = category_name
    budgets = Budget.objects.all()
    return render(request, 'FlowerApp/quiz-step.html', {'budgets': budgets})


def quiz_result(request):
    category_name = request.session.get('category_name')
    budget_level = request.POST.get('budget_level')
    consultation_request_form = ConsultationRequestForm(request.GET)

    if category_name == 'Без повода':
        bouquets_by_category = Bouquet.objects.all()
    else:
        bouquets_by_category = Bouquet.objects.filter(category__name=category_name)

    budget = Budget.objects.get(budget_level=budget_level)

    if budget_level == 'Не имеет значения':
        bouquets = bouquets_by_category.order_by('?')
    else:
        bouquets = bouquets_by_category.filter(
            Q(budget__budget_from__lte=budget.budget_from) & Q(budget__budget_up_to__gte=budget.budget_up_to)
        ).order_by('?')

    recommended_bouquet = random.choice(bouquets)

    store_context = [{
        'address': store.address,
        'phone': store.phone_number
    } for store in Store.objects.all()]

    bouquet_context = {
        'id': recommended_bouquet.pk,
        'name': recommended_bouquet.name,
        'price': recommended_bouquet.price,
        'description': recommended_bouquet.description,
        'small_description': recommended_bouquet.small_description,
        'image_path': request.build_absolute_uri(recommended_bouquet.image.url),
        'compound': recommended_bouquet.compound
    }

    context = {
        'store_context': store_context,
        'recommended_bouquet': bouquet_context,
        'consultation_request_form': consultation_request_form
    }
    return render(request, 'FlowerApp/result.html', context=context)


def order_confirmation(request):
    order_number = request.GET.get('order')
    order = Order.objects.get(pk=order_number)
    order.payment_status = True
    order.save()
    return redirect('index')
