import httpx

async def validate_breed(breed_name: str) -> bool:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("https://api.thecatapi.com/v1/breeds")
            response.raise_for_status()
            breeds = response.json()
            return any(breed["name"].lower() == breed_name.lower() for breed in breeds)
    except Exception:
        return False
