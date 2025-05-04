# Hybrid API and UI Automation Testing Framework

## Table of Contents
1. [Introduction](#introduction)
2. [Framework Architecture](#framework-architecture)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Running Tests](#running-tests)
6. [API Testing](#api-testing)
7. [UI Testing](#ui-testing)
8. [Reporting](#reporting)
9. [Extending the Framework](#extending-the-framework)
10. [Best Practices](#best-practices)
11. [Allure Reporting Implementation Guide](#Allure-Reporting-Implementation-Guide)

## Introduction

This hybrid automation testing framework is designed to support both API and UI testing using Python with pytest, requests, and Selenium. The framework follows a modular architecture with clear separation of concerns, making it easy to maintain and extend.

### Key Features

- Support for both API and UI testing
- Environment-based configuration (staging, production)
- Parameterized testing with data-driven approach
- Page Object Model pattern for UI testing
- Support for local and cloud-based browser testing (BrowserStack, LambdaTest)
- Comprehensive logging and reporting
- Modular and extensible architecture
- Data sharing between API tests

## Framework Architecture

The framework follows a layered architecture with the following components:

```
hybrid_python_automation_framework/
│
│
├── config/                      # Configuration files
│   ├── config.ini               # General framework configuration
│   ├── environment.py           # Environment configuration handler
│   ├── .env.staging             # Staging environment variables
│   └── .env.prod                # Production environment variables
│
├── test_data/                        # JSON test data files
│   └── TodoListData/            # Test data for API tests
│        ├── Create_todos.json   # Create To-Dos API test data
│        └── Delete_todo.json    # Delete To-Dos API test data
│
├── logs/                        # Test execution logs
│
├── reports/                     # Test reports
│   ├── html_report/             # HTML reports
│   └── screenshots/             # Test failure screenshots
│
├── src/                         # Source code
│   ├── base/                    # Base components
│   │   ├── api_client.py        # API client for making requests
│   │   └── web_driver.py        # WebDriver manager
│   │
│   ├── utils/                   # Utility modules
│   │   ├── api_utilities.py     # Utility and Validation functions for API testing
│   │   ├── file_reader.py       # File reader for test data
│   │   ├── logger.py            # Logging utility
│   │   ├── allure_reporter.py   # Allure Function
│   │   └── Shared_API_Data.py   # Shared data between API tests
│   │
│   └── pages/                   # Page Objects for UI testing
│       ├── base_page.py         # Base page with common methods
│       └── locators.py          # UI element locators
│       ├── RahulshettyAcademyPage/
│
├── tests/                       # Test modules
│   ├── api/                     # API tests
│   └── ui/                      # UI tests
│
├── conftest.py                  # Pytest fixtures and configuration
├── pytest.ini                   # Pytest configuration
├── requirements.txt             # Dependencies
└── README.md                    # Project documentation
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Chrome, Firefox, or Edge browser

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd hybrid_python_automation_framework
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  
# On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

### Environment Configuration

The framework supports different environments (staging, production) through environment-specific configuration files:

- `.env.staging`: Staging environment variables
- `.env.prod`: Production environment variables

These files contain environment-specific variables such as API URLs, credentials, and browser settings.

### Environment Variables

The following environment variables are used by the framework:

#### API Testing
- `TO_DOS`: TO_DOS Base URL for API testing


#### UI Testing
- `UI_BASE_URL`: Base URL for UI testing
- `BROWSER`: Browser to use for UI tests (chrome, firefox, edge)
- `HEADLESS`: Whether to run browser in headless mode (True/False)
- `IMPLICIT_WAIT`: Implicit wait time in seconds
- `EXPLICIT_WAIT`: Explicit wait time in seconds

#### Remote Testing
- `REMOTE_URL`: URL for remote WebDriver (BrowserStack/LambdaTest)
- `BS_USERNAME`: BrowserStack/LambdaTest username
- `BS_ACCESS_KEY`: BrowserStack/LambdaTest access key
- `PLATFORM`: Platform for remote testing (Windows, macOS, iOS, Android)
- `BROWSER_VERSION`: Browser version for remote testing
- `RESOLUTION`: Screen resolution for remote testing

## Running Tests

### Command Line Options

The framework supports various command line options for test execution:

- `--environment`: Specify the environment (staging, prod)
- `--browser`: Specify the browser for UI tests (chrome, firefox, edge)
- `--remote`: Run tests on remote browser (BrowserStack/LambdaTest)
- `--platform`: Specify platform for remote testing (Windows, macOS, iOS, Android)
- `--headless`: Run browser in headless mode
- `--test-type`: Type of tests to run (api, ui, all)

### Running API Tests

To run API tests only:

```bash
pytest tests --test-type=api --environment=staging -v
```

### Running UI Tests

To run UI tests locally:

```bash
pytest tests --test-type=ui --environment=staging --browser=chrome -v
```

To run UI tests on BrowserStack or LambdaTest:

```bash
pytest tests --test-type=ui --environment=staging --browser=chrome --remote --platform=Windows -v
```

### Running All Tests In Local

To run all tests:

```bash
pytest tests --test-type=all --environment=staging -v
```

## API Testing

### API Client

The framework includes a flexible API client (`API_Utilities/api_client.py`) that supports:

- Different HTTP methods (GET, POST, PUT, DELETE, PATCH)
- Request customization
- Response validation
- JSON schema validation
- Detailed logging

### API Utilities

The framework includes various utility modules for API testing:

- `api_utilities.py`: Utility functions for API testing
- `api_validations.py`: Validation functions for API testing
- `file_reader.py`: File reader for test data
- `Shared_API_Data.py`: Shared data between API tests

### Test Data

API test data is defined in JSON files (`data/test_data/AITestPlatformData/*.json`) with the following structure:

```json
{
  "positive": [
    {
      "endpoint": "/api/endpoint",
      "method": "GET",
      "headers": {
        "Content-Type": "application/json",
        "Authorization": "Bearer {{jwtToken}}"
      },
      "params": {},
      "payload": null,
      "expected_status": 200,
      "expected_schema": {}
    }
  ],
  "negative": [
    {
      "endpoint": "/api/endpoint",
      "method": "GET",
      "headers": {
        "Content-Type": "application/json",
        "Authorization": "Bearer {{jwtToken}}"
      },
      "params": {},
      "payload": null,
      "expected_status": 404,
      "expected_schema": {}
    }
  ]
}
```

### Creating API Tests

API tests are created using pytest's parameterization feature:

```python
import pytest
import os
from src.utils.shared_API_Data import shared_data
from src.utils.api_utilities import validate_response_code, validate_schema, validate_response_content_type, \
    validate_in_response_body, get_value_from_response
from src.utils.file_reader import read_file
from src.utils import logger
log = logger.customLogger()

testcasedata = read_file("TodoListData", 'Create_todos.json')

@pytest.mark.Positive
@pytest.mark.parametrize("case", testcasedata["Positive"])
def test_Create_Todo_Positive(api_request_context, case):

    log.info(f"Running test case: {case['description']}")

    baseURL = os.getenv('TO_DOS')

    # Make API request
    response = api_request_context.make_request(
        base_url=baseURL,
        method=case["method"],
        api_endpoint=case["endpoint"],
        header=case["headers"],
        payload=case["payload"]
    )

    # Validate response
    validate_response_code(response, case["expected_status"])

    # Validate content type
    validate_response_content_type(response)

    validate_in_response_body(response, 'data.title', case["payload"]["title"], 'title not matches')
    validate_in_response_body(response, 'data.description', case["payload"]["description"], 'description not matches')

    shared_data.set_data("todos_id", get_value_from_response(response, 'data._id'))

    # Validate schema if provided
    if "expected_schema" in case and case["expected_schema"]:
        validate_schema(response=response, schema=case["expected_schema"])
```

## UI Testing

### WebDriver Manager

The framework includes a WebDriver manager (`src/base/web_driver.py`) that supports:

- Local browser testing (Chrome, Firefox, Edge)
- Remote browser testing (BrowserStack, LambdaTest)
- Browser configuration (headless mode, window size, etc.)

### Page Object Model

UI tests follow the Page Object Model pattern with:

- Base page (`src/pages/base_page.py`) with common methods
- Page-specific classes
- Centralized locators (`src/pages/locators.py`)

### Creating UI Tests

UI tests are created using the Page Object Model pattern:

```python
import pytest
from src.pages.login_page import LoginPage
from src.pages.dashboard_page import DashboardPage
from API_Utilities.logger_utility import customLogger

log = customLogger()

class TestLogin:
    def test_valid_login(self, driver, ui_test_data):
        # Initialize pages
        login_page = LoginPage(driver)
        dashboard_page = DashboardPage(driver)
        
        # Perform login
        login_page.open_login_page()
        login_page.login("username", "password")
        
        # Verify login success
        assert dashboard_page.is_dashboard_displayed()
```

## Reporting

### HTML Reports

The framework generates HTML reports using pytest-html with custom enhancements:

- Test execution summary
- Environment information
- Test details with descriptions
- Screenshots for UI test failures

HTML reports are saved to `reports/html_report/report.html`.

### Logging

The framework includes comprehensive logging with:

- Console logging
- File logging to `logs/test_execution_<timestamp>.log`
- Configurable log levels (INFO, DEBUG, etc.)
- Detailed log format with timestamps and source information

## Extending the Framework

### Adding New API Tests

1. Add test data to `data/test_data/AITestPlatformData/`
2. Create a new test module in `tests/api/`
3. Implement test functions using the API client and test data

### Adding New UI Tests

1. Add locators to `src/pages/locators.py`
2. Create page objects in `src/pages/`
3. Add test data if needed
4. Create a new test module in `tests/ui/`
5. Implement test functions using page objects

### Adding New Environments

1. Create a new environment file (e.g., `.env.dev`)
2. Add environment-specific variables
3. Use the new environment with `--environment=dev`

## Best Practices

### API Testing

- Use parameterized tests for different test cases
- Validate response status codes and schemas
- Share response data between related tests
- Handle API errors gracefully
- Keep test data in JSON files

### UI Testing

- Follow the Page Object Model pattern
- Keep locators centralized and well-organized
- Use explicit waits for reliable element interactions
- Take screenshots on test failures
- Run tests in headless mode for CI/CD pipelines

### General

- Use descriptive test names and docstrings
- Keep test data separate from test logic
- Log important information for debugging
- Use fixtures for common setup and teardown
- Run tests in parallel when possible


## Allure Reporting Implementation Guide

## Overview

This document provides instructions on how to use Allure reporting in the automation framework. Allure provides rich and detailed test reports with features like test steps, attachments, and categorization.



## Setup

Allure is already included in the framework dependencies. Make sure you have installed all requirements:

```bash
pip install -r requirements.txt
```

To generate Allure reports, you need to install the Allure command-line tool:

### For Linux:
```bash
sudo apt-add-repository ppa:qameta/allure
sudo apt-get update
sudo apt-get install allure
```

### For macOS:
```bash
brew install allure
```

### For Windows:
```bash
scoop install allure
```

## Running Tests with Allure

To run tests with Allure reporting enabled, use the following command:

```bash
pytest tests --test-type=api --environment=staging --alluredir=reports/allure-results
```

This will run the tests and generate Allure result files in the `reports/allure-results` directory.

## Generating Allure Reports

After running the tests, generate the Allure report with:

```bash
allure serve reports/allure-results
```

This will generate and open the report in your default web browser.

To generate a static report:

```bash
allure generate reports/allure-results -o reports/allure-report
```

Then you can open the report by opening `reports/allure-report/index.html` in a web browser.

## Allure Features Used in Framework

The framework uses the following Allure features:

1. **Epic, Feature, and Story**: Hierarchical organization of tests
2. **Test Title and Description**: Detailed test information
3. **Severity Levels**: Indicating test importance
4. **Steps**: Breaking down test execution into logical steps
5. **Attachments**: Including screenshots, request/response data, and test data
6. **Dynamic Test Metadata**: Setting test metadata at runtime

## API Test Example

The API test example (`test_01_Create_Todo.py`) demonstrates:

- Setting Epic, Feature, and Story
- Adding test title and description
- Setting severity level
- Breaking down test into steps
- Attaching request and response data
- Attaching test data

Example:

```python
import allure
import pytest
import os
from src.utils.shared_API_Data import shared_data
from src.utils.api_utilities import validate_response_code, validate_schema, validate_response_content_type, \
    validate_in_response_body, get_value_from_response
from src.utils.file_reader import read_file
from src.utils.allure_reporter import (
    allure_step,
    add_allure_step,
    attach_request_data,
    attach_response_data,
    attach_test_data
)
from src.utils import logger


log = logger.customLogger()

testcasedata = read_file("TodoListData", 'Create_todos.json')

@allure.epic("API Testing")
@allure.feature("Todo_List")
@pytest.mark.Positive
@pytest.mark.parametrize("case", testcasedata["Positive"])
def test_Create_Todo_Positive(api_request_context, case):
    # Allure test metadata
    allure.dynamic.story("Positive User API Tests")
    allure.dynamic.title(f"Test User API: {case['endpoint']} - {case['method']}")
    allure.dynamic.description(f"Testing {case['method']} request to {case['endpoint']} with expected status {case.get('expected_status', 200)}")
    allure.dynamic.severity(allure.severity_level.NORMAL)
    # Attach test data to report
    attach_test_data(case)
    # Setup test
    add_allure_step("Setting up test environment")

    log.info(f"Running test case: {case['description']}")

    baseURL = os.getenv('TO_DOS')

    with allure.step(f"Making {case['method']} request to {baseURL}{case['endpoint']}"):
        # Attach request data
        attach_request_data(
            method=case["method"],
            url=f"{baseURL}{case['endpoint']}",
            headers=case["headers"],
            payload=case["payload"]
        )

        # Make API request
        response = api_request_context.make_request(
            base_url=baseURL,
            method=case["method"],
            api_endpoint=case["endpoint"],
            header=case["headers"],
            payload=case["payload"]
        )

        # Attach response data
        attach_response_data(response)

    # Validate response
    with allure.step("Validating response status code"):
        status_valid=validate_response_code(response, case["expected_status"])
    
    # Validate content type
    with allure.step("Validating response content type"):
        validate_response_content_type(response)
        
    # Validate response body
    with allure.step("Validating response body content "):
        validate_in_response_body(response, 'data.title', case["payload"]["title"], 'title not matches')
        validate_in_response_body(response, 'data.description', case["payload"]["description"], 'description not matches')


    shared_data.set_data("todos_id", get_value_from_response(response, 'data._id'))

    # Validate schema if provided
    with allure.step("Validating response schema"):
        if "expected_schema" in case and case["expected_schema"]:
            validate_schema(response=response, schema=case["expected_schema"])
```
### 📊 Sample Allure Report

![Allure Report Screenshot](docs/images/allure_report_api.png)


## UI Test Example

The UI test example (`test_login_allure.py`) demonstrates:

- Setting Epic, Feature, and Story
- Adding test title and description
- Setting severity level
- Breaking down test into steps
- Attaching screenshots at different test stages

Example:

```python
@allure.epic("UI Testing")
@allure.feature("Authentication")
class TestLogin:
    @allure.story("Login Functionality")
    @allure.title("Verify Login with Valid Credentials")
    @allure.description("This test verifies that a user can successfully login with valid credentials")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.ui
    def test_login_with_valid_credentials(self, driver):
        # Test steps with allure.step
        with allure.step("Opening login page"):
            # Step implementation
        
        # Attach screenshots
        screenshot_path = base_page.take_screenshot("login_page.png")
        attach_screenshot(screenshot_path, "Login Page Screenshot")
```

## Best Practices

1. **Use Hierarchical Organization**: 
   - Epic: High-level feature area (e.g., "API Testing", "UI Testing")
   - Feature: Specific feature (e.g., "Todo_List", "Authentication")
   - Story: User story or test scenario (e.g., "Login Functionality")

2. **Add Descriptive Titles and Descriptions**:
   - Title should be clear and concise
   - Description should provide more details about the test purpose

3. **Set Appropriate Severity Levels**:
   - BLOCKER: Tests that block further testing
   - CRITICAL: Critical functionality tests
   - NORMAL: Regular functionality tests
   - MINOR: Minor functionality tests
   - TRIVIAL: Trivial tests

4. **Use Steps to Break Down Tests**:
   - Each logical step should be wrapped in `allure.step`
   - Steps should be descriptive and follow a logical sequence

5. **Add Relevant Attachments**:
   - Screenshots for UI tests
   - Request/response data for API tests
   - Test data for both API and UI tests

6. **Handle Failures Gracefully**:
   - Attach additional information on test failure
   - Take screenshots on UI test failures
