import logging
from fastapi import HTTPException
from jwt import decode as jwt_decode, ExpiredSignatureError, InvalidTokenError

_logger = logging.getLogger(__name__)


def verify_token(token: str, secret_key: str, algorithms: list):
    """Verify that the header Authorization was sent from APP.

    Raise and return 403 if not authorized.
    """
    if not token:
        raise HTTPException(status_code=401, detail="Token is missing!")

    try:
        # Decode the token without verification for the demo purpose, replace 'secret_key' with your actual secret
        verified_token_data = jwt_decode(
            token, secret_key, algorithms=algorithms)
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except InvalidTokenError as e:
        raise HTTPException(status_code=401, detail=str(e))

    cd_auth = verified_token_data.get("role")
    if not cd_auth:
        raise HTTPException(status_code=403, detail="Role not found in token")

    _logger.debug(f"<cd_auth: {cd_auth}>")

    return cd_auth
