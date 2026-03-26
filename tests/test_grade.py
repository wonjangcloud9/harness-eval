"""Tests for grade system."""

from harness_eval.models import pct_to_grade


def test_grade_a():
    assert pct_to_grade(95) == "A"
    assert pct_to_grade(90) == "A"


def test_grade_b():
    assert pct_to_grade(80) == "B"
    assert pct_to_grade(75) == "B"


def test_grade_c():
    assert pct_to_grade(60) == "C"
    assert pct_to_grade(55) == "C"


def test_grade_d():
    assert pct_to_grade(40) == "D"
    assert pct_to_grade(35) == "D"


def test_grade_f():
    assert pct_to_grade(20) == "F"
    assert pct_to_grade(0) == "F"
