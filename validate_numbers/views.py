# validate_numbers/views.py

from django.shortcuts import render, redirect
from django.http import HttpResponse
import phonenumbers
from phonenumbers import geocoder, carrier, timezone

def index(request):
    return render(request, 'phone_number_form.html')

def process_phone_number(request):
    context = {}  # Initialize the context dictionary

    if request.method == 'POST':
        phone_number = request.POST.get('phone_number', '')

        try:
            parsed_number = phonenumbers.parse(phone_number, None)
            if phonenumbers.is_valid_number(parsed_number):
                context['is_valid'] = True
                context['formatted_number'] = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
                context['country_code'] = parsed_number.country_code
                context['national_number'] = parsed_number.national_number
                context['region'] = phonenumbers.region_code_for_number(parsed_number)
                context['country'] = geocoder.description_for_number(parsed_number, "en")
                context['carrier'] = carrier.name_for_number(parsed_number,"en")
                context['timezone'] = timezone.time_zones_for_number(parsed_number)
            else:
                context['is_valid'] = False
                context['error'] = "Invalid phone number."
        except phonenumbers.NumberParseException:
            context['is_valid'] = False
            context['error'] = "Error parsing phone number."
        return render(request, 'phone_number_form.html', context)

    # If GET request or form is invalid, only the form will be rendered
    return redirect('index')
