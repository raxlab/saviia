from dataclasses import dataclass, field
from enum import Enum
from typing import Literal


class LogStatus(Enum):
    STARTED = "started"
    SUCCESSFUL = "successful"
    FAILED = "failed"
    ERROR = "error"
    EARLY_RETURN = "early_return"
    ALERT = "alert"


@dataclass
class LogClientArgs:
    client_name: str = field(default="logging")
    service_name: str = field(default="")
    class_name: str = field(default="")
    method_name: str = field(default="")
    active_record: bool = False


@dataclass
class InfoArgs:
    status: Literal[LogStatus.STARTED, LogStatus.SUCCESSFUL, LogStatus.EARLY_RETURN]
    metadata: dict = field(default_factory=dict)


@dataclass
class DebugArgs:
    status: Literal[
        LogStatus.STARTED, LogStatus.SUCCESSFUL, LogStatus.EARLY_RETURN, LogStatus.ALERT
    ]
    metadata: dict = field(default_factory=dict)


@dataclass
class ErrorArgs:
    status: Literal[LogStatus.ERROR]
    metadata: dict = field(default_factory=dict)


@dataclass
class WarningArgs:
    status: Literal[LogStatus.FAILED, LogStatus.ALERT]
    metadata: dict = field(default_factory=dict)
