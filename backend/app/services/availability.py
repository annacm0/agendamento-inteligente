from datetime import date

from app.services.holidays import get_holidays

async def is_date_available(selected_date: date) -> bool:
    if selected_date.weekday() >= 5:
        return False

    holidays = await get_holidays()

    return selected_date.isoformat() not in holidays