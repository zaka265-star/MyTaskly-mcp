"""Base HTTP client with authentication and common request methods."""

import httpx
import jwt
from typing import Dict, Any, Optional
from datetime import datetime, timedelta, timezone
from src.config import settings


class BaseClient:
    """Base HTTP client for communicating with MyTaskly FastAPI server."""

    def __init__(self):
        self.base_url = settings.fastapi_base_url
        self.api_key = settings.fastapi_api_key
        # This secret must match the SECRET_KEY in FastAPI server for user token generation
        self.secret_key = "349878uoti34h80943iotrhf-83490ewofridsh3t4iner"
        self.timeout = 30.0

    async def _get_user_token(self, user_id: int) -> str:
        """
        Generate a JWT token for the user to authenticate with FastAPI.

        This token is separate from the MCP authentication token.
        It's used by the MCP server to act on behalf of the user when
        calling FastAPI backend endpoints.

        Args:
            user_id: User ID to generate token for

        Returns:
            JWT token string
        """
        now = datetime.now(timezone.utc)
        payload = {
            "sub": str(user_id),
            "type": "access",
            "exp": int((now + timedelta(minutes=30)).timestamp()),
        }
        token = jwt.encode(payload, self.secret_key, algorithm="HS256")
        return token

    def _get_headers(self, token: Optional[str] = None) -> Dict[str, str]:
        """
        Build request headers with API key and optional Bearer token.

        Args:
            token: Optional JWT token for user authentication

        Returns:
            Headers dictionary
        """
        headers = {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json"
        }
        if token:
            headers["Authorization"] = f"Bearer {token}"
        return headers

    async def _get(
        self,
        path: str,
        token: str,
        params: Optional[Dict[str, Any]] = None
    ) -> Any:
        """
        Generic GET request.

        Args:
            path: API endpoint path (e.g., "/tasks/")
            token: JWT token for authentication
            params: Optional query parameters

        Returns:
            Response JSON data

        Raises:
            httpx.HTTPStatusError: If request fails
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(
                f"{self.base_url}{path}",
                headers=self._get_headers(token),
                params=params
            )
            response.raise_for_status()
            return response.json()

    async def _post(
        self,
        path: str,
        token: str,
        json: Dict[str, Any]
    ) -> Any:
        """
        Generic POST request.

        Args:
            path: API endpoint path
            token: JWT token for authentication
            json: Request body data

        Returns:
            Response JSON data

        Raises:
            httpx.HTTPStatusError: If request fails
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.base_url}{path}",
                headers=self._get_headers(token),
                json=json
            )
            response.raise_for_status()
            return response.json()

    async def _put(
        self,
        path: str,
        token: str,
        json: Dict[str, Any]
    ) -> Any:
        """
        Generic PUT request.

        Args:
            path: API endpoint path
            token: JWT token for authentication
            json: Request body data

        Returns:
            Response JSON data

        Raises:
            httpx.HTTPStatusError: If request fails
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.put(
                f"{self.base_url}{path}",
                headers=self._get_headers(token),
                json=json
            )
            response.raise_for_status()
            return response.json()

    async def _delete(
        self,
        path: str,
        token: str
    ) -> Any:
        """
        Generic DELETE request.

        Args:
            path: API endpoint path
            token: JWT token for authentication

        Returns:
            Response JSON data

        Raises:
            httpx.HTTPStatusError: If request fails
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.delete(
                f"{self.base_url}{path}",
                headers=self._get_headers(token)
            )
            response.raise_for_status()
            return response.json()

    async def _get_no_auth(self, path: str) -> Any:
        """
        Generic GET request without authentication (for health checks).

        Args:
            path: API endpoint path

        Returns:
            Response JSON data
        """
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{self.base_url}{path}")
            return {"status": "healthy", "code": response.status_code}
