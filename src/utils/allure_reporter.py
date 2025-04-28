"""
Allure Report Configuration Module.

This module provides functionality for generating Allure reports.
It includes custom steps, attachments, and environment information.
"""
import os
import json
import allure
from datetime import datetime
from pathlib import Path
from src.utils.logger import get_logger

logger = get_logger(__name__)


def setup_allure_environment():
    """
    Set up Allure environment properties.
    
    This function creates environment.properties file for Allure reporting.
    """
    logger.info("Setting up Allure environment properties")
    
    # Get environment variables
    environment = os.environ.get("ENVIRONMENT", "staging")
    browser = os.environ.get("BROWSER", "chrome")
    headless = os.environ.get("HEADLESS", "False")
    remote = os.environ.get("REMOTE", "False")
    platform = os.environ.get("PLATFORM", "Windows")
    
    # Create environment properties
    env_properties = {
        "Environment": environment.upper(),
        "Browser": browser.capitalize(),
        "Headless": headless,
        "Remote Execution": remote,
        "Platform": platform,
        "Python Version": os.environ.get("PYTHON_VERSION", "3.10"),
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Create allure-results directory if not exists
    allure_results_dir = Path(__file__).parent.parent.parent / "reports" / "allure-results"
    allure_results_dir.mkdir(parents=True, exist_ok=True)
    
    # Write environment.properties file
    env_file = allure_results_dir / "environment.properties"
    with open(env_file, "w") as f:
        for key, value in env_properties.items():
            f.write(f"{key}={value}\n")
    
    logger.info(f"Allure environment properties saved to {env_file}")


def allure_step(step_name):
    """
    Decorator for Allure step.
    
    Args:
        step_name (str): Step name
        
    Returns:
        function: Decorated function
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            with allure.step(step_name):
                return func(*args, **kwargs)
        return wrapper
    return decorator


def attach_screenshot(driver, name="Screenshot"):
    """
    Attach screenshot to Allure report.
    
    Args:
        driver: WebDriver instance
        name (str, optional): Screenshot name. Defaults to "Screenshot".
    """
    try:
        allure.attach(
            driver.get_screenshot_as_png(),
            name=name,
            attachment_type=allure.attachment_type.PNG
        )
        logger.info(f"Screenshot '{name}' attached to Allure report")
    except Exception as e:
        logger.error(f"Failed to attach screenshot to Allure report: {str(e)}")


def attach_html(html_content, name="HTML Content"):
    """
    Attach HTML content to Allure report.
    
    Args:
        html_content (str): HTML content
        name (str, optional): Attachment name. Defaults to "HTML Content".
    """
    try:
        allure.attach(
            html_content,
            name=name,
            attachment_type=allure.attachment_type.HTML
        )
        logger.info(f"HTML content '{name}' attached to Allure report")
    except Exception as e:
        logger.error(f"Failed to attach HTML content to Allure report: {str(e)}")


def attach_json(json_data, name="JSON Data"):
    """
    Attach JSON testData to Allure report.
    
    Args:
        json_data (dict): JSON testData
        name (str, optional): Attachment name. Defaults to "JSON Data".
    """
    try:
        allure.attach(
            json.dumps(json_data, indent=2),
            name=name,
            attachment_type=allure.attachment_type.JSON
        )
        logger.info(f"JSON testData '{name}' attached to Allure report")
    except Exception as e:
        logger.error(f"Failed to attach JSON testData to Allure report: {str(e)}")


def attach_text(text, name="Text Content"):
    """
    Attach text content to Allure report.
    
    Args:
        text (str): Text content
        name (str, optional): Attachment name. Defaults to "Text Content".
    """
    try:
        allure.attach(
            text,
            name=name,
            attachment_type=allure.attachment_type.TEXT
        )
        logger.info(f"Text content '{name}' attached to Allure report")
    except Exception as e:
        logger.error(f"Failed to attach text content to Allure report: {str(e)}")
