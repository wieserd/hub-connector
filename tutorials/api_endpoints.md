## API Endpoints

The `hubspot-connector` exposes the following RESTful API endpoints:

### Generic CRUD Endpoints

The following endpoints are dynamically generated for HubSpot objects like `contacts`, `companies`, and `tickets`.

#### `POST /{object_type}`

**Purpose:** Creates a new HubSpot object or updates an existing one based on a unique identifier (email for contacts, domain for companies). If an object with the given identifier already exists, its properties will be updated with the provided data. Otherwise, a new object will be created.

**Path Parameters:**
*   `object_type` (string, required): The type of the HubSpot object (e.g., `contacts`, `companies`, `tickets`).

**Request Body (JSON Example for `POST /contacts`):**

```json
{
    "email": "john.doe@example.com",
    "firstname": "John",
    "lastname": "Doe",
    "phone": "123-456-7890",
    "company": "Example Corp",
    "my_custom_contact_property": "Custom Value Here" 
}
```
*   For `contacts`, `email` is used for identification.
*   For `companies`, `domain` is used for identification.
*   For `tickets`, a new ticket is always created as there is no unique identifier for searching existing tickets in the current implementation.
*   **Any other fields** will be treated as custom HubSpot properties and passed through directly.

**Success Response (HTTP 200 OK - JSON Example):**

```json
{
    "status": "success",
    "message": "Contact created/updated successfully",
    "hubspot_contact_id": "123456789",
    "action": "created" 
}
```
*   `action` will be `"created"` if a new object was made, or `"updated"` if an existing one was modified.
*   `hubspot_{object_type}_id` will contain the ID of the created or updated HubSpot object.

**Error Response (HTTP 4xx/5xx - JSON Example):**

```json
{
    "detail": "Error message from HubSpot or internal server error details"
}
```

#### `GET /{object_type}/{object_id}`

**Purpose:** Retrieves a HubSpot object by its unique ID.

**Path Parameters:**
*   `object_type` (string, required): The type of the HubSpot object (e.g., `contacts`, `companies`, `tickets`).
*   `object_id` (string, required): The unique ID of the HubSpot object.

**Success Response (JSON Example for `GET /contacts/{contact_id}`):**

```json
{
    "id": "123456789",
    "properties": {
        "email": "john.doe@example.com",
        "firstname": "John",
        "lastname": "Doe",
        "phone": "123-456-7890",
        "company": "Example Corp",
        "my_custom_contact_property": "Custom Value Here"
    },
    "createdAt": "2023-01-01T12:00:00.000Z",
    "updatedAt": "2023-01-01T12:00:00.000Z",
    "archived": false
}
```

**Error Response (HTTP 404 Not Found - JSON Example):**

```json
{
    "detail": "Contact not found"
}
```

**Error Response (HTTP 4xx/5xx - JSON Example):**

```json
{
    "detail": "Error message from HubSpot or internal server error details"
}
```

### Specific Endpoints

#### `POST /webhooks/hubspot`

**Purpose:** Receives webhook events from HubSpot. This endpoint is where HubSpot will send notifications about changes in your CRM (e.g., contact updates, new deals).

**Request Body (JSON Example - HubSpot Webhook Event):**

```json
[
  {
    "eventId": 123456789,
    "subscriptionId": 987654321,
    "portalId": 123456,
    "appId": 789012,
    "occurredAt": "2023-07-06T12:34:56.789Z",
    "subscriptionType": "contact.propertyChange",
    "attemptNumber": 1,
    "objectId": 54321,
    "changeFlag": "NEW",
    "changeSource": "CRM",
    "propertyName": "email",
    "propertyValue": "new.email@example.com",
    "rawBody": "..."
  }
]
```
*   This endpoint expects a list of HubSpot webhook event objects. The structure of these objects varies based on the `subscriptionType`.

**Success Response (HTTP 200 OK - JSON Example):**

```json
{
    "status": "success",
    "message": "Received X events"
}
```

**Error Response (HTTP 4xx/5xx - JSON Example):**

```json
{
    "detail": "Error message or internal server error details"
}
```

**Important Note on Security:**

In a production environment, it is **CRITICAL** to verify the `X-HubSpot-Signature` header sent with each webhook request. This ensures that the request genuinely originated from HubSpot and has not been tampered with. The current implementation includes commented-out code in `routers/webhooks.py` that demonstrates how to perform this verification. You will need to uncomment and enable this for production use.

#### `POST /associations`

**Purpose:** Creates an association between two HubSpot objects.

**Request Body (JSON Example):**

```json
{
    "from_object_type": "contact",
    "from_object_id": "123",
    "to_object_type": "company",
    "to_object_id": "456",
    "association_type_id": "279" 
}
```
*   `from_object_type` (string, required): The type of the first object (e.g., "contact", "company", "ticket").
*   `from_object_id` (string, required): The ID of the first object.
*   `to_object_type` (string, required): The type of the second object.
*   `to_object_id` (string, required): The ID of the second object.
*   `association_type_id` (string, required): The ID of the association type. You can find these in HubSpot's API documentation or by inspecting existing associations.

**Success Response (HTTP 200 OK - JSON Example):**

```json
{
    "status": "success",
    "message": "Association created successfully",
    "action": "created"
}
```

**Error Response (HTTP 4xx/5xx - JSON Example):**

```json
{
    "detail": "Error message from HubSpot or internal server error details"
}
```

#### `GET /associations/{object_type}/{object_id}/{to_object_type}`

**Purpose:** Retrieves associations for a given HubSpot object.

**Path Parameters:**
*   `object_type` (string, required): The type of the object (e.g., "contact", "company", "ticket").
*   `object_id` (string, required): The ID of the object.
*   `to_object_type` (string, required): The type of the associated objects to retrieve (e.g., "company", "contact", "ticket").

**Success Response (HTTP 200 OK - JSON Example):**

```json
{
    "results": [
        {
            "id": "456",
            "type": "company"
        }
    ]
}
```
*   `results` (array): A list of associated objects, each with an `id` and `type`.

**Error Response (HTTP 4xx/5xx - JSON Example):**

```json
{
    "detail": "Error message from HubSpot or internal server error details"
}
```