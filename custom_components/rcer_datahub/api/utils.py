from typing import Any, Dict, Union
from ..libs.zero_dependency.helpers.datetime_utils import datetime_to_str, today


def http_response(
    message: Any, status: int, metadata: Dict[str, Any] = {}
) -> Dict[str, Union[int, Any]]:
    return {
        "status": status,
        "message": message,
        **metadata,
    }


def generate_file_content(
    file_contents: Dict[str, Any],
) -> Dict[str, Dict[str, Union[int, str]]]:
    return {
        filename: {
            "size": len(data),
            "date": datetime_to_str(today()),
        }
        for filename, data in file_contents.items()
    }
