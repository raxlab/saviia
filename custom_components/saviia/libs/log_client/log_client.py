# Internal modules
from custom_components.saviia.libs.log_client.log_client_contract import (
    LogClientContract,
)
from custom_components.saviia.libs.log_client.logging_client.logging_client import (
    LoggingClient,
)
from custom_components.saviia.libs.log_client.types.log_client_types import (
    DebugArgs,
    ErrorArgs,
    InfoArgs,
    LogClientArgs,
    WarningArgs,
)


class LogClient(LogClientContract):
    def __init__(self, args: LogClientArgs):
        clients = {
            "logging": LoggingClient(args),
        }
        if clients.get(args.client_name):
            self.client_name = args.client_name
            self.client_obj = clients[args.client_name]
        else:
            msg = f"Unsupported client '{args.client_name}'."
            raise KeyError(msg)

    @property
    def method_name(self) -> str:
        return self.client_obj.method_name

    @method_name.setter
    def method_name(self, method_name: str) -> None:
        self.client_obj.method_name = method_name

    @property
    def log_history(self) -> list:
        return self.client_obj.log_history

    def info(self, args: InfoArgs) -> None:
        return self.client_obj.info(args)

    def error(self, args: ErrorArgs) -> None:
        return self.client_obj.error(args)

    def debug(self, args: DebugArgs) -> None:
        return self.client_obj.debug(args)

    def warning(self, args: WarningArgs) -> None:
        return self.client_obj.warning(args)
