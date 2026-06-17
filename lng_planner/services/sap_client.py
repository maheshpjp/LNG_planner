import os
import requests
from typing import Dict, Any, Optional, Tuple

class SAPClientError(Exception):
    pass


def _get_sap_auth_config() -> Tuple[Dict[str, str], Optional[requests.auth.AuthBase]]:
    headers: Dict[str, str] = {
        'Content-Type': 'application/json',
    }
    auth = None

    auth_type = os.environ.get('SAP_AUTH_TYPE', 'header').strip().lower()

    if auth_type == 'basic':
        username = os.environ.get('SAP_USERNAME')
        password = os.environ.get('SAP_PASSWORD')
        if not username or not password:
            raise SAPClientError('Missing SAP_USERNAME or SAP_PASSWORD for basic auth')
        auth = requests.auth.HTTPBasicAuth(username, password)
    else:
        sap_api_key = os.environ.get('SAP_API_KEY')
        if not sap_api_key:
            raise SAPClientError('Missing SAP_API_KEY environment variable')

        header_name = os.environ.get('SAP_API_KEY_HEADER_NAME', 'Authorization' if auth_type == 'bearer' else 'X-Gravitee-Api-Key')
        if auth_type == 'bearer':
            headers[header_name] = f'Bearer {sap_api_key}'
        else:
            headers[header_name] = sap_api_key

    return headers, auth


def fetch_sap_data(sap_api_url: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    headers, auth = _get_sap_auth_config()
    try:
        response = requests.get(sap_api_url, headers=headers, params=params or {}, auth=auth, timeout=60)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        raise SAPClientError(f'SAP request failed: {exc}') from exc


def summarize_sap_payload(sap_payload: Dict[str, Any]) -> str:
    summary_lines = []
    for key, value in sap_payload.items():
        if isinstance(value, list):
            summary_lines.append(f'{key}: {len(value)} items')
        else:
            summary_lines.append(f'{key}: {type(value).__name__}')
    return '\n'.join(summary_lines)
