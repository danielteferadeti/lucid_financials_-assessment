from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.auth import decode_access_token

security = HTTPBearer()


async def get_current_user(
    token: HTTPAuthorizationCredentials = Security(security)
):
    payload = decode_access_token(token.credentials)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return payload
