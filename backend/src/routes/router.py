from fastapi import APIRouter
from .events.event import router as events_router
from .booking.bookings import router as bookings_router
from .slot.slot import router as slots_router
from .users.user import router as users_router
from .admin.admin import router as admin_router

router = APIRouter()

# Include all route files
router.include_router(events_router, tags=["events"])
router.include_router(bookings_router, tags=["bookings"])
router.include_router(slots_router, tags=["slots"])
router.include_router(users_router, prefix="/users", tags=["users"])
router.include_router(admin_router, tags=["admin"])
