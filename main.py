from fastapi import FastAPI, HTTPException
import aiohttp
import aiocache

app = FastAPI()

# Configuração do cache
cache = aiocache.Cache(aiocache.SimpleMemoryCache)

# Função para obter dados da API externa
async def fetch_roulette_games():
    url = "https://blaze1.space/api/roulette_games/recent"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                raise HTTPException(status_code=response.status, detail="Failed to fetch data")
            return await response.json()

@app.get("/recent_games")
async def get_recent_games():
    # Verifica se os dados estão no cache
    cached_data = await cache.get("recent_games")
    if cached_data:
        return cached_data
    
    # Se não estiver no cache, busca os dados da API externa
    data = await fetch_roulette_games()
    
    # Armazena os dados no cache por 60 segundos
    await cache.set("recent_games", data, ttl=30)
    
    return data
