from dataclasses import dataclass

@dataclass
class FtpClientInitArgs:
    host: str
    user: str
    password: str
    client_name: str = "aioftp_client"
    port: int = 21

@dataclass
class ListFilesArgs:
    path: str

@dataclass
class ReadFileArgs:
    file_path: str