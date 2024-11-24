import logging
from urllib.parse import urljoin

import httpx

from .results import TestResults

logger = logging.getLogger(__name__)


def upload_results(results: TestResults, hostname: str, branch: str):
    if not hostname.startswith("https://") and not hostname.startswith(
        "http://"
    ):
        hostname = f"https://{hostname}"
    logger.debug(f"Hostname is now {hostname}")
    url = urljoin(hostname, "/api/v1/results")
    logger.debug(f"Uploading results to {url}")
    data = {
        "branch": branch,
        "passed": list(results.passed),
        "failed": list(results.failed),
    }
    logger.info(f"⬆️ Uploading test results to {hostname}...")
    httpx_logger = logging.getLogger("httpx")
    httpx_logger.setLevel(logging.WARNING)

    try:
        response = httpx.post(url, json=data, timeout=15)
        response.raise_for_status().json()
    except httpx.HTTPError as exc:
        logger.error(f"⚠️ Failed to upload results: {exc}")
        return
    logger.info("🥐 Done!")
