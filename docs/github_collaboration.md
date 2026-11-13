# GitHub Team Work Guide

This file explains how to put the assignment on GitHub and work with teammates. It does not claim that these steps have already been completed.

## 1. Repository

This project is stored in the GitHub repository:
https://github.com/Ahmed0607-p/SQE-Assignment-2

## 2. Create a branch for black-box tests

```bash
git switch -c blackbox-testing
git add tests/test_blackbox.py docs/blackbox_test_design.xlsx docs/decision_table.xlsx docs/initial_blackbox_execution.txt
git commit -m "Add black-box test cases"
git push -u origin blackbox-testing
```

Open a pull request from `blackbox-testing` to `main`. Ask a teammate to review it.

## 3. Create a branch for white-box tests

```bash
git switch main
git pull
git switch -c whitebox-testing
git add tests/test_whitebox.py docs/cfg.png docs/analysis.md docs/testing_report.pdf docs/final_test_execution.txt
git commit -m "Add white-box tests and coverage report"
git push -u origin whitebox-testing
```

Open a second pull request and ask another teammate to review it.

## 4. Report the defects

Create one GitHub issue for each defect listed in the testing report:

- DEF-01: Positive dues do not block registration.
- DEF-02: Some missing prerequisites are accepted.
- DEF-03: Exactly 18 credits are rejected.
- DEF-04: A full course is not waitlisted.
- DEF-05: Withdrawal does not reduce course enrollment.

Copy the reproduction steps, expected result, and actual result from the report. Add the real issue links to the final report.

## 5. Run GitHub Actions

The workflow file is `.github/workflows/tests.yml`. After pushing the project, open the **Actions** tab on GitHub. Record the actual run link and result in the report.

The first run may show test failures. Do not remove valid tests to make the workflow green. The failures are evidence of problems in the supplied program.

## 6. Add real team details

Record each teammate's actual contribution, pull request, review, and issue links. Do not make up names, reviews, or links.
