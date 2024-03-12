from django.shortcuts import render, redirect
from django.views import View

from FlowerApp.forms import ConsultationRequestForm
from FlowerApp.models import ConsultationRequest


def index(request):
    return render(request, 'FlowerApp/index.html')


def order(request):
    return render(request, 'FlowerApp/order.html')


def catalog(request):
    return render(request, 'FlowerApp/catalog.html')


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

