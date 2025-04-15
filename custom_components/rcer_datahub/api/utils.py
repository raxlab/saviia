from typing import Any

from custom_components.rcer_datahub.helpers.datetime_utils import datetime_to_str, today


def http_response(
    message: Any, status: int, metadata: dict[str, Any] | None = None
) -> dict[str, int | Any]:
    if metadata is None:
        metadata = {}
    return {
        "status": status,
        "message": message,
        **metadata,
    }


def generate_file_content(
    file_contents: dict[str, Any],
) -> dict[str, dict[str, int | str]]:
    return {
        filename: {
            "size": len(data),
            "date": datetime_to_str(today()),
        }
        for filename, data in file_contents.items()
    }
