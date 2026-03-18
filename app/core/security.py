import os, hmac, hashlib, time
from typing import Annotated, Optional
from fastapi import Request, Header, HTTPException, status


# 환경변수 미설정 시 None → 명시적으로 ALLOW_NO_AUTH=true 를 설정해야만 인증 생략 가능
_API_KEY = os.getenv("AI_ENGINE_API_KEY")
_HMAC_SECRET = os.getenv("INTERNAL_HMAC_SECRET")
_ALLOW_NO_AUTH = os.getenv("ALLOW_NO_AUTH", "false").lower() == "true"


async def require_internal_auth(
    request: Request,
    x_api_key: Annotated[Optional[str], Header(alias="X-API-KEY")] = None,
    x_ts: Annotated[Optional[str], Header(alias="X-Timestamp")] = None,
    x_sig: Annotated[Optional[str], Header(alias="X-Signature")] = None,
) -> None:
    # 1) API Key 인증
    if _API_KEY:
        if not x_api_key:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="X-API-KEY header missing")
        if x_api_key != _API_KEY:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")
        return

    # 2) HMAC 서명 인증
    if _HMAC_SECRET:
        if not x_ts or not x_sig:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing signature headers")
        try:
            ts_i = int(x_ts)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid timestamp")
        if abs(time.time() - ts_i) > 300:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Signature expired")
        body = await request.body()
        payload = f"{x_ts}.{body.decode()}".encode()
        expected = hmac.new(_HMAC_SECRET.encode(), payload, hashlib.sha256).hexdigest()
        if not hmac.compare_digest(expected, x_sig):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid signature")
        return

    # 3) 아무 인증도 설정되지 않은 경우 — ALLOW_NO_AUTH=true 로 명시해야만 허용
    if not _ALLOW_NO_AUTH:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Server misconfigured: set AI_ENGINE_API_KEY or INTERNAL_HMAC_SECRET, or set ALLOW_NO_AUTH=true for dev",
        )


def require_api_key(x_api_key: Annotated[Optional[str], Header(alias="X-API-KEY")] = None) -> str:
    if not _API_KEY:
        if _ALLOW_NO_AUTH:
            return ""
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Server misconfigured: set AI_ENGINE_API_KEY env var, or set ALLOW_NO_AUTH=true for dev",
        )
    if not x_api_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="X-API-KEY header is missing.")
    if x_api_key != _API_KEY:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key.")
    return x_api_key
