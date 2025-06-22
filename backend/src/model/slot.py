class Slot(Base):
    __tablename__ = "slots"

    id = Column(Integer, primary_key=True, index=True)
    time = Column(DateTime, nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"))
    event = relationship("Event", back_populates="slots")
    bookings = relationship("Booking", back_populates="slot")