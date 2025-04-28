"""
Pytest configuration file.

This file contains fixtures and configuration for pytest.
"""
import base64
import os
import pathlib
import time
import uuid
from collections import defaultdict
from datetime import datetime
from typing import Dict, Optional
from pytest_metadata.plugin import metadata_key
import pytest
import requests
from py.xml import html
from requests.adapters import HTTPAdapter
from urllib3 import Retry
from config.environment import Environment
from src.base.api_client import APIClient
from src.base.web_driver import WebDriverManager
from src.utils import logger
log = logger.customLogger()


def pytest_addoption(parser):
    parser.addoption("--environment", action="store", default="staging", help="Environment to run tests against")
    parser.addoption("--browser", action="store", default=None, help="Browser to use for UI tests")
    parser.addoption("--remote", action="store_true", default=False, help="Run tests on remote platform")
    parser.addoption("--platform", action="store", default=None, help="Remote platform: Windows, macOS, etc.")
    parser.addoption("--headless", action="store_true", help="Run browser in headless mode")
    parser.addoption("--test-type",action="store",default="all",choices=["all", "api", "ui"],help="Run only specific test types: all, api, or ui")


@pytest.fixture(scope="session", autouse=True)
def setup_environment(request):
    env_name = request.config.getoption("--environment")
    log.info(f"🔧 Setting up environment: {env_name}")

    # Load environment using Environment class
    Environment(env_name)

    # Override other CLI-based environment variables
    if browser := request.config.getoption("--browser"):
        os.environ["BROWSER"] = browser

    if headless := request.config.getoption("--headless"):
        os.environ["HEADLESS"] = str(headless)

    if request.config.getoption("--remote"):
        os.environ["REMOTE"] = "True"

    if platform := request.config.getoption("--platform"):
        os.environ["PLATFORM"] = platform


@pytest.fixture(scope="session")
def api_session():
    log.info("🌐 Creating API session")
    session = requests.Session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504],allowed_methods=["HEAD", "GET", "OPTIONS", "POST", "PUT", "DELETE"],raise_on_status=False)
    adapter = HTTPAdapter(max_retries=retries)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    yield session
    session.close()


@pytest.fixture(scope="function")
def api_request_context(api_session):
     # Import your client class
    return APIClient(api_session)


@pytest.fixture(scope="class")
def driver_manager():
    """Create WebDriver Manager instance."""
    log.info("Creating WebDriver Manager")
    return WebDriverManager()


@pytest.fixture(scope="function")
def driver(request, driver_manager):
    """
    Create WebDriver instance.
    
    This fixture initializes a WebDriver instance for UI tests
    and handles cleanup after test completion.
    """
    remote = request.config.getoption("--remote")
    log.info(f"Initializing WebDriver (remote: {remote})")
    
    # Initialize driver
    driver = driver_manager.initialize_driver(remote=remote)
    
    # Yield driver to test
    yield driver
    
    # Quit driver after test
    driver_manager.quit_driver()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    now = datetime.now()
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()

    # ✅ Add description from parametrize or fixtures
    if "case" in item.fixturenames:
        case = item.callspec.params.get("case", {})
        description = case.get("description", "")
        setattr(report, "description", description)

    extra = getattr(report, 'extra', [])
    # Only attach screenshots on failure/skipped with xfail
    if report.when in ('call', 'setup'):
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            # Check if Selenium driver is available
            driver = item.funcargs.get("driver", None)
            if driver:
                try:
                    # Create screenshot directory
                    screenshots_dir = pathlib.Path(__file__).parent / "reports" / "screenshots"
                    screenshots_dir.mkdir(parents=True, exist_ok=True)

                    # Generate screenshot filename
                    file_name = report.nodeid.replace("::", "_").replace("/", "_") + ".png"
                    screenshot_path = screenshots_dir / file_name

                    # Save screenshot
                    driver.save_screenshot(str(screenshot_path))

                    # Encode image to base64
                    with open(screenshot_path, "rb") as f:
                        encoded_image = base64.b64encode(f.read()).decode("utf-8")
                        html = f'<div><img src="data:image/png;base64,{encoded_image}" ' \
                               f'style="width:400px;height:auto;" ' \
                               f'onclick="window.open(this.src)" align="right"/></div>'
                        extra.append(pytest_html.extras.html(html))
                except Exception as e:
                    print(f"Screenshot capture failed: {e}")

        report.extras = extra


def pytest_html_results_table_header(cells):
    """Add 'Description' column to report header."""
    cells.insert(2, html.th("Description"))
    cells.pop()  # Remove "Links" column if not needed


def pytest_html_results_table_row(report, cells):
    """Add 'Description' value to report row."""
    cells.insert(2, html.td(getattr(report, "description", "")))
    cells.pop()  # Remove "Links" column if not needed

@pytest.hookimpl(optionalhook=True)
def pytest_metadata(metadata):
    metadata.pop("Platform", None)
    metadata.pop("Packages", None)
    metadata.pop("Plugins", None)
    metadata.pop("JAVA_HOME", None)


