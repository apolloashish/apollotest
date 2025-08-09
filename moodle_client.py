from __future__ import annotations

import json
from typing import Any, Dict, Mapping, Optional

import requests


class MoodleError(Exception):
    """Represents an error returned by Moodle's web service API."""


class MoodleClient:
    """Minimal client for Moodle's REST web services API.

    Typical usage:
        client = MoodleClient(base_url="https://moodle.example.com", token="YOUR_TOKEN")
        site_info = client.get_site_info()
    """

    def __init__(self, base_url: str, token: str, timeout_seconds: float = 15.0) -> None:
        if not base_url:
            raise ValueError("base_url must be provided")
        if not token:
            raise ValueError("token must be provided")
        # Normalize: drop trailing slashes
        self.base_url: str = base_url.rstrip("/")
        self.token: str = token
        self.timeout_seconds: float = timeout_seconds

    def _server_url(self) -> str:
        return f"{self.base_url}/webservice/rest/server.php"

    def call(self, function_name: str, params: Optional[Mapping[str, Any]] = None) -> Any:
        """Call a Moodle web service function and return the parsed JSON result.

        Args:
            function_name: Name of the WS function, e.g. "core_webservice_get_site_info".
            params: Dict of parameters accepted by that function. Supports nested dicts/lists.

        Raises:
            MoodleError: If Moodle returns an error payload.
            requests.HTTPError: For non-2xx HTTP responses.

        Returns:
            Parsed JSON (dict or list) returned by Moodle.
        """
        payload: Dict[str, Any] = {
            "wstoken": self.token,
            "wsfunction": function_name,
            "moodlewsrestformat": "json",
        }
        if params:
            payload.update(_encode_moodle_params(params))

        response = requests.post(self._server_url(), data=payload, timeout=self.timeout_seconds)
        response.raise_for_status()

        # Moodle always returns JSON when moodlewsrestformat=json is set
        data: Any = response.json()

        # Moodle errors are JSON objects with an "exception" key
        if isinstance(data, dict) and data.get("exception"):
            # Provide compact, informative error
            error_code = data.get("errorcode", "unknown_error")
            message = data.get("message", "An error occurred")
            debug_info = data.get("debuginfo")
            composed = f"{error_code}: {message}"
            if debug_info:
                composed += f" | debug: {debug_info}"
            raise MoodleError(composed)

        return data

    def get_site_info(self) -> Dict[str, Any]:
        """Convenience wrapper for core_webservice_get_site_info."""
        result = self.call("core_webservice_get_site_info")
        if not isinstance(result, dict):
            # Defensive: Moodle should return a dict here
            raise MoodleError(
                f"Unexpected response type for get_site_info: {type(result).__name__} -> {json.dumps(result)[:200]}"
            )
        return result

    def get_users_by_field(self, field: str, values: list[str]) -> Any:
        """Call core_user_get_users_by_field.

        Args:
            field: "id", "idnumber", "username", or "email".
            values: List of field values to query.
        """
        return self.call(
            "core_user_get_users_by_field",
            params={"field": field, "values": values},
        )


def _encode_moodle_params(value: Any, prefix: str = "") -> Dict[str, Any]:
    """Recursively flattens nested structures to Moodle's expected bracket notation.

    Example:
        {"users": [{"id": 1, "role": "student"}]}
    becomes:
        {"users[0][id]": 1, "users[0][role]": "student"}
    """
    flat: Dict[str, Any] = {}

    if isinstance(value, Mapping):
        for key, inner in value.items():
            next_prefix = f"{prefix}[{key}]" if prefix else str(key)
            flat.update(_encode_moodle_params(inner, next_prefix))
    elif isinstance(value, (list, tuple)):
        for index, inner in enumerate(value):
            next_prefix = f"{prefix}[{index}]" if prefix else f"[{index}]"
            flat.update(_encode_moodle_params(inner, next_prefix))
    else:
        if not prefix:
            raise ValueError("Cannot encode a scalar value without a parameter name prefix")
        flat[prefix] = value

    return flat