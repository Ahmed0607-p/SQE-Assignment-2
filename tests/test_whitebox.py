
import registration
from registration import Student, Course, registration_decision, register_course


def test_WB01_dues_above_1000_executes_dues_block_return():
    student = Student("S-WB-01", outstanding_dues=1001)
    course = Course("CS-WB", 3, 10, enrolled=2)
    assert registration_decision(student, course) == "DUES_BLOCK"


def test_WB02_waitlisted_student_is_appended_without_other_state_changes(monkeypatch):
    student = Student("S-WB-02", current_credits=6)
    course = Course("CS-WB", 3, 10, enrolled=10)
    monkeypatch.setattr(registration, "registration_decision", lambda _s, _c: "WAITLISTED")

    result = register_course(student, course)

    assert result == "WAITLISTED"
    assert course.waitlist == ["S-WB-02"]
    assert student.registered_courses == set()
    assert student.current_credits == 6
    assert course.enrolled == 10


def test_WB03_existing_waitlist_entry_is_not_appended_twice(monkeypatch):
    student = Student("S-WB-03", current_credits=6)
    course = Course("CS-WB", 3, 10, enrolled=10, waitlist=["S-WB-03"])
    monkeypatch.setattr(registration, "registration_decision", lambda _s, _c: "WAITLISTED")

    result = register_course(student, course)

    assert result == "WAITLISTED"
    assert course.waitlist == ["S-WB-03"]
    assert student.registered_courses == set()
    assert student.current_credits == 6
    assert course.enrolled == 10


def test_WB04_dues_validation_precedes_invalid_capacity():
    """FR-15: negative dues must be validated before capacity/enrollment."""
    import pytest

    student = Student("S-WB-04", outstanding_dues=-1)
    course = Course("CS-WB", 3, 0, enrolled=0)
    with pytest.raises(ValueError, match="^Invalid dues$"):
        registration_decision(student, course)
