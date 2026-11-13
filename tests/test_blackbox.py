
import pytest

from registration import (
    Student,
    Course,
    check_credit_limit,
    prerequisites_satisfied,
    registration_decision,
    register_course,
    withdraw_course,
)


def make_student(**kwargs):
    values = {"student_id": "S100", "completed_courses": set(),
              "current_credits": 0, "outstanding_dues": 0,
              "registered_courses": set()}
    values.update(kwargs)
    return Student(**values)


def make_course(**kwargs):
    values = {"code": "CS301", "credit_hours": 3, "capacity": 30,
              "enrolled": 10, "prerequisites": set(), "waitlist": []}
    values.update(kwargs)
    return Course(**values)


def state(student, course):
  
    return (
        student.student_id,
        set(student.completed_courses),
        student.current_credits,
        student.outstanding_dues,
        set(student.registered_courses),
        course.code,
        course.credit_hours,
        course.capacity,
        course.enrolled,
        set(course.prerequisites),
        list(course.waitlist),
    )


# A1: Equivalence Class Partitioning

def test_ECP01_valid_course_credits_and_zero_dues():
    student = make_student(current_credits=6, outstanding_dues=0)
    course = make_course(credit_hours=3)
    assert registration_decision(student, course) == "REGISTERED"


def test_ECP02_BVA19_positive_dues_block_registration():
    student = make_student(outstanding_dues=1)
    assert registration_decision(student, make_course()) == "DUES_BLOCK"


def test_ECP03_negative_dues_are_invalid():
    with pytest.raises(ValueError, match="^Invalid dues$"):
        registration_decision(make_student(outstanding_dues=-1), make_course())


def test_ECP04_empty_prerequisite_list_is_satisfied():
    assert prerequisites_satisfied(set(), set()) is True


def test_ECP05_all_prerequisites_completed():
    student = make_student(completed_courses={"CS101", "MATH101"})
    course = make_course(prerequisites={"CS101", "MATH101"})
    assert registration_decision(student, course) == "REGISTERED"


def test_ECP06_only_some_prerequisites_completed():
    student = make_student(completed_courses={"CS101"})
    course = make_course(prerequisites={"CS101", "MATH101"})
    assert registration_decision(student, course) == "PREREQUISITES_MISSING"


def test_ECP07_no_prerequisites_completed():
    course = make_course(prerequisites={"CS101"})
    assert registration_decision(make_student(), course) == "PREREQUISITES_MISSING"


def test_ECP08_course_already_registered():
    student = make_student(registered_courses={"CS301"})
    assert registration_decision(student, make_course()) == "ALREADY_REGISTERED"


def test_ECP09_seats_are_available():
    course = make_course(capacity=30, enrolled=12)
    assert registration_decision(make_student(), course) == "REGISTERED"


def test_ECP10_BVA13_course_is_full():
    course = make_course(capacity=30, enrolled=30)
    assert registration_decision(make_student(), course) == "WAITLISTED"


def test_ECP11_course_credit_hours_below_valid_class():
    with pytest.raises(ValueError, match="^Invalid course credits$"):
        check_credit_limit(2, 0)


def test_ECP12_course_credit_hours_above_valid_class():
    with pytest.raises(ValueError, match="^Invalid course credits$"):
        check_credit_limit(2, 5)


# A2: Boundary Value Analysis

def test_BVA01_current_credits_at_lower_boundary_zero():
    assert check_credit_limit(0, 1) is True


def test_BVA02_current_credits_one_above_lower_boundary():
    assert check_credit_limit(1, 2) is True


def test_BVA03_current_credits_at_upper_boundary_with_min_course():
    assert check_credit_limit(18, 1) is False


def test_BVA04_current_credits_outside_upper_boundary():
    with pytest.raises(ValueError, match="^Invalid current credits$"):
        check_credit_limit(19, 1)


def test_BVA05_course_credits_at_lower_boundary():
    assert check_credit_limit(10, 1) is True


