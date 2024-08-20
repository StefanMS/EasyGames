'''
Main module for backend development of EasyGames
'''

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .api.user.routes import router as user_router
from .api.collection.routes import router as collection_router
from .api.bidding_basket.routes import router as bidding_basket_router
from app.db.initialize import create_superuser
from app.db.session import engine
from app.api.user.models import Base as UserBase
from app.api.bidding_basket.models import Base as BiddingBasketBase
from app.api.collection.models import Base as CollectionBase


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(UserBase.metadata.create_all)
        await conn.run_sync(BiddingBasketBase.metadata.create_all)
        await conn.run_sync(CollectionBase.metadata.create_all)

    await create_superuser()
    yield

app = FastAPI(title="Backend for EasyGames",
              version="0.0.1",
              lifespan=lifespan)

app.include_router(user_router)
app.include_router(collection_router)
app.include_router(bidding_basket_router)

# Add CORS middleware
# origins = [
#     "http://localhost:3000",
#     "http://127.0.0.1:3000",
# ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
