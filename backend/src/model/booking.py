class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"))
    slot_id = Column(Integer, ForeignKey("slots.id"))
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    
    __table_args__ = (UniqueConstraint('email', 'slot_id', name='unique_email_slot'),)

    event = relationship("Event", back_populates="bookings")
    slot = relationship("Slot", back_populates="bookings")