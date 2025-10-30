# TEST PLAN - Flask To-Do List Application

## 1. INTRODUCTION

### 1.1 Project Overview
**Application Name:** Flask To-Do List Application  
**Platform:** Web Application  
**Programming Language:** Python 3.x  
**Framework:** Flask (Web Framework)  
**Testing Framework:** pytest  
**Environment:** Windows OS, PowerShell

### 1.2 Objectives
- Validate functionality of all features
- Ensure data integrity and timestamp accuracy
- Verify user interface behavior
- Identify and document defects
- Ensure application meets acceptance criteria

---

## 2. SCOPE OF TESTING

### 2.1 Features to be Tested

#### **Core Functionality**
1. **Task Management**
   - Add new tasks
   - Edit existing tasks
   - Delete tasks
   - Mark tasks as complete (single and multiple)
   - Clear pending tasks (keeps completed tasks)
   - Prevent duplicate tasks
   - Prevent empty tasks

2. **Timestamp Tracking**
   - Display task creation timestamp
   - Display task completion timestamp
   - Timestamp persistence across operations
   - Timestamp format validation

3. **User Interface**
   - Home page rendering
   - Pending tasks section
   - Completed tasks section
   - Task counter display
   - Form submissions
   - Navigation and redirects

4. **Data Validation**
   - Input sanitization (empty strings, whitespace)
   - Duplicate detection
   - Boundary conditions (long strings, special characters)
   - Invalid index handling

### 2.2 Features NOT to be Tested
- Database persistence (application uses in-memory storage)
- Multi-user functionality
- Authentication/Authorization
- Performance under high load
- Browser compatibility (focus on functionality)

---

## 3. BUG TAXONOMY

### 3.1 Bug Severity Levels

| Severity | Description | Example |
|----------|-------------|---------|
| **Critical** | Application crash, data loss, core functionality broken | Server crash when adding task |
| **High** | Major feature not working, no workaround | Cannot mark tasks as complete |
| **Medium** | Feature partially broken, workaround exists | Timestamp not displaying |
| **Low** | Minor UI issue, cosmetic defect | Inconsistent spacing |

### 3.2 Bug Categories

1. **Functional Bugs**
   - Feature not working as specified
   - Incorrect data processing
   - Business logic errors

2. **UI/UX Bugs**
   - Display issues
   - Layout problems
   - Incorrect labels

3. **Data Integrity Bugs**
   - Data corruption
   - Incorrect data storage
   - Lost data

4. **Validation Bugs**
   - Missing input validation
   - Incorrect error handling
   - Security vulnerabilities

5. **Integration Bugs**
   - Route errors
   - Template rendering issues
   - Form submission problems

---

## 4. TEST APPROACH

### 4.1 Testing Types

#### **A. Black-Box Testing (Integration Tests)**
- **Focus:** User perspective, end-to-end workflows
- **Method:** Test through HTTP requests and response validation
- **Tool:** pytest with Flask test client
- **Coverage:** User interactions, page rendering, form submissions

#### **B. White-Box Testing (Unit Tests)**
- **Focus:** Internal functions, code logic, edge cases
- **Method:** Direct function calls with various inputs
- **Tool:** pytest
- **Coverage:** Helper functions, data structures, boundary conditions

### 4.2 Test Environment
- **Operating System:** Windows 10/11
- **Python Version:** 3.8+
- **Flask Version:** 2.x+
- **pytest Version:** 7.x+
- **Browser:** Any modern browser (Chrome, Firefox, Edge)

---

## 5. TEST SCENARIOS

### 5.1 Integration Test Scenarios (Black-Box)

| Test ID | Scenario | Priority |
|---------|----------|----------|
| TC-INT-001 | Verify home page loads successfully | High |
| TC-INT-002 | Verify task is added with creation timestamp | High |
| TC-INT-003 | Verify empty tasks are not added | High |
| TC-INT-004 | Verify duplicate tasks are prevented | Medium |
| TC-INT-005 | Verify task can be marked as complete | High |
| TC-INT-006 | Verify task can be deleted | High |
| TC-INT-007 | Verify multiple tasks can be marked complete | Medium |
| TC-INT-008 | Verify only pending tasks are cleared | Medium |
| TC-INT-009 | Verify task count is displayed correctly | Low |

### 5.2 Unit Test Scenarios (White-Box)

