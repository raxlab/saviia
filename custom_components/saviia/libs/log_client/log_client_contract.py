# External libraries
from abc import ABC, abstractmethod

# Internal modules
from custom_components.saviia.libs.log_client.types.log_client_types import (
    DebugArgs,
    ErrorArgs,
    InfoArgs,
    WarningArgs,
)


class LogClientContract(ABC):
    @abstractmethod
    def info(self, args: InfoArgs) -> None:
        pass

    @abstractmethod
    def error(self, args: ErrorArgs) -> None:
        pass

    @abstractmethod
    def debug(self, args: DebugArgs) -> None:
        pass

    @abstractmethod
    def warning(self, args: WarningArgs) -> None:
        pass
