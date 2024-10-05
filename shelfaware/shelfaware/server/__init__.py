import os
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# Allow environment variables for dynamic configuration
HOST = os.getenv("SHELFWARE_HOST", "localhost")
PORT = int(os.getenv("SHELFAWARE_PORT", 8000))
FRONTEND_URL = os.getenv("SHELFAWARE_FRONTEND_URL", "http://localhost:3000")

app = FastAPI()

# Allow CORS for React app running on the same server
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Item(BaseModel):
    name: str
    quantity: int


# Endpoint to get all items (dummy data for now)
@app.get("/items")
def read_items():
    return [{"name": "Apple", "quantity": 10}, {"name": "Banana", "quantity": 5}]


# Endpoint to add an item
@app.post("/items")
def create_item(item: Item):
    return {"message": f"Item {item.name} added with quantity {item.quantity}"}


# Run the app with uvicorn
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=HOST, port=PORT)
