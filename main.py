import logging
from fastapi import FastAPI
from routers.crud_router import create_crud_router
from routers import webhooks, associations
from models.contact_models import ContactProperties, HubSpotContactOutput
from models.company_models import CompanyProperties, HubSpotCompanyOutput
from models.ticket_models import TicketProperties, HubSpotTicketOutput
from fastapi_limiter import FastAPILimiter
from redis.asyncio import Redis
from config import settings

app = FastAPI(
    title="HubSpot Connector API",
    description="API to simplify interactions with HubSpot CRM",
    version="0.1.0",
)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@app.on_startup
async def startup():
    redis = Redis(host="localhost", port=6379, db=0, encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(redis)

# Include generic CRUD routers for HubSpot objects
app.include_router(create_crud_router(
    object_type="contacts",
    create_schema=ContactProperties,
    response_schema=HubSpotContactOutput,
    search_property="email"
))

app.include_router(create_crud_router(
    object_type="companies",
    create_schema=CompanyProperties,
    response_schema=HubSpotCompanyOutput,
    search_property="domain"
))

app.include_router(create_crud_router(
    object_type="tickets",
    create_schema=TicketProperties,
    response_schema=HubSpotTicketOutput,
    # Tickets don't have a unique search property like email/domain for update-or-create
    # so we omit search_property. This means POST /tickets will always create a new ticket.
))

# Include specific routers
app.include_router(webhooks.router)
app.include_router(associations.router)