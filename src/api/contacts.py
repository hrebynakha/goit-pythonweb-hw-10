"""Contacts api views"""

from typing import List

from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.schemas.contacts import ContactModel, ContactResponse
from src.services.contacts import ContactService
from src.exceptions.contacts import ContactNotFound
from src.schemas.contacts import ContactNotFoundResponse
from src.helpers.helpers import filter_normalize


router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.get("/", response_model=List[ContactResponse])
async def read_contacts(
    skip: int = 0,
    limit: int = 100,
    filter: str = Query(default=""),  # pylint: disable=redefined-builtin
    db: AsyncSession = Depends(get_db),
):
    """Return contacts list"""
    contact_service = ContactService(db)
    contacts = await contact_service.get_contacts(filter_normalize(filter), skip, limit)
    return contacts


@router.get("/get-upcoming-birthday", response_model=List[ContactResponse])
async def get_upcoming_birthday(
    skip: int = 0,
    limit: int = 100,
    time_range: int = 7,
    db: AsyncSession = Depends(get_db),
):
    """Return contacts list"""
    contact_service = ContactService(db)
    contacts = await contact_service.get_upcoming_birthday_contacts(
        skip, limit, time_range
    )
    return contacts


@router.get(
    "/{contact_id}",
    response_model=ContactResponse,
    responses={
        404: {"model": ContactNotFoundResponse, "description": "Not found response"},
    },
)
async def read_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    """Get contact by ID"""
    contact_service = ContactService(db)
    contact = await contact_service.get_contact(contact_id)
    if contact is None:
        raise ContactNotFound
    return contact


@router.post(
    "/",
    response_model=ContactResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_contact(body: ContactModel, db: AsyncSession = Depends(get_db)):
    """Create new contact"""
    contact_service = ContactService(db)
    return await contact_service.create_contact(body)


@router.put(
    "/{contact_id}",
    response_model=ContactResponse,
    responses={
        404: {"model": ContactNotFoundResponse, "description": "Not found response"},
    },
)
async def update_contact(
    body: ContactModel, contact_id: int, db: AsyncSession = Depends(get_db)
):
    """Udpate contact by ID"""
    contact_service = ContactService(db)
    contact = await contact_service.update_contact(contact_id, body)
    if contact is None:
        raise ContactNotFound
    return contact


@router.delete(
    "/{contact_id}",
    response_model=ContactResponse,
    responses={
        404: {"model": ContactNotFoundResponse, "description": "Not found response"},
    },
)
async def remove_contact(contact_id: int, db: AsyncSession = Depends(get_db)):
    """Delete contact by ID"""
    contact_service = ContactService(db)
    contact = await contact_service.remove_contact(contact_id)
    if contact is None:
        raise ContactNotFound
    return contact
