from dataclasses import dataclass, field
from typing import Any


@dataclass
class ConfigAPI:
    ftp_host: str
    ftp_password: str
    ftp_user: str
    logger: Any = field(default_factory=object)
    ftp_port: int = 21
