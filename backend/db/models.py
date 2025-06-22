from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    max_bookings_per_slot = Column(Integer)
    created_by = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default='now()')
    slots = relationship("Slot", back_populates="event")
    bookings = relationship("Booking", back_populates="event")

class Slot(Base):
    __tablename__ = "slots"

    id = Column(Integer, primary_key=True, index=True)
    time = Column(DateTime, nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"))
    event = relationship("Event", back_populates="slots")
    bookings = relationship("Booking", back_populates="slot")

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"))
    slot_id = Column(Integer, ForeignKey("slots.id"))
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    
    event = relationship("Event", back_populates="bookings")
    slot = relationship("Slot", back_populates="bookings")