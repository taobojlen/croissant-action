from .extractor import extract_tests
from .uploader import upload_results
import argparse
import logging

logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Upload test results to Croissant")
    parser.add_argument("--hostname", required=True, help="The hostname of the Croissant server, e.g. croissant.example.workers.dev")
    parser.add_argument("--branch", required=True, help="The branch name that the tests ran on")
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="The log level to use",
    )
    parser.add_argument("files", nargs="*", help="The path to the test results")

    args = parser.parse_args()
    logging.basicConfig(level=getattr(logging, args.log_level.upper()), format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    logger.debug(f"Hostname: {args.hostname}")
    logger.debug(f"Branch: {args.branch}")
    logger.debug(f"Files: {args.files}")

    results = extract_tests(*args.files)
    upload_results(results, args.hostname, args.branch)

if __name__ == "__main__":
    main()