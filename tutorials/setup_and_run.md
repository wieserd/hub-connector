## Setup and Run Instructions

1.  **Clone the repository.**

2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment:**
    *   **Linux/macOS:**
        ```bash
        source venv/bin/activate
        ```
    *   **Windows:**
        ```bash
        .\venv\Scripts\activate
        ```

4.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Configure Environment Variables:**
    Create a `.env` file in the root directory of the project based on `.env.example` and add your HubSpot Private App Access Token.

    Your `.env` file should look like this:
    ```
    HUBSPOT_PRIVATE_APP_TOKEN=YOUR_HUBSPOT_PRIVATE_APP_TOKEN
    HUBSPOT_WEBHOOK_SECRET=YOUR_HUBSPOT_WEBHOOK_SECRET
    RATE_LIMIT=100/minute
    ```
    Replace `YOUR_HUBSPOT_PRIVATE_APP_TOKEN` with your actual HubSpot Private App Access Token.
    Replace `YOUR_HUBSPOT_WEBHOOK_SECRET` with your HubSpot Webhook Secret.
    Adjust `RATE_LIMIT` as needed (e.g., "100/minute", "10/second").

6.  **Run the application:**
    ```bash
    uvicorn main:app --reload
    ```
    The API will be accessible at `http://127.0.0.1:8000` (or similar, as indicated by uvicorn).
    You can access the interactive API documentation (Swagger UI) at `http://127.0.0.1:8000/docs`.

**Note:** The rate limiting feature uses Redis. Ensure you have a Redis server running and accessible (defaulting to `localhost:6379`).