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
automation_framework_updated/
│
├── API_Utilities/                # API testing utilities
│   ├── api_client.py            # API client for making requests
│   ├── api_utilities.py         # Utility functions for API testing
│   ├── api_validations.py       # Validation functions for API testing
│   ├── file_reader.py           # File reader for test data
│   ├── logger_utility.py        # Logging utility
│   └── Shared_API_Data.py       # Shared data between API tests
│
├── config/                      # Configuration files
│   ├── config.ini               # General framework configuration
│   ├── environment.py           # Environment configuration handler
│   ├── .env.staging             # Staging environment variables
│   └── .env.prod                # Production environment variables
│
├── data/                        # Test data
│   └── test_data/               # JSON test data files
│       └── AITestPlatformData/  # Test data for API tests
│           ├── workSector.json  # Work sector API test data
│           └── users.json       # Users API test data
│
├── logs/                        # Test execution logs
│
├── reports/                     # Test reports
│   ├── html_report/             # HTML reports
│   └── screenshots/             # Test failure screenshots
│
├── src/                         # Source code
│   ├── base/                    # Base components
│   │   └── web_driver.py        # WebDriver manager
│   │
│   ├── utils/                   # Utility modules
│   │
│   └── pages/                   # Page Objects for UI testing
│       ├── base_page.py         # Base page with common methods
│       └── locators.py          # UI element locators
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
cd automation_framework_updated
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
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
- `AI_TUTOR_URL`: Base URL for API testing
- `AI_TUTOR_TOKEN`: Authentication token for API testing

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
pytest tests/api --test-type=api --environment=staging -v
```

### Running UI Tests

To run UI tests locally:

```bash
pytest tests/ui --test-type=ui --environment=staging --browser=chrome -v
```

To run UI tests on BrowserStack or LambdaTest:

```bash
pytest tests/ui --test-type=ui --environment=staging --browser=chrome --remote --platform=Windows -v
```

### Running All Tests

To run all tests:

```bash
pytest --environment=staging -v
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
from API_Utilities.api_utilities import get_response_data, get_value_from_response
from API_Utilities.api_validations import validate_response_code, validate_in_response_body, validate_schema,
    validate_response_content_type
from src.utils.file_reader import read_file
from API_Utilities.Shared_API_Data import shared_data
import os
from API_Utilities import logger_utility

log = logger_utility.customLogger()

testcasedata = read_file("AITestPlatformData", 'workSector.json')


@pytest.mark.Positive
@pytest.mark.parametrize("case", testcasedata["positive"])
def test_workSector(api_request_context, case):
    baseURL = os.getenv('AI_TUTOR_URL')
    token = os.getenv('AI_TUTOR_TOKEN')
    case["headers"]["X-Resume-Builder-Token"] = token

    response = api_request_context.make_request(
        base_url=baseURL,
        method=case["method"],
        api_endpoint=case["endpoint"],
        header=case["headers"],
        payload=case["payload"]
    )

    validate_schema(response=response, schema=case['expected_schema'])
    validate_response_content_type(response)
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
