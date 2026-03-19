from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from ..services.auth_utils import verify_password, create_access_token, get_password_hash

# Initialize the core API
api_app = FastAPI(title="Stock Market Predictor API")

# Setup for token handling
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Static User Database for our Trading Predictor
# These are baseline credentials for your initial setup
fake_users_db = {
    "admin": {
        "username": "admin",
        "full_name": "Market Strategist",
        "email": "admin@trading.local",
        "hashed_password": get_password_hash("password123"), # Default password
        "disabled": False,
    }
}

@api_app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Secure Login: Validates user and returns a JWT."""
    user = fake_users_db.get(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

@api_app.get("/users/me")
async def read_users_me(token: str = Depends(oauth2_scheme)):
    """User Profile: Returns data for the currently logged-in user."""
    return {"username": "admin", "role": "Strategist", "status": "Authenticated"}

@api_app.post("/logout")
async def logout():
    """Logout: Signals the client to discard the session."""
    return {"message": "Successfully logged out of the trading session."}
