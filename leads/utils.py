def calculate_match_score(lead, potential_match):
    score = 0

    # Location Matching (Stronger weight if exact, partial match gets lower score)
    if lead.location == potential_match.location:
        score += 40
    elif lead.location.split()[0] == potential_match.location.split()[0]:  # Matches first part of location
        score += 20

    # Property Type Matching (Ensures the desired type aligns)
    if lead.lead_type in ["buyer", "renter"] and lead.desired_property_type == potential_match.property_type:
        score += 20
    elif lead.lead_type in ["seller", "landlord"] and lead.property_type == potential_match.desired_property_type:
        score += 20

    # Price/Budget Matching with Percentage-Based Scoring
    if lead.lead_type == "buyer":
        budget_difference = abs(lead.budget - potential_match.price)
        budget_percentage_diff = (budget_difference / lead.budget) * 100 if lead.budget else 100

        if budget_percentage_diff == 0:
            score += 40
        elif budget_percentage_diff <= 5:
            score += 30
        elif budget_percentage_diff <= 10:
            score += 20
        elif budget_percentage_diff <= 20:
            score += 10

    elif lead.lead_type == "seller":
        price_difference = abs(lead.price - potential_match.budget)
        price_percentage_diff = (price_difference / lead.price) * 100 if lead.price else 100

        if price_percentage_diff == 0:
            score += 40
        elif price_percentage_diff <= 5:
            score += 30
        elif price_percentage_diff <= 10:
            score += 20
        elif price_percentage_diff <= 20:
            score += 10

    elif lead.lead_type == "renter":
        rent_difference = abs(lead.rent_budget - potential_match.rental_price)
        rent_percentage_diff = (rent_difference / lead.rent_budget) * 100 if lead.rent_budget else 100

        if rent_percentage_diff == 0:
            score += 40
        elif rent_percentage_diff <= 5:
            score += 30
        elif rent_percentage_diff <= 10:
            score += 20
        elif rent_percentage_diff <= 20:
            score += 10

    elif lead.lead_type == "landlord":
        rent_difference = abs(lead.rental_price - potential_match.rent_budget)
        rent_percentage_diff = (rent_difference / lead.rental_price) * 100 if lead.rental_price else 100

        if rent_percentage_diff == 0:
            score += 40
        elif rent_percentage_diff <= 5:
            score += 30
        elif rent_percentage_diff <= 10:
            score += 20
        elif rent_percentage_diff <= 20:
            score += 10

    # Additional Matching (e.g., bedrooms, property size, amenities)
    if hasattr(lead, "bedrooms") and hasattr(potential_match, "bedrooms"):
        if lead.bedrooms == potential_match.bedrooms:
            score += 10

    if hasattr(lead, "property_size") and hasattr(potential_match, "property_size"):
        size_difference = abs(lead.property_size - potential_match.property_size)
        if size_difference == 0:
            score += 10
        elif size_difference <= lead.property_size * 0.1:
            score += 5

    return min(score, 100)  # Ensure max score is capped at 100

