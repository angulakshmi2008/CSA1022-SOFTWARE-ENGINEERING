import uuid
from fastapi import APIRouter, HTTPException, status, Depends
from backend.app.schemas.auth import LoginRequest, TokenResponse, UserCreate
from backend.app.core.security import verify_password, hash_password, create_access_token, get_current_user
from backend.app.database import get_db

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (request.username,))
        user = cursor.fetchone()
        if not user or not verify_password(request.password, user["password_hash"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password"
            )
        if not user["is_active"]:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User account is disabled")
            
        token = create_access_token({"sub": user["user_id"], "role": user["role"], "region": user["region_id"]})
        return TokenResponse(
            access_token=token,
            user_id=user["user_id"],
            username=user["username"],
            role=user["role"],
            region_id=user["region_id"]
        )

@router.post("/register", response_model=TokenResponse)
def register(user_in: UserCreate):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM users WHERE username = ? OR email = ?", (user_in.username, user_in.email))
        if cursor.fetchone():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username or email already registered")
            
        user_id = str(uuid.uuid4())
        pwd_hash = hash_password(user_in.password)
        cursor.execute("""
            INSERT INTO users (user_id, username, email, password_hash, role, region_id, is_active, created_at)
            VALUES (?, ?, ?, ?, ?, ?, 1, datetime('now', 'utc'))
        """, (user_id, user_in.username, user_in.email, pwd_hash, user_in.role, user_in.region_id))
        
        token = create_access_token({"sub": user_id, "role": user_in.role, "region": user_in.region_id})
        return TokenResponse(
            access_token=token,
            user_id=user_id,
            username=user_in.username,
            role=user_in.role,
            region_id=user_in.region_id
        )

@router.get("/me")
def read_current_user_profile(current_user: dict = Depends(get_current_user)):
    return current_user
