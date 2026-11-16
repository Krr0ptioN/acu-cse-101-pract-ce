"""Unit tests for review_and_merge script."""

import pytest
from scripts import review_and_merge as rm


def test_detect_submission_week_from_head_ref():
    pr = {"headRefName": "submit/week_06_strings_lists_tuples_dicts"}
    assert rm.detect_submission_week(pr) == "week_06_strings_lists_tuples_dicts"


def test_detect_submission_week_from_files():
    pr = {
        "headRefName": "some-random-branch",
        "files": [{"path": "exercises/week_03_functions/challenge.py"}],
    }
    assert rm.detect_submission_week(pr) == "week_03_functions"


def test_detect_submission_week_none():
    pr = {"headRefName": "feature-branch", "files": [{"path": "README.md"}]}
    assert rm.detect_submission_week(pr) is None


def test_check_ci_status():
    assert rm.check_ci_status({"statusCheckRollup": []}) is None
    assert rm.check_ci_status({
        "statusCheckRollup": [{"workflowName": "ACU CSE 101 - TA Automated Grading", "conclusion": "SUCCESS"}]
    }) is True
    assert rm.check_ci_status({
        "statusCheckRollup": [{"name": "grade", "conclusion": "FAILURE"}]
    }) is False


def test_route_pr_base_already_correct():
    class DummyAPI:
        pass

    assert rm.route_pr_base(DummyAPI(), "test/repo", 1, "student1", "student1") is True
