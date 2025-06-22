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