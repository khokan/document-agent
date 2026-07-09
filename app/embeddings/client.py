"""
🌐 Resilient HTTP client wrapper for interacting with the Ollama service.
"""

import httpx
from typing import Dict, List, Any, Optional
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from app.utils.logger import logger
from app.utils.config import config


class OllamaClient:
    """Async client wrapper for the local Ollama service."""

    def __init__(self):
        self.base_url = config.ollama_endpoint
        self.timeout = httpx.Timeout(float(config.embeddings_timeout))
        
        logger.info(f"[EMBEDDINGS] OllamaClient initialized (endpoint={self.base_url}, timeout={config.embeddings_timeout}s)")

    @retry(
        reraise=True,
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((httpx.HTTPError, httpx.TimeoutException)),
        before_sleep=lambda retry_state: logger.warning(
            f"[RETRY] Ollama request failed, retrying in {retry_state.next_action.sleep}s... "
            f"(Attempt {retry_state.attempt_number})"
        )
    )
    async def post(self, path: str, payload: Dict[str, Any]) -> httpx.Response:
        """
        Send a POST request to Ollama with retry logic.

        Args:
            path: API path (e.g., '/api/embeddings')
            payload: JSON request payload

        Returns:
            httpx.Response object
        """
        url = f"{self.base_url.rstrip('/')}{path}"
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            return response

    async def check_health(self) -> bool:
        """Check if Ollama service is reachable."""
        try:
            url = f"{self.base_url.rstrip('/')}/"
            async with httpx.AsyncClient(timeout=httpx.Timeout(3.0)) as client:
                res = await client.get(url)
                return res.status_code == 200
        except Exception:
            return False
