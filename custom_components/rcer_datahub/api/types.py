from dataclasses import dataclass


@dataclass
class ConfigAPI:
    ftp_host: str
    ftp_password: str
    ftp_user: str
    ftp_port: int = 21
