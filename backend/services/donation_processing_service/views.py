from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Mock database for demonstration purposes
donations = []

def create_donation(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            donation = {
                "id": len(donations) + 1,
                "amount": data.get("amount"),
                "donor": data.get("donor"),
                "cause": data.get("cause")
            }
            donations.append(donation)
            return JsonResponse({"message": "Donation created successfully", "donation": donation}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)

def get_donation_statistics(request):
    if request.method == 'GET':
        total_donations = sum(donation["amount"] for donation in donations)
        donation_count = len(donations)
        return JsonResponse({"total_donations": total_donations, "donation_count": donation_count}, status=200)
    return JsonResponse({"error": "Invalid request method"}, status=405)