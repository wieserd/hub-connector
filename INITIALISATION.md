# INITIALISATION: hubspot-connector

This document provides detailed instructions on how to set up, configure, run, and interact with the `hubspot-connector` API. For a high-level overview of the project, its purpose, and features, please refer to the [`README.md`](./README.md) file.

## Setup and Run Instructions

For detailed instructions on setting up your development environment and running the application, please refer to the [`setup_and_run.md`](./tutorials/setup_and_run.md) tutorial.

## API Endpoints

For comprehensive documentation of all available API endpoints, including request/response examples and parameter details, please refer to the [`api_endpoints.md`](./tutorials/api_endpoints.md) tutorial.

## Handling Custom HubSpot Properties

To understand how to work with custom HubSpot properties when using the `hubspot-connector`, please refer to the [`custom_properties.md`](./tutorials/custom_properties.md) tutorial.

## Running Tests

For instructions on how to run the project's tests, please refer to the [`running_tests.md`](./tutorials/running_tests.md) tutorial.

## Project Structure

```
hubspot-connector/
├── main.py             # FastAPI application entry point
├── config.py           # Configuration settings (e.g., HubSpot API key)
├── hubspot_client.py   # Module for HubSpot API interactions
├── models/             # Pydantic models for data validation and serialization
│   ├── __init__.py
│   ├── api_response_model.py
│   ├── company_models.py
│   ├── contact_models.py
│   └── ticket_models.py
├── .env.example        # Example environment variables file
├── requirements.txt    # Python dependencies
├── README.md           # General information about the project
├── INITIALISATION.md   # This file
├── routers/
│   ├── __init__.py     # Makes 'routers' a Python package
│   ├── crud_router.py  # Generic CRUD router for HubSpot objects
│   ├── webhooks.py     # API endpoint for HubSpot Webhooks
│   └── associations.py # API endpoints for HubSpot Associations
├── tutorials/          # Detailed guides and how-tos
│   ├── setup_and_run.md
│   ├── api_endpoints.md
│   ├── custom_properties.md
│   └── running_tests.md
└── tests/              # Unit and integration tests
    ├── conftest.py
    ├── test_main.py
    └── test_hubspot_client.py
```
