document.addEventListener("DOMContentLoaded", function () {
    function updateFields() {
        var leadType = document.querySelector("#id_lead_type").value;

        // Hide all conditional fields
        var allFields = ["price", "property_type", "budget", "rent_budget", "desired_property_type", "rental_price"];
        allFields.forEach(function (field) {
            var fieldRow = document.querySelector(".form-row.field-" + field);
            if (fieldRow) {
                fieldRow.style.display = "none";
            }
        });

        // Show fields based on selected lead type
        if (leadType === "seller") {
            showFields(["price", "property_type"]);
        } else if (leadType === "buyer") {
            showFields(["budget"]);
        } else if (leadType === "renter") {
            showFields(["rent_budget", "desired_property_type"]);
        } else if (leadType === "landlord") {
            showFields(["rental_price", "property_type"]);
        }
    }

    function showFields(fields) {
        fields.forEach(function (field) {
            var fieldRow = document.querySelector(".form-row.field-" + field);
            if (fieldRow) {
                fieldRow.style.display = "";
            }
        });
    }

    // Attach event listener to lead type dropdown
    var leadTypeField = document.querySelector("#id_lead_type");
    if (leadTypeField) {
        leadTypeField.addEventListener("change", updateFields);
    }

    // Run on page load
    updateFields();
});
