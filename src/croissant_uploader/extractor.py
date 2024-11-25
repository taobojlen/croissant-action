import glob
import logging

from junitparser import JUnitXml

from .results import TestResults

logger = logging.getLogger(__name__)


def extract_tests(*paths: str):
    if not paths:
        raise RuntimeError(
            "Please provide at least one path to a JUnit XML file"
        )
    results = TestResults()
    expanded_paths = []
    for path in paths:
        expanded_paths.extend(glob.glob(path, recursive=True))
    logger.debug(f"Found files: {expanded_paths}")
    xmls = [JUnitXml.fromfile(path) for path in expanded_paths]
    xml = sum(xmls, JUnitXml())
    for suite in xml:
        for test in suite:
            test_name = f"{test.classname}.{test.name}"
            # handle duplicates
            if test_name in results.passed:
                results.passed.remove(test_name)
            if test_name in results.failed:
                results.failed.remove(test_name)

            if test.is_skipped:
                continue

            if test.is_passed:
                results.passed.add(test_name)
            else:
                results.failed.add(test_name)
    logger.info(
        f"🔎 Found {len(results.passed)} passed tests and {len(results.failed)} failed tests"
    )
    return results
