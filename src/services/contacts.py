"""Contacts serivices"""

from sqlalchemy.ext.asyncio import AsyncSession

from src.repository.contacts import ContactRepository
from src.schemas.contacts import ContactModel
from src.exceptions.contacts import EmailValueError


class ContactService:
    """Contact service"""

    def __init__(self, db: AsyncSession):
        self.repository = ContactRepository(db)

    async def create_contact(self, body: ContactModel):
        """Create contact service"""
        existing_contact = await self.repository.get_contact_by_email(body.email)
        if existing_contact:
            raise EmailValueError(f"Contact with this email {body.email} alredy exists")
        return await self.repository.create_contact(body)

    async def get_contacts(self, filter_: str, skip: int, limit: int):
        """Get contacts service"""
        return await self.repository.get_contacts(filter_, skip, limit)

    async def get_contact(self, contact_id: int):
        """get contact by id"""
        return await self.repository.get_contact_by_id(contact_id)

    async def update_contact(self, contact_id: int, body: ContactModel):
        """Update contact by id"""
        existing_contact = await self.repository.get_contact_by_email(
            body.email, contact_id
        )
        if existing_contact:
            raise EmailValueError(f"Contact with this email {body.email} alredy exists")
        return await self.repository.update_contact(contact_id, body)

    async def remove_contact(self, contact_id: int):
        """Remove contact by ID"""
        return await self.repository.remove_contact(contact_id)

    async def get_upcoming_birthday_contacts(self, skip, limit, time_range):
        """Get contacts service"""
        return await self.repository.get_upcoming_birthday_contacts(
            skip, limit, time_range
        )
