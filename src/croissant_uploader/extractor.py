from junitparser import JUnitXml
import logging
from .results import TestResults

logger = logging.getLogger(__name__)

def extract_tests(*paths: list[str]):
    if not paths:
        raise RuntimeError(f"Please provide at least one path to a JUnit XML file")
    results = TestResults()
    xmls = [JUnitXml.fromfile(path) for path in paths]
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
    return results