def test_BVA06_course_credits_at_upper_boundary():
    assert check_credit_limit(10, 4) is True


def test_BVA07_course_credits_one_below_lower_boundary():
    with pytest.raises(ValueError, match="^Invalid course credits$"):
        check_credit_limit(10, 0)


def test_BVA08_course_credits_one_above_upper_boundary():
    with pytest.raises(ValueError, match="^Invalid course credits$"):
        check_credit_limit(10, 5)


def test_BVA09_combined_credits_one_below_maximum():
    assert check_credit_limit(14, 3) is True


def test_BVA10_combined_credits_exactly_maximum():
    assert check_credit_limit(15, 3) is True


def test_BVA11_combined_credits_one_above_maximum():
    assert check_credit_limit(16, 3) is False


def test_BVA12_enrollment_one_below_capacity():
    course = make_course(capacity=8, enrolled=7)
    assert registration_decision(make_student(), course) == "REGISTERED"


# BVA13 is executed once by ECP10 (same 30/30 full-course case).

def test_BVA14_enrollment_above_capacity_is_invalid():
    course = make_course(capacity=8, enrolled=9)
    with pytest.raises(ValueError, match="^Invalid capacity or enrollment$"):
        registration_decision(make_student(), course)


def test_BVA15_minimum_valid_capacity():
    course = make_course(capacity=1, enrolled=0)
    assert registration_decision(make_student(), course) == "REGISTERED"


def test_BVA16_capacity_below_minimum_is_invalid():
    course = make_course(capacity=0, enrolled=0)
    with pytest.raises(ValueError, match="^Invalid capacity or enrollment$"):
        registration_decision(make_student(), course)


def test_BVA17_dues_at_zero_allow_registration():
    student = make_student(outstanding_dues=0)
    assert registration_decision(student, make_course()) == "REGISTERED"


def test_BVA18_current_credits_one_below_upper_boundary():
    assert check_credit_limit(17, 1) is True


def test_BVA20_current_credits_below_lower_boundary():
    with pytest.raises(ValueError, match="^Invalid current credits$"):
        check_credit_limit(-1, 1)


def test_BVA21_enrollment_below_zero_is_invalid():
    course = make_course(capacity=8, enrolled=-1)
    with pytest.raises(ValueError, match="^Invalid capacity or enrollment$"):
        registration_decision(make_student(), course)


# BVA19 is executed once by ECP02 (same dues=1 case).


# A3: Decision Table Testing

def test_DT01_only_dues_condition_true():
    assert registration_decision(make_student(outstanding_dues=25), make_course()) == "DUES_BLOCK"


def test_DT02_only_duplicate_condition_true():
    student = make_student(registered_courses={"CS301"})
    assert registration_decision(student, make_course()) == "ALREADY_REGISTERED"


def test_DT03_only_missing_prerequisite_condition_true():
    course = make_course(prerequisites={"CS201"})
    assert registration_decision(make_student(), course) == "PREREQUISITES_MISSING"


def test_DT04_only_credit_limit_condition_true():
    student = make_student(current_credits=17)
    course = make_course(credit_hours=2)
    assert registration_decision(student, course) == "CREDIT_LIMIT"


def test_DT05_only_full_seat_condition_true():
    course = make_course(capacity=5, enrolled=5)
    assert registration_decision(make_student(), course) == "WAITLISTED"


def test_DT06_no_blocking_condition_and_seat_available():
    course = make_course(capacity=5, enrolled=4)
    assert registration_decision(make_student(), course) == "REGISTERED"


def test_DT07_dues_has_priority_over_duplicate():
    student = make_student(outstanding_dues=10, registered_courses={"CS301"})
    assert registration_decision(student, make_course()) == "DUES_BLOCK"


def test_DT08_duplicate_has_priority_over_missing_prerequisite():
    student = make_student(registered_courses={"CS301"})
    course = make_course(prerequisites={"CS201"})
    assert registration_decision(student, course) == "ALREADY_REGISTERED"


