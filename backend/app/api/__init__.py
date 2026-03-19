from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from ..services.auth_utils import verify_password, create_access_token, get_password_hash
from .settings import router as settings_router

# Initialize the core API for the Stock Market Predictor
api_app = FastAPI(title="Stock Market Predictor API")

# Register the Integration Settings module baseline
api_app.include_router(settings_router, prefix="/settings", tags=["Configuration"])

# Setup for token handling (Phase 2)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

fake_users_db = {
    "admin": {
        "username": "admin",
        "full_name": "Market Strategist",
        "email": "admin@trading.local",
        "hashed_password": get_password_hash("password123"),
        "disabled": False,
    }
}

@api_app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect credentials"
        )
    
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

@api_app.get("/users/me")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    return {"username": "admin", "role": "Strategist", "status": "Authenticated"}
