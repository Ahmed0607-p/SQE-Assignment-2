# Student Course Registration System – Testing Assignment

This project tests the Student Course Registration System provided for the assignment.

## Important note

The file `registration.py` is the original program supplied for testing. It has not been changed. The expected results in the tests come from `REQUIREMENTS.md` and the SRS document. Some tests may fail because they show problems in the original program. Keep those failures as evidence.

## Install the required packages

```bash
python -m pip install -r requirements.txt
```

## Run the tests

Run black-box tests:

```bash
python -m pytest tests/test_blackbox.py -v
```

Run white-box tests:

```bash
python -m pytest tests/test_whitebox.py -v
```

Run all tests with statement and branch coverage:

```bash
python -m pytest tests/ --cov=registration --cov-branch --cov-report=term-missing
```

Do not change a test's expected result just to make it pass. If a defect is fixed, make the change on a separate branch after saving the original test results.

## Project files

- `registration.py`: original program being tested.
- `REQUIREMENTS.md` and `Student_Registration_SRS.docx`: system requirements.
- `tests/test_blackbox.py`: tests based on inputs and expected results.
- `tests/test_whitebox.py`: tests based on the program's code paths.
- `docs/`: test cases, decision table, control flow graph, test report, and run results.
- `.github/workflows/tests.yml`: runs tests automatically on GitHub.


## Supporting files

The separate project ZIP package also includes the Word SRS, Excel test-design sheets, CFG image, and PDF report. Those binary files are not included in this GitHub upload; the source code, test suites, workflow, and text reports are available in this repository.
