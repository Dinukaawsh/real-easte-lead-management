from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import LeadForm  
import openpyxl
from .models import Lead
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .utils import calculate_match_score




# Home Page
def index(request):
    return render(request, 'index.html')

# Login View
@csrf_exempt
def custom_login(request):
    if request.user.is_authenticated:
        return redirect('lead_list')  # Redirect logged-in users

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('lead_list')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'auth/login.html')


def logout_view(request):
    print("Before logout:", request.user)  # Debug: Print current user
    logout(request)
    print("After logout:", request.user)  # Debug: Should now be AnonymousUser
    request.session.flush()  
    return redirect('index')



# View All Leads
@login_required
def lead_list(request):
    leads = Lead.objects.all()
    return render(request, 'leads/lead_list.html', {'leads': leads})



def add_lead(request):
    form = LeadForm(request.POST or None)

    if request.method == 'POST':
        print(request.POST)  # Log the form data submitted
        if form.is_valid():
            form.save()
            return redirect('lead_list')  # Redirect to lead list page after success
        else:
            print(form.errors)  # Log form errors to debug

    return render(request, 'leads/add_lead.html', {'form': form})


# Update a Lead
@login_required
def update_lead(request, id):
    lead = get_object_or_404(Lead, id=id)
    if request.method == "POST":
        form = LeadForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            return redirect('lead_list')
    else:
        form = LeadForm(instance=lead)
    return render(request, 'leads/update_lead.html', {'form': form, 'lead': lead})


# View for the lead list
def lead_list(request):
    leads = Lead.objects.all()

    # Search filter
    search_query = request.GET.get('search', '')
    if search_query:
        leads = leads.filter(name__icontains=search_query)

    # Lead type filter
    lead_type = request.GET.get('lead_type', '')
    if lead_type:
        leads = leads.filter(lead_type=lead_type)

    # Sort filter
    sort_by = request.GET.get('sort_by', '')
    if sort_by:
        if sort_by == 'name':
            leads = leads.order_by('name')
        elif sort_by == 'location':
            leads = leads.order_by('location')
        elif sort_by == 'price':
            leads = leads.order_by('price')  # Assuming price for sellers or buyers

    # Sorting by created_at to show the latest leads first by default
    leads = leads.order_by('-created_at')

    return render(request, 'leads/lead_list.html', {
        'leads': leads,
        'search_query': search_query,
        'lead_type': lead_type,
        'sort_by': sort_by,
    })



def delete_lead(request, id):
    lead = get_object_or_404(Lead, id=id)
    lead.delete()
    return redirect('lead_list')  # Redirect to the lead list after deletion



def lead_detail(request, id):
    lead = get_object_or_404(Lead, id=id)

    # Debugging
    print(f"Lead Type: {lead.lead_type}")
    print(f"Property Type: {lead.property_type}")
    print(f"Location: {lead.location}")

    matches = None  # Initialize matches

    # Filtering based on the lead type and property type
    if lead.lead_type == "seller":
        matches = Lead.objects.filter(
            lead_type="buyer",
            desired_property_type=lead.property_type,
            location=lead.location
        )
    elif lead.lead_type == "buyer":
        matches = Lead.objects.filter(
            lead_type="seller",
            property_type=lead.desired_property_type,
            location=lead.location
        )
    elif lead.lead_type == "renter":
        matches = Lead.objects.filter(
            lead_type="landlord",
            property_type=lead.desired_property_type,
            location=lead.location
        )
    elif lead.lead_type == "landlord":
        matches = Lead.objects.filter(
            lead_type="renter",
            desired_property_type=lead.property_type,
            location=lead.location
        )

    # Debugging matches found
    print(f"Matches found: {matches.count()}")

    if not matches:
        # Handle case where no matches are found
        print("No matches found.")
        context = {
            "lead": lead,
            "matches": [],  # No matches to show
        }
        return render(request, "leads/lead_detail.html", context)

    # Calculate match scores
    matches_with_scores = []
    for match in matches:
        score = calculate_match_score(lead, match)  # Assuming this function is defined
        if score is not None:
            matches_with_scores.append({'lead': match, 'score': score})

    # Sort matches by highest score (only if matches are available)
    matches_with_scores.sort(key=lambda x: x['score'], reverse=True)

    # Debugging sorted matches
    print(f"Matches sorted by score: {matches_with_scores}")

    # Pass matches_with_scores to the template
    context = {
        "lead": lead,
        "matches": matches_with_scores,  # Use matches_with_scores for the template
    }
    return render(request, "leads/lead_detail.html", context)



def download_leads_excel(request):
    # Create a new workbook and set the active sheet
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Leads"

    # Define column headers
    headers = [
        "ID", "Name", "Lead Type", "Location", "Price", "Budget",
        "Desired Property Type", "Property Type", "Rental Price", "Date Added"
    ]
    ws.append(headers)

    # Fetch all leads from the database
    leads = Lead.objects.all()

    # Populate the Excel sheet with lead data
    for lead in leads:
        lead_data = [
            str(lead.id),  # Convert UUID to string
            lead.name,
            lead.get_lead_type_display(),  # Convert lead type choice field to display value
            lead.location,
            lead.price if lead.lead_type == 'seller' else "",  # Show price for sellers
            lead.budget if lead.lead_type == 'buyer' else "",  # Show budget for buyers
            lead.desired_property_type if lead.lead_type in ['buyer', 'renter'] else "",  # Show desired property type
            lead.property_type if lead.lead_type in ['seller', 'landlord'] else "",  # Show property type
            lead.rental_price if lead.lead_type == 'landlord' else "",  # Show rental price for landlords
            lead.created_at.strftime('%Y-%m-%d %H:%M:%S')  # Format the date
        ]
        ws.append(lead_data)

    # Create an HTTP response with the Excel file
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=leads.xlsx'
    wb.save(response)

    return response