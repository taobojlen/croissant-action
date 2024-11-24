import httpx
import logging
from urllib.parse import urljoin
from .results import TestResults

logger = logging.getLogger(__name__)

def upload_results(results: TestResults, hostname: str, branch: str):
    if not hostname.startswith('https://') and not hostname.startswith('http://'):
        hostname = f'https://{hostname}'
    logger.debug(f"Hostname is now {hostname}")
    url = urljoin(hostname, '/api/v1/results')
    logger.debug(f"Uploading results to {url}")
    data = {
        "branch": branch,
        "passed": list(results.passed),
        "failed": list(results.failed),
    }
    httpx.post(url, json=data, timeout=15)