def test_DT09_missing_prerequisite_has_priority_over_credit_limit():
    student = make_student(current_credits=17)
    course = make_course(credit_hours=2, prerequisites={"CS201"})
    assert registration_decision(student, course) == "PREREQUISITES_MISSING"


def test_DT10_credit_limit_has_priority_over_full_seats():
    student = make_student(current_credits=17)
    course = make_course(credit_hours=2, capacity=4, enrolled=4)
    assert registration_decision(student, course) == "CREDIT_LIMIT"


def test_DT11_dues_has_priority_over_all_other_conditions():
    student = make_student(outstanding_dues=1, registered_courses={"CS301"},
                           current_credits=18)
    course = make_course(credit_hours=4, capacity=3, enrolled=3,
                         prerequisites={"CS201"})
    assert registration_decision(student, course) == "DUES_BLOCK"


def test_DT12_duplicate_has_priority_over_prerequisite_credit_and_seats():
    student = make_student(registered_courses={"CS301"}, current_credits=18)
    course = make_course(credit_hours=4, prerequisites={"CS201"},
                         capacity=2, enrolled=2)
    assert registration_decision(student, course) == "ALREADY_REGISTERED"


# A4: State changes and non-mutation checks

def test_STATE01_successful_registration_updates_all_required_state():
    student = make_student(current_credits=6)
    course = make_course(credit_hours=3, capacity=10, enrolled=4)
    assert register_course(student, course) == "REGISTERED"
    assert student.registered_courses == {"CS301"}
    assert student.current_credits == 9
    assert course.enrolled == 5


def test_STATE02_waitlisting_adds_student_once_without_other_changes():
    student = make_student(current_credits=6)
    course = make_course(credit_hours=3, capacity=4, enrolled=4)
    before = state(student, course)
    assert register_course(student, course) == "WAITLISTED"
    after = state(student, course)
    assert after[:-1] == before[:-1]
    assert after[-1] == ["S100"]
    assert register_course(student, course) == "WAITLISTED"
    assert course.waitlist == ["S100"]


def test_STATE03_failed_registration_does_not_change_state():
    student = make_student(outstanding_dues=1, current_credits=5)
    course = make_course(enrolled=7, capacity=10)
    before = state(student, course)
    assert register_course(student, course) == "DUES_BLOCK"
    assert state(student, course) == before


def test_STATE04_registration_decision_does_not_mutate_objects():
    student = make_student(current_credits=5)
    course = make_course(enrolled=7, capacity=10)
    before = state(student, course)
    assert registration_decision(student, course) == "REGISTERED"
    assert state(student, course) == before


def test_STATE05_successful_withdrawal_updates_student_and_course():
    student = make_student(current_credits=9, registered_courses={"CS301"})
    course = make_course(credit_hours=3, enrolled=6)
    assert withdraw_course(student, course) is True
    assert student.registered_courses == set()
    assert student.current_credits == 6
    assert course.enrolled == 5


def test_STATE06_withdrawal_when_not_registered_changes_nothing():
    student = make_student(current_credits=9)
    course = make_course(credit_hours=3, enrolled=6)
    before = state(student, course)
    assert withdraw_course(student, course) is False
    assert state(student, course) == before


def test_STATE07_all_unsuccessful_registration_outcomes_preserve_state():
    scenarios = [
        (make_student(outstanding_dues=5), make_course(), "DUES_BLOCK"),
        (make_student(registered_courses={"CS301"}), make_course(), "ALREADY_REGISTERED"),
        (make_student(), make_course(prerequisites={"CS201"}), "PREREQUISITES_MISSING"),
        (make_student(current_credits=17), make_course(credit_hours=2), "CREDIT_LIMIT"),
    ]
    for student, course, expected in scenarios:
        before = state(student, course)
        assert register_course(student, course) == expected
        assert state(student, course) == before
