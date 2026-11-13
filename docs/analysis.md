# Testing Report – Student Course Registration System

## 1. Introduction

The aim of this assignment is to test the given Student Course Registration System. We used black-box testing and white-box testing. The requirements document was used to decide what the correct result should be.

The original `registration.py` file was kept unchanged during the first round of testing. This is important because the tests should show problems in the supplied program, not hide them.

## 2. Black-box testing

Black-box testing checks the program by giving it inputs and checking the results. It does not depend on how the code is written.

### 2.1 Equivalence Class Partitioning (ECP)

We divided the input values into groups that should behave in the same way. We then selected examples from those groups.

The main groups were:

- Course credit hours from 1 to 4 are allowed. Values below 1 or above 4 are not allowed.
- A student with zero dues can register. Positive dues should stop registration. Negative dues are invalid.
- A student must have all required prerequisite courses completed.
- A course with an available seat can accept a student. A full course should put the student on the waiting list.
- A student must not register for the same course twice.

Twelve ECP cases are included in `tests/test_blackbox.py`. Their IDs start with `ECP`.

### 2.2 Boundary Value Analysis (BVA)

BVA checks values at the limits and just outside the limits. We checked:

- Current credits: 0 and 18, plus values outside this range.
- Course credits: 1 and 4, plus values outside this range.
- Total credits after adding a course: 17, 18, and 19.
- Course capacity: one seat left, full capacity, and invalid enrollment values.
- Outstanding dues: zero and a small positive amount.

The test IDs start with `BVA`. Two cases are not run twice because they are exactly the same as ECP cases: BVA-13 is the same full-course case as ECP-10, and BVA-19 is the same positive-dues case as ECP-02. Both remain listed in the design so the requirements can be traced.

### 2.3 Decision table testing

The decision table checks the order in which the program should make its decision. The required order is:

1. Check outstanding dues.
2. Check whether the course is already registered.
3. Check prerequisites.
4. Check the credit limit.
5. Check course seats.

If none of these checks blocks registration and a seat is available, the result is `REGISTERED`. If the course is full, the result should be `WAITLISTED`.

The decision table and its test cases are in `docs/decision_table.xlsx`. The related test IDs start with `DT`.

### 2.4 Checking changes to data

The tests also check what happens to the student and course data after registration or withdrawal. They check that a failed operation does not change the data. They also check that a student is added to the waiting list only once.

## 3. White-box testing

White-box testing checks the paths and decisions inside the program.

### 3.1 Control Flow Graph (CFG)

The control flow graph is saved as `docs/cfg.png`. It shows the main steps and decisions in `registration_decision()`.

Using the graph in this report:

- Nodes (N) = 17
- Edges (E) = 23
- Cyclomatic complexity = E - N + 2
- V(G) = 23 - 17 + 2 = 8

There are seven `if` decision points in the selected graph, so decisions + 1 = 7 + 1 = 8. Both methods give the same result.

This count treats each `if` statement as one decision. Python may also check more than one condition inside a statement. Those short-circuit conditions are discussed separately below.

### 3.2 Basis paths

The eight paths are linked to tests in `tests/test_whitebox.py` and `tests/test_blackbox.py`. One path that should return `WAITLISTED` cannot be reached normally in the supplied program. The earlier validation rejects enrollment above capacity, while the later decision checks for that same situation. The test suite uses a controlled test replacement to check the waiting-list update code separately. This does not claim that the normal decision function reached that path.

### 3.3 Statement and branch coverage

Coverage was measured with `pytest-cov`.

| Measure | Black-box tests | Black-box + white-box tests |
|---|---:|---:|
| Tests collected | 50 | 54 |
| Passed | 37 | 41 |
| Failed | 13 | 13 |
| Statements covered | 53 of 57 | 56 of 57 |
| Statement coverage | 93.0% | 98.2% |
| Branches covered | 21 of 26 | 25 of 26 |
| Branch coverage | 80.8% | 96.2% |

The 13 failures are kept because they show differences between the supplied program and the requirements. The remaining missed statement and branch are linked to the unreachable full-capacity decision described above.

### 3.4 Condition coverage and MC/DC

The coverage tool reports statement and branch coverage. It does not directly report condition coverage or MC/DC, so these were checked manually.

For the current-credit check, the two parts are:

- Is the current credit value at least zero?
- Is the current credit value no more than 18?

We used values 0, 19, and -1 to show true, false, and short-circuit behaviour.

For the enrollment check, the two parts are:

- Is the enrolled number outside the allowed range?
- Is the course capacity less than one?

We used normal enrollment, enrollment above capacity, zero capacity, and negative enrollment. When Python skips a condition because of short-circuit evaluation, it is marked as not evaluated rather than being counted as true or false.

## 4. Defects found

The tests found these five problems in the supplied program:

| ID | Problem | Expected result | Actual result in supplied program |
|---|---|---|---|
| DEF-01 | A small positive dues amount does not block registration. | Any positive dues should block registration. | The program blocks dues only above Rs. 1000. |
| DEF-02 | The program accepts a student who has completed only some prerequisites. | All prerequisites must be completed. | Registration can be accepted with a missing prerequisite. |
| DEF-03 | Exactly 18 total credits are rejected. | A total of 18 credits should be allowed. | The program rejects the exact limit. |
| DEF-04 | A full course is not sent to the waiting list. | The result should be `WAITLISTED`. | The program returns `REGISTERED` for a full course. |
| DEF-05 | Withdrawal does not reduce course enrollment. | Enrollment should decrease by one. | The student's course and credits change, but enrollment does not. |

A proposed fix is saved in `docs/proposed_defect_fixes.patch`. It was tested in a separate temporary copy. The original program in this submission was not changed.

## 5. Test execution summary

The first run used only the black-box tests. It collected 50 tests: 37 passed and 13 failed. After adding the white-box tests, the full suite collected 54 tests: 41 passed and 13 failed.

The extra white-box tests increased statement coverage from 93.0% to 98.2% and branch coverage from 80.8% to 96.2%. The failures remain because they point to defects in the original program.

## 6. GitHub work

The project includes a GitHub Actions workflow in `.github/workflows/tests.yml`. It is set to run tests when code is pushed or a pull request is opened.

The local project also includes a suggested branch plan, issue descriptions, and pull request descriptions in `docs/github_collaboration.md`. These are instructions only. A repository, actual issues, pull requests, peer reviews, and Actions run links must be added after they have really been created on GitHub. They must not be reported as completed before that happens.

## 7. Conclusion

The assignment uses ECP, BVA, decision table testing, CFG, cyclomatic complexity, basis paths, condition coverage, and MC/DC. The tests found five issues in the original program. Adding white-box tests improved coverage, while keeping the original failures helped show where the program does not follow the requirements.
