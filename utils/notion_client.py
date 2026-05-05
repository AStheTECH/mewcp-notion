"""Shared utilities for Notion API requests"""

import logging
from typing import Dict, Optional

import requests
from fastmcp_credentials import get_credentials

NOTION_API_BASE = "https://api.notion.com"
NOTION_VERSION = "2025-09-03"

logger = logging.getLogger("notion-mcp-server")


def get_headers() -> Dict[str, str]:
    """Headers for Notion API requests with resolved credentials"""
    cred = get_credentials()
    if not cred.access_token:
        raise ValueError("Credential must have access_token")
    return {
        "Authorization": f"Bearer {cred.access_token}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }


def make_notion_request(
    method: str,
    endpoint: str,
    body: Optional[Dict] = None,
    params: Optional[Dict] = None,
) -> Dict:
    """request handler for Notion API"""
    headers = get_headers()
    url = f"{NOTION_API_BASE}{endpoint}"

    try:
        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            json=body,
            params=params,
        )
        result = response.json()

        if not (200 <= response.status_code < 300):
            logger.error(f"Notion API error: {result}")
            return {
                "error": result.get("message", "Unknown error"),
                "code": result.get("code"),
                "status": response.status_code,
            }
        return result

    except Exception as e:
        logger.error(f"Request error: {e}")
        return {"error": str(e)}
