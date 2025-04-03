"""Contacts repo"""

from typing import List
from datetime import datetime, timedelta, timezone

from fastapi_sa_orm_filter.main import FilterCore

from sqlalchemy import select, func, or_, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.contacts import Contact
from src.schemas.contacts import ContactModel
from src.filters.contacts import contact_filter


class ContactRepository:
    """Contact repo class"""

    def __init__(self, session: AsyncSession):
        self.db = session

    async def get_contacts(
        self,
        filter_: str,
        skip: int,
        limit: int,
    ) -> List[Contact]:
        """Get contcats in database and return by limit"""
        filter_inst = FilterCore(Contact, contact_filter)
        query = (
            filter_inst.get_query(filter_)
            .offset(skip)
            .limit(limit)
            .order_by(Contact.id)
        )
        contacts = await self.db.execute(query)
        return contacts.scalars().all()

    async def get_contact_by_id(self, contact_id: int) -> Contact | None:
        """Get contact in databse by ID"""
        query = select(Contact).filter_by(id=contact_id)
        contact = await self.db.execute(query)
        return contact.scalar_one_or_none()

    async def get_contact_by_email(
        self, contact_email: str, contact_id: int = None
    ) -> Contact | None:
        """Get contact in databse by email"""
        if contact_id:
            query = select(Contact).filter(
                Contact.email == contact_email, Contact.id != contact_id
            )
        else:
            query = select(Contact).filter_by(email=contact_email)
        contact = await self.db.execute(query)
        return contact.scalar_one_or_none()

    async def create_contact(self, body: ContactModel) -> Contact:
        """Create contact function"""
        contact = Contact(**body.model_dump(exclude_unset=True))
        self.db.add(contact)
        await self.db.commit()
        await self.db.refresh(contact)
        return contact

    async def update_contact(
        self, contact_id: int, body: ContactModel
    ) -> Contact | None:
        """Update contact in database"""
        contact = await self.get_contact_by_id(contact_id)
        for field, value in body.model_dump(exclude_unset=True).items():
            current_value = getattr(contact, field)
            if current_value != value:
                setattr(contact, field, value)
        await self.db.commit()
        await self.db.refresh(contact)
        return contact

    async def remove_contact(self, contact_id: int) -> Contact | None:
        """Remove contact in DB"""
        contact = await self.get_contact_by_id(contact_id)
        if contact:
            await self.db.delete(contact)
            await self.db.commit()
        return contact

    async def get_upcoming_birthday_contacts(
        self,
        skip: int,
        limit: int,
        time_range: int = 7,
    ) -> List[Contact]:
        """
        Search contacts in database where birthday for user is in set range.Default - 7 day
        Debug to change current time manually:
        current_time = datetime.strptime("Dec 24 2005  1:33PM", "%b %d %Y %I:%M%p")
        """
        current_time = datetime.now(tz=timezone.utc)
        delta = current_time + timedelta(days=time_range)
        start, end = current_time.strftime("%m-%d"), delta.strftime("%m-%d")
        fn_ = or_ if current_time.month > delta.month else and_
        query = (
            select(Contact)
            .filter(
                fn_(
                    func.to_char(Contact.birthday, "MM-DD") >= start,
                    func.to_char(Contact.birthday, "MM-DD") <= end,
                )
            )
            .offset(skip)
            .limit(limit)
        )
        contacts = await self.db.execute(query)
        return contacts.scalars().all()
