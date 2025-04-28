# """
# Custom HTML Report Generator Module.
#
# This module provides functionality for generating custom HTML reports.
# It extends the default pytest-html report with additional information and styling.
# """
# import os
# import time
# import datetime
# import pytest
# import pytest_html
# from py.xml import html
# from pathlib import Path
# from src.utils.logger import get_logger
#
# logger = get_logger(__name__)
#
#
# def pytest_html_report_title(report):
#     """Set report title."""
#     report.title = "Automation Testing Framework - Test Report"
#
#
# def pytest_configure(config):
#     """Configure pytest-html report."""
#     # Get environment name
#     environment = os.environ.get("ENVIRONMENT", "staging")
#
#     # Set report variables
#     config._metadata = {
#         "Project": "Automation Testing Framework",
#         "Environment": environment.upper(),
#         "Python Version": config.pluginmanager.getplugin("metadata").metadata["Python"]
#     }
#
#     # Add browser info for UI tests
#     if os.environ.get("BROWSER"):
#         config._metadata["Browser"] = os.environ.get("BROWSER").capitalize()
#         config._metadata["Headless"] = os.environ.get("HEADLESS", "False")
#
#         if os.environ.get("REMOTE", "False").lower() == "true":
#             config._metadata["Execution"] = "Remote (Cloud)"
#             config._metadata["Platform"] = os.environ.get("PLATFORM", "Windows")
#         else:
#             config._metadata["Execution"] = "Local"
#
#
# def pytest_html_results_table_header(cells):
#     """Customize HTML report table header."""
#     cells.insert(2, html.th("Description"))
#     cells.insert(3, html.th("Time", class_="sortable time", col="time"))
#     cells.pop()  # Remove links column
#
#
# def pytest_html_results_table_row(report, cells):
#     """Customize HTML report table row."""
#     cells.insert(2, html.td(getattr(report, "description", "")))
#     cells.insert(3, html.td(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"), class_="col-time"))
#     cells.pop()  # Remove links column
#
#
# @pytest.hookimpl(hookwrapper=True)
# def pytest_runtest_makereport(item, call):
#     """Customize test report."""
#     outcome = yield
#     report = outcome.get_result()
#
#     # Set test description from docstring
#     report.description = str(item.function.__doc__ or "").strip()
#
#     # Add screenshot to report for UI test failures
#     if report.when == "call" and report.failed:
#         if "driver" in item.funcargs:
#             try:
#                 driver = item.funcargs["driver"]
#                 timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
#                 screenshot_dir = Path(__file__).parent / "reports" / "screenshots"
#                 screenshot_dir.mkdir(parents=True, exist_ok=True)
#                 screenshot_path = screenshot_dir / f"failure_{timestamp}_{item.name}.png"
#                 driver.save_screenshot(str(screenshot_path))
#
#                 # Add screenshot to report
#                 if hasattr(report, "extras"):
#                     report.extras.append(pytest_html.extras.image(str(screenshot_path)))
#                     report.extras.append(pytest_html.extras.html(f"<div>Screenshot saved to: {screenshot_path}</div>"))
#
#                 logger.info(f"Screenshot saved to {screenshot_path}")
#             except Exception as e:
#                 logger.error(f"Failed to take screenshot: {str(e)}")
