# hubspot-connector

## Overview

The `hubspot-connector` is a middleware API designed to streamline and simplify interactions with the HubSpot CRM for various third-party applications. It acts as a central gateway, abstracting the complexities of direct HubSpot API calls, authentication, and data mapping.

## Disclaimer

This project is a personal initiative and is **not affiliated with, endorsed by, or officially connected to HubSpot, Inc.** in any way. It is provided "as is" without any warranty, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, and non-infringement. Use this software at your own risk. The author is not responsible for any direct, indirect, incidental, special, exemplary, or consequential damages arising from the use of this software.

## Why use hubspot-connector?

*   **Simplified Integration:** Instead of each external application needing to understand and implement HubSpot's specific API calls, they can interact with a single, consistent API provided by `hubspot-connector`.
*   **Centralized Logic:** Handles HubSpot authentication (using Private App Access Tokens), rate limiting, and error handling in one place.
*   **Data Transformation:** Provides a layer for transforming data between the generic format used by external applications and the specific format required by HubSpot, and vice-versa.
*   **Extensibility:** Designed to be easily extended to support additional HubSpot objects (e.g., Companies, Deals, Tickets) and functionalities beyond the initial contact management.

## How it Works

External applications send requests to the `hubspot-connector`'s API endpoints. The `hubspot-connector` then translates these requests into the appropriate HubSpot API calls, executes them, processes the responses, and returns a simplified, consistent response back to the originating application.

## Key Features

*   **Contact Management:** Create and update HubSpot contacts, identifying existing contacts by email.
*   **Company Management:** Create and update HubSpot companies, identifying existing companies by domain.
*   **Ticket Management:** Create new HubSpot tickets.
*   **Custom Property Handling:** Seamlessly pass through any custom HubSpot properties defined in your portal for contacts, companies, and tickets.
*   **Modular Architecture:** Built with FastAPI routers and separated Pydantic models for easy extension and maintenance.

## Roadmap & Future Enhancements

This project is continuously evolving. We have a roadmap of exciting features and improvements planned to further enhance the `hubspot-connector`'s capabilities. For a detailed look at potential future developments, please refer to the [`FUTURE_DEVELOPMENT.md`](./FUTURE_DEVELOPMENT.md) file.

## Getting Started

For detailed instructions on how to set up, configure, and run the `hubspot-connector` locally, as well as comprehensive API documentation, please refer to the [`INITIALISATION.md`](./INITIALISATION.md) file.

## Project Structure

```
hubspot-connector/
├── main.py
├── config.py
├── hubspot_client.py
├── models/             # Contains Pydantic models for data structures
├── .env.example
├── requirements.txt
├── README.md
├── INITIALISATION.md
├── routers/            # Contains API endpoint definitions
├── tutorials/          # Detailed guides and how-tos
└── tests/              # Unit and integration tests
```