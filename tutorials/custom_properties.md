## Handling Custom HubSpot Properties (Detailed)

HubSpot's flexibility allows you to define custom properties for Contacts, Companies, and Tickets. The `hubspot-connector` is designed to automatically handle these custom properties without requiring any modifications to the connector's codebase.

When sending data to any of the API endpoints (`/contacts`, `/companies`, `/tickets`), simply include the custom property's **internal name** (as defined in your HubSpot portal) and its corresponding value directly in the JSON request body. The connector's Pydantic models are configured to accept these additional fields, and they will be seamlessly passed to the HubSpot API.

**Important:** Ensure you use the exact internal name of the custom property from HubSpot. You can find this in your HubSpot portal under Settings > Properties.

**Example for a Contact with Custom Properties:**

```json
{
    "email": "jane.doe@example.com",
    "firstname": "Jane",
    "lastname": "Doe",
    "account_record_type": "Customer", 
    "my_custom_text_field": "This is a custom text value",
    "number_of_employees": 50 
}
```

**Example for a Company with Custom Properties:**

```json
{
    "name": "Global Innovations Inc.",
    "domain": "globalinnovations.com",
    "annual_revenue": 10000000, 
    "company_type": "Enterprise"
}
```

**Example for a Ticket with Custom Properties:**

```json
{
    "hs_pipeline": "0",
    "hs_pipeline_stage": "1",
    "subject": "Login Issue",
    "priority_level": "Urgent", 
    "affected_system": "Website"
}
```