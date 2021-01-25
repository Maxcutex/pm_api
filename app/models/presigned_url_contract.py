from typing import Optional, Dict


class PresignedUrlContract:
    url: str
    headers: Optional[Dict[str, str]] = None