| Test ID | Scenario | Priority |
|---------|----------|----------|
| TC-UNIT-001 | Test add_task function with valid/invalid inputs | High |
| TC-UNIT-002 | Test toggle_task function and timestamp assignment | High |
| TC-UNIT-003 | Test delete_task function | High |
| TC-UNIT-004 | Test edit_task function | Medium |
| TC-UNIT-005 | Test clear_tasks function (pending only) | Medium |
| TC-UNIT-006 | Test timestamp persistence after toggle | Medium |
| TC-UNIT-007 | Test boundary conditions | Low |

---

## 6. TEST PROCEDURES

### 6.1 Test Execution Steps

#### **Step 1: Environment Setup**
```powershell
# Navigate to project directory
cd C:\Users\DELL\OneDrive\Desktop\flask_app_project

# Install dependencies
pip install -r requirements.txt
```

#### **Step 2: Run All Tests**
```powershell
# Execute all test cases
pytest tests/test_app.py -v

# Run with coverage report
pytest tests/test_app.py --cov=app --cov-report=html
```

#### **Step 3: Run Specific Test Categories**
```powershell
# Run only integration tests
pytest tests/test_app.py -v -k "integration"

# Run only unit tests
pytest tests/test_app.py -v -k "unit"
```

#### **Step 4: Manual Testing (Optional)**
```powershell
# Start the application
python app.py

# Access in browser: http://127.0.0.1:5000
# Perform manual exploratory testing
```

### 6.2 Test Data

#### **Valid Test Data**
- Task Name: "Buy groceries"
- Task Name: "Complete homework"
- Task Name: "Call dentist"
- Long Task: 500 character string
- Special Characters: "Task @#$% <>&"

#### **Invalid Test Data**
- Empty string: ""
- Whitespace only: "   "
- Duplicate: Same task text twice
- Invalid index: -1, 999

### 6.3 Expected Results

Each test case should:
1. Execute without errors
2. Return expected values (True/False for unit tests)
3. Produce correct HTTP status codes (200 for success)
4. Display correct data in UI
5. Maintain data integrity

---

## 7. TEST DELIVERABLES

1. **Test Cases Document** (tests/test_app.py)
2. **Test Execution Report** (TEST_REPORT.md)
3. **Code Coverage Report** (htmlcov/index.html)
4. **Bug Reports** (if any defects found)
5. **Test Summary Report**

---

## 8. PASS/FAIL CRITERIA

### 8.1 Individual Test Case Criteria

**PASS:**
- Test executes without errors
- Actual result matches expected result
- No exceptions or crashes
- Data integrity maintained

**FAIL:**
- Assertion failure
- Unexpected exception
- Incorrect output
- Application crash

### 8.2 Overall Application Acceptance Criteria

**Application is ACCEPTED if:**
- ✅ All Critical severity tests pass (100%)
- ✅ 95%+ of High priority tests pass
- ✅ 85%+ of Medium priority tests pass
- ✅ All core features functional
- ✅ No critical bugs remain

**Application is REJECTED if:**
- ❌ Any Critical test fails
- ❌ < 90% of High priority tests pass
- ❌ Core functionality broken
- ❌ Data loss or corruption occurs

---

## 9. RISK ANALYSIS

| Risk | Impact | Mitigation |
|------|--------|------------|
| In-memory data loss on restart | High | Document as known limitation |
| Concurrent access issues | Medium | Not applicable (single-user) |
| Invalid timestamp format | Medium | Validate format in tests |
| XSS through task input | High | Test with special characters |

---

## 10. TEST SCHEDULE

| Phase | Duration | Activities |
|-------|----------|------------|
| Test Planning | 1 day | Create test plan, identify scenarios |
| Test Case Development | 1 day | Write unit and integration tests |
| Test Execution | 0.5 day | Run all tests, document results |
| Defect Reporting | 0.5 day | Log bugs, prioritize fixes |
| Regression Testing | 0.5 day | Re-test after fixes |
| **Total** | **3.5 days** | |

---

## 11. TOOLS AND RESOURCES

### 11.1 Testing Tools
- **pytest:** Test framework and runner
- **Flask test_client:** HTTP testing
- **coverage.py:** Code coverage measurement
- **PowerShell:** Command execution

### 11.2 Human Resources
- Test Engineer: Create and execute tests
- Developer: Fix identified bugs
- QA Lead: Review test results

---

## 12. CONCLUSION

This test plan provides comprehensive coverage of the Flask To-Do List application through both black-box and white-box testing approaches. The combination of unit tests (testing internal functions) and integration tests (testing user workflows) ensures robust validation of all features and proper timestamp functionality.
