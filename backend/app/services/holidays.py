import httpx

HOLIDAYS_URL = "https://date.nager.at/api/v3/PublicHolidays/2026/BR"

async def get_holidays() -> set[str]:
    async with httpx.AsyncClient() as client:
        response = await client.get(HOLIDAYS_URL)
        response.raise_for_status()

    holidays = response.json()

    return {holiday["date"] for holiday in holidays}