# enve: str = "None"
def pytest_configure(config):
    # global enve
    enve=config.getoption('--environment')
    # Add custom metadata to the report
    config.stash[metadata_key]["Report ID"] = str(uuid.uuid4())[:8]
    config.stash[metadata_key]["Project Name"] = "API/UI Testing Report"
    config.stash[metadata_key]["Version"] = "1.0.0"
    config.stash[metadata_key]["Environment"] = enve
    config.stash[metadata_key]["Execution Time"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    config.stash[metadata_key]["Author"] = "Dipankar"

def pytest_html_report_title(report):
    report.title = "Pytest API/UI Testing Report"



def pytest_collection_modifyitems(config, items):
    for item in items:
        if "tests/api/" in item.nodeid:
            item.add_marker(pytest.mark.api)
        elif "tests/ui/" in item.nodeid:
            item.add_marker(pytest.mark.ui)


def pytest_ignore_collect(collection_path: pathlib.Path, config):
    """
    Prevent collecting test files from undesired directories based on --test-type.
    Uses pathlib.Path as required by Pytest 8+.
    """
    test_type = config.getoption("--test-type")
    path_norm = collection_path.as_posix()  # Normalize path for cross-platform

    if test_type == "api" and "/tests/ui/" in path_norm:
        return True
    elif test_type == "ui" and "/tests/api/" in path_norm:
        return True

    return False



test_data: Dict[str, Optional[float] | dict] = {
    "start_time": None,
    "end_time": None,
    "duration": None,
    "project_wise_results": defaultdict(
        lambda: defaultdict(
            lambda: {
                "total": 0,
                "passed": 0,
                "failed": 0,
                "skipped": 0,
                "PassedTest": [],
                "FailedTest": [],
                "SkippedTest": [],
            }
        )
    )
}




def get_test_group_and_project(nodeid):
    parts = nodeid.split("::")[0].split("/")
    if "tests" in parts:
        index = parts.index("tests")
        if index + 2 < len(parts):
            test_type = parts[index + 1]  # api or ui
            project = parts[index + 2]    # AiTutor or TestPlatform
            group = f"{test_type.upper()} Tests"
            return group, project
    return "Other Tests", "UnknownProject"


# def pytest_itemcollected(item):
#     """
#     Append the test case description to the nodeid while preserving the original nodeid.
#     """
#     if "case" in item.fixturenames:
#         case = item.callspec.params.get("case", {})
#         description = case.get("description", "")
#         if description:
#             # item._nodeid += f" - {description}"
#             # Remove [caseX] using regex
#             original_nodeid = re.sub(r"\[.*?\]", "", item.nodeid)
#             # Preserve original nodeid and append the description
#             item._nodeid = f"{original_nodeid} - {description}"


@pytest.hookimpl
def pytest_runtest_logreport(report):
    if report.when != "call":
        return

    test_name = report.nodeid
    duration = report.duration

    group, project = get_test_group_and_project(test_name)
    project_result = test_data["project_wise_results"][group][project]
    project_result["total"] += 1

    if report.passed:
        project_result["passed"] += 1
        project_result["PassedTest"].append({
            "name": test_name,
            "duration": f"{duration:.2f}s"
        })
    elif report.failed:
        project_result["failed"] += 1
        project_result["FailedTest"].append({
            "name": test_name,
            "duration": f"{duration:.2f}s",
            "reason": report.longrepr.reprcrash.message.splitlines()[0] #str(report.longrepr).splitlines()[0]
        })
    elif report.skipped:
        project_result["skipped"] += 1
        project_result["SkippedTest"].append({
            "name": test_name,
            "duration": f"{duration:.2f}s",
            "reason": str(report.longrepr)
        })


@pytest.hookimpl
def pytest_sessionstart(session):
    test_data["start_time"] = time.time()


@pytest.hookimpl
def pytest_terminal_summary(terminalreporter, exitstatus, config):
    test_data["end_time"] = time.time()
    if test_data["start_time"] is not None:
        test_data["duration"] = test_data["end_time"] - test_data["start_time"]
    else:
        test_data["duration"] = 0

    all_projects = test_data["project_wise_results"]

    total_tests = sum(sum(p["total"] for p in projects.values()) for projects in all_projects.values())
    total_passed = sum(sum(p["passed"] for p in projects.values()) for projects in all_projects.values())
    total_failed = sum(sum(p["failed"] for p in projects.values()) for projects in all_projects.values())
    total_skipped = sum(sum(p["skipped"] for p in projects.values()) for projects in all_projects.values())

    terminalreporter.write_sep("-", f"Total duration: {test_data['duration']:.2f} seconds")

    env = config.getoption("--environment") or "unknown"

    report = (
        f"\n\nAPI/UI Testing Report\n"
        f"{'=' * 25}\n"
        f"Environment: {env}\n"
        f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"Duration: {test_data['duration']:.2f} seconds\n\n"
        f"Summary:\n"
        f"- Total Tests: {total_tests}\n"
        f"- Passed: {total_passed}\n"
        f"- Failed: {total_failed}\n"
        f"- Skipped: {total_skipped}\n\n"
    )

    failed_tests = []

    for group, projects in all_projects.items():
        report += f"{group}:\n"
        for project, data in projects.items():
            report += (
                f"{project}:\n"
                f"- Total: {data['total']}, Passed: {data['passed']}, "
                f"Failed: {data['failed']}, Skipped: {data['skipped']}\n\n"
            )
            failed_tests.extend(data["FailedTest"])

    if failed_tests:
        report += f"Failed Test Details:\n"
        for test in failed_tests:
            report += f"  - {test['name']} ({test['duration']}) Reason: {test['reason']}\n"

    print(report)








