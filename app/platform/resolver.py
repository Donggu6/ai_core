from app.platform.types import PlatformType

def normalize_platform(value: str | None) -> str:
    raw = (value or PlatformType.SOURCING.value).strip().lower()
    allowed = {p.value for p in PlatformType}
    return raw if raw in allowed else PlatformType.SOURCING.value
