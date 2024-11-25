from croissant_uploader.extractor import extract_tests


def test_gets_list_of_tests():
    results = extract_tests("tests/test_data/singletest.xml")
    assert results.passed == {"tests.test_extractor.test_foo"}
    assert results.failed == set()


def test_handles_failed_tests():
    results = extract_tests("tests/test_data/failedtest.xml")
    assert results.passed == set()
    assert results.failed == {"tests.test_extractor.test_foo"}


def test_handles_skipped_tests():
    results = extract_tests("tests/test_data/skippedtest.xml")
    assert results.passed == set()
    assert results.failed == set()


def test_handles_test_in_multiple_pytest_files():
    results = extract_tests("tests/test_data/multiplepytestfiles.xml")
    assert results.passed == {
        "tests.test_foo.test_foo",
        "tests.test_bar.test_bar",
    }
    assert results.failed == set()


def test_handles_multiple_suites():
    results = extract_tests("tests/test_data/multiplesuites.xml")
    assert results.passed == {
        "tests.test_foo.test_foo",
        "tests.test_bar.test_bar",
    }
    assert results.failed == set()


def handles_duplicate_tests_last_one_wins():
    results = extract_tests(
        "tests/test_data/fooskipped.xml",
        "tests/test_data/foosuccess.xml",
        "tests/test_data/foofailure.xml",
    )
    assert results.passed == set()
    assert results.failed == {"tests.test_extractor.test_foo"}

    results = extract_tests(
        "tests/test_data/foofailure.xml",
        "tests/test_data/fooskipped.xml",
        "tests/test_data/foosuccess.xml",
    )
    assert results.passed == {"tests.test_extractor.test_foo"}
    assert results.failed == set()

    results = extract_tests(
        "tests/test_data/foofailure.xml",
        "tests/test_data/foosuccess.xml",
        "tests/test_data/fooskipped.xml",
    )
    assert results.passed == set()
    assert results.failed == set()


def test_handles_globs():
    results = extract_tests("tests/test_data/folder/*.xml")
    assert results.passed == {"tests.test_foo.test_a"}
    assert results.failed == {"tests.test_bar.test_b"}

    results = extract_tests("tests/test_data/folder/**/*.xml")
    assert results.passed == {"tests.test_foo.test_a", "tests.test_baz.test_c"}
    assert results.failed == {"tests.test_bar.test_b"}
