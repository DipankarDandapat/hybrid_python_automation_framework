class BasePage:
    """Base Page class for all page objects."""

    def __init__(self, driver):
        self.driver = driver
        self.explicit_wait = int(os.getenv('EXPLICIT_WAIT', '20'))
        self.base_url = os.getenv('UI_BASE_URL', 'https://example.com')
        log.info(f"Initialized BasePage with base URL: {self.base_url}")

    def _wait_for_condition(self, locator, condition, timeout=None):
        """
        Wait for a condition on an element.

        Args:
            locator (tuple): Locator tuple (By, value)
            condition (callable): Expected condition function
            timeout (int, optional): Timeout in seconds

        Returns:
            WebElement: Found element
        """
        timeout = timeout or self.explicit_wait
        try:
            log.debug(f"Waiting for {condition.__name__} with locator: {locator} for {timeout}s")
            element = WebDriverWait(self.driver, timeout).until(
                condition(locator)
            )
            log.info(f"Condition {condition.__name__} met for locator: {locator}")
            return element
        except TimeoutException:
            log.error(f"TimeoutException: {condition.__name__} not met for locator: {locator} in {timeout}s")
            raise

    def open(self, url_path=""):
        full_url = f"{self.base_url}/{url_path.lstrip('/')}"
        log.info(f"Opening URL: {full_url}")
        try:
            self.driver.get(full_url)
            log.info(f"Opened URL successfully: {full_url}")
        except Exception as e:
            log.error(f"Failed to open URL {full_url}: {str(e)}")
            raise
        return self

    def find_element(self, locator, timeout=None):
        log.info(f"Finding element: {locator}")
        return self._wait_for_condition(locator, EC.presence_of_element_located, timeout)

    def find_elements(self, locator, timeout=None):
        log.info(f"Finding elements: {locator}")
        return self._wait_for_condition(locator, EC.presence_of_all_elements_located, timeout)

    def click(self, locator, timeout=None):
        log.info(f"Clicking on element: {locator}")
        try:
            element = self._wait_for_condition(locator, EC.element_to_be_clickable, timeout)
            element.click()
            log.info(f"Clicked element: {locator}")
        except Exception as e:
            log.error(f"Failed to click element {locator}: {str(e)}")
            raise
        return self

    def input_text(self, locator, text, clear=True, timeout=None):
        log.info(f"Inputting text into element: {locator}")
        try:
            element = self._wait_for_condition(locator, EC.visibility_of_element_located, timeout)
            if clear:
                element.clear()
                log.debug(f"Cleared existing text in element: {locator}")
            element.send_keys(text)
            log.info(f"Entered text '{text}' into element: {locator}")
        except Exception as e:
            log.error(f"Failed to input text into element {locator}: {str(e)}")
            raise
        return self

    def get_text(self, locator, timeout=None):
        log.info(f"Getting text from element: {locator}")
        try:
            element = self._wait_for_condition(locator, EC.visibility_of_element_located, timeout)
            text = element.text
            log.info(f"Got text '{text}' from element: {locator}")
            return text
        except Exception as e:
            log.error(f"Failed to get text from element {locator}: {str(e)}")
            raise

    def is_element_present(self, locator, timeout=5):
        log.info(f"Checking if element is present: {locator}")
        try:
            self._wait_for_condition(locator, EC.presence_of_element_located, timeout)
            log.info(f"Element is present: {locator}")
            return True
        except TimeoutException:
            log.warning(f"Element not present: {locator}")
            return False

    def is_element_visible(self, locator, timeout=5):
        log.info(f"Checking if element is visible: {locator}")
        try:
            self._wait_for_condition(locator, EC.visibility_of_element_located, timeout)
            log.info(f"Element is visible: {locator}")
            return True
        except TimeoutException:
            log.warning(f"Element not visible: {locator}")
            return False

    def wait_for_element(self, locator, timeout=None, condition=EC.presence_of_element_located):
        log.info(f"Waiting for element with custom condition: {condition.__name__} for locator {locator}")
        return self._wait_for_condition(locator, condition, timeout)

    def dropdown_select_element(self, locator, selector, selector_type="value", timeout=10):
        """Select a value/index/text from a dropdown."""
        try:
            element = self._wait_for_condition(locator, EC.element_to_be_clickable, timeout)
            sel = Select(element)
            if selector_type == "value":
                sel.select_by_value(selector)
            elif selector_type == "index":
                sel.select_by_index(selector)
            elif selector_type == "text":
                sel.select_by_visible_text(selector)
            else:
                raise ValueError(f"Invalid selector_type: {selector_type}")
            log.info(f"Selected '{selector}' using selector type '{selector_type}'")
        except Exception as e:
            log.error(f"Failed to select '{selector}' using selector type '{selector_type}': {str(e)}")

    def get_dropdown_options_count(self, locator, timeout=10):
        """Return the number of options in a dropdown."""
        try:
            element = self._wait_for_condition(locator, EC.presence_of_element_located, timeout)
            sel = Select(element)
            options = sel.options
            log.info(f"Found {len(options)} options in dropdown")
            return len(options)
        except Exception as e:
            log.error(f"Failed to get dropdown options: {str(e)}")
            return 0

    def get_dropdown_selected_option_text(self, locator, timeout=10):
        """Return the text of the selected option."""
        try:
            element = self._wait_for_condition(locator, EC.presence_of_element_located, timeout)
            sel = Select(element)
            selected_text = sel.first_selected_option.text
            log.info(f"Selected dropdown option text: '{selected_text}'")
            return selected_text
        except Exception as e:
            log.error(f"Failed to get selected dropdown text: {str(e)}")
            return None

    def get_dropdown_selected_option_value(self, locator, timeout=10):
        """Return the value of the selected option."""
        try:
            element = self._wait_for_condition(locator, EC.presence_of_element_located, timeout)
            sel = Select(element)
            selected_value = sel.first_selected_option.get_attribute("value")
            log.info(f"Selected dropdown option value: '{selected_value}'")
            return selected_value
        except Exception as e:
            log.error(f"Failed to get selected dropdown value: {str(e)}")
            return None

    def is_element_selected(self, locator, timeout=10):
        """Check if an element is selected."""
        try:
            element = self._wait_for_condition(locator, EC.presence_of_element_located, timeout)
            selected = element.is_selected()
            log.info(f"Element selected status: {selected}")
            return selected
        except Exception as e:
            log.error(f"Failed to check element selected status: {str(e)}")
            return False

    def element_hover(self, locator, timeout=10):
        """Hover over an element."""
        try:
            element = self._wait_for_condition(locator, EC.presence_of_element_located, timeout)
            ActionChains(self.driver).move_to_element(element).perform()
            time.sleep(1)
            log.info(f"Hovered over element")
        except Exception as e:
            log.error(f"Failed to hover over element: {str(e)}")

    def web_scroll(self, direction="up"):
        """Scroll the web page up or down."""
        try:
            if direction == "up":
                self.driver.execute_script("window.scrollBy(0, -1000);")
                log.info("Scrolled up the page")
            elif direction == "down":
                self.driver.execute_script("window.scrollBy(0, 1000);")
                log.info("Scrolled down the page")
            else:
                log.warning(f"Invalid scroll direction '{direction}'")
        except Exception as e:
            log.error(f"Failed to scroll the page: {str(e)}")

    def get_title(self):
        """Return the page title."""
        try:
            title = self.driver.title
            log.info(f"Page title: '{title}'")
            return title
        except Exception as e:
            log.error(f"Failed to get page title: {str(e)}")
            return None

    def get_url(self):
        """Return the current URL."""
        try:
            url = self.driver.current_url
            log.info(f"Current URL: '{url}'")
            return url
        except Exception as e:
            log.error(f"Failed to get current URL: {str(e)}")
            return None

    def page_back(self):
        """Go back to the previous page."""
        try:
            self.driver.execute_script("window.history.go(-1)")
            log.info("Navigated back to previous page")
        except Exception as e:
            log.error(f"Failed to navigate back: {str(e)}")

    def refresh(self):
        """Refresh the current page."""
        try:
            self.driver.get(self.driver.current_url)
            log.info("Refreshed the page")
        except Exception as e:
            log.error(f"Failed to refresh page: {str(e)}")

    def get_attribute_value(self, locator, attribute, timeout=10):
        """Get the value of an attribute of an element."""
        try:
            element = self._wait_for_condition(locator, EC.presence_of_element_located, timeout)
            value = element.get_attribute(attribute)
            log.info(f"Attribute '{attribute}' value: '{value}'")
            return value
        except Exception as e:
            log.error(f"Failed to get attribute '{attribute}': {str(e)}")
            return None

    def find_all_elements_click_based_on_text(self, locator, text_to_match, timeout=None):
        """
        Find all elements matching the locator, click the element whose text matches the given text.
        :param locator: Tuple(By.<method>, "locator")
        :param text_to_match: Text to match and click
        :param timeout: Max time to wait for elements
        """
        try:
            log.info(f"Finding all elements with locator: {locator}")
            elements = self.find_elements(locator, timeout)

            log.info(f"Total elements found: {len(elements)}")
            for element in elements:
                print("#################################")
                print(element)
                element_text = element.text
                if len(element_text) == 0:
                    element_text = element.get_attribute("innerText")
                if len(element_text) != 0:
                    log.info("Getting text on element The text is :: '" + element_text + "'")
                    text = element_text.strip()
                log.info(f"Checking element text: '{element_text}'")
                if element_text == text_to_match:
                    log.info(f"Match found. Clicking element with text: '{element_text}'")
                    element.click()
                    break
            else:
                log.warning(f"No element with matching text '{text_to_match}' found.")
        except Exception as e:
            log.error(
                f"Error occurred while finding/clicking element based on text: {text_to_match}. Exception: {str(e)}")

    def scroll_to_element(self, locator, direction="down", timeout=None):
        """
        Scroll to a specific element based on direction.
        :param locator: Tuple(By.<method>, "locator")
        :param direction: 'up', 'down', 'left', 'right'
        :param timeout: Max time to wait for element
        """
        try:
            log.info(f"Waiting for element to be present with locator: {locator}")
            element = self._wait_for_condition(locator, EC.presence_of_element_located, timeout)

            if direction.lower() == "down" or direction.lower() == "right":
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'start', inline: 'start', behavior: 'smooth'});", element)
                log.info(f"Scrolled {direction} to element with locator: {locator}")
            elif direction.lower() == "up" or direction.lower() == "left":
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'end', inline: 'end', behavior: 'smooth'});", element)
                log.info(f"Scrolled {direction} to element with locator: {locator}")
            else:
                log.warning(f"Invalid scroll direction '{direction}' provided. No action taken.")

        except Exception as e:
            log.error(f"Failed to scroll to element with locator: {locator}. Exception: {str(e)}")

    def scroll_to_element_automatic(self, locator, timeout=None):
        """
        Scroll automatically to a specific element based on its position on the page.
        :param locator: Tuple(By.<method>, "locator")
        :param timeout: Max time to wait for element
        """
        try:
            log.info(f"Waiting for element to be present with locator: {locator}")
            element = self._wait_for_condition(locator, EC.presence_of_element_located, timeout)

            element_location = element.location
            element_y = element_location['y']
            element_x = element_location['x']

            current_scroll_y = self.driver.execute_script("return window.pageYOffset;")
            current_scroll_x = self.driver.execute_script("return window.pageXOffset;")

            log.info(f"Element location (X: {element_x}, Y: {element_y})")
            log.info(f"Current scroll position (X: {current_scroll_x}, Y: {current_scroll_y})")

            # Decide vertical scroll
            if element_y > current_scroll_y:
                log.info("Scrolling down to the element")
            elif element_y < current_scroll_y:
                log.info("Scrolling up to the element")

            # Decide horizontal scroll
            if element_x > current_scroll_x:
                log.info("Scrolling right to the element")
            elif element_x < current_scroll_x:
                log.info("Scrolling left to the element")

            # Final scroll into view
            self.driver.execute_script(
                "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center', inline: 'center'});", element)
            log.info(f"Successfully scrolled to element with locator: {locator}")

        except Exception as e:
            log.error(f"Failed to scroll to element with locator: {locator}. Exception: {str(e)}")

    # New ActionChains methods

    def drag_and_drop(self, source_locator, target_locator, timeout=None):
        """
        Drag an element and drop it onto another element.
        :param source_locator: Tuple(By.<method>, "locator") for the source element
        :param target_locator: Tuple(By.<method>, "locator") for the target element
        :param timeout: Max time to wait for elements
        """
        try:
            log.info(f"Attempting drag and drop from {source_locator} to {target_locator}")
            source_element = self._wait_for_condition(source_locator, EC.visibility_of_element_located, timeout)
            target_element = self._wait_for_condition(target_locator, EC.visibility_of_element_located, timeout)

            action_chains = ActionChains(self.driver)
            action_chains.drag_and_drop(source_element, target_element).perform()
            log.info(f"Successfully dragged element from {source_locator} to {target_locator}")
        except Exception as e:
            log.error(f"Failed to perform drag and drop: {str(e)}")
            raise

    def drag_and_drop_by_offset(self, source_locator, x_offset, y_offset, timeout=None):
        """
        Drag an element and drop it at a specific offset.
        :param source_locator: Tuple(By.<method>, "locator") for the source element
        :param x_offset: X coordinate offset to move to
        :param y_offset: Y coordinate offset to move to
        :param timeout: Max time to wait for element
        """
        try:
            log.info(f"Attempting drag and drop from {source_locator} by offset ({x_offset}, {y_offset})")
            source_element = self._wait_for_condition(source_locator, EC.visibility_of_element_located, timeout)

            action_chains = ActionChains(self.driver)
            action_chains.drag_and_drop_by_offset(source_element, x_offset, y_offset).perform()
            log.info(f"Successfully dragged element from {source_locator} by offset ({x_offset}, {y_offset})")
        except Exception as e:
            log.error(f"Failed to perform drag and drop by offset: {str(e)}")
            raise

    def double_click(self, locator, timeout=None):
        """
        Double click on an element.
        :param locator: Tuple(By.<method>, "locator")
        :param timeout: Max time to wait for element
        """
        try:
            log.info(f"Double-clicking on element: {locator}")
            element = self._wait_for_condition(locator, EC.element_to_be_clickable, timeout)

            action_chains = ActionChains(self.driver)
            action_chains.double_click(element).perform()
            log.info(f"Successfully double-clicked on element: {locator}")
        except Exception as e:
            log.error(f"Failed to double-click on element: {str(e)}")
            raise

    def right_click(self, locator, timeout=None):
        """
        Right click (context click) on an element.
        :param locator: Tuple(By.<method>, "locator")
        :param timeout: Max time to wait for element
        """
        try:
            log.info(f"Right-clicking on element: {locator}")
            element = self._wait_for_condition(locator, EC.element_to_be_clickable, timeout)

            action_chains = ActionChains(self.driver)
            action_chains.context_click(element).perform()
            log.info(f"Successfully right-clicked on element: {locator}")
        except Exception as e:
            log.error(f"Failed to right-click on element: {str(e)}")
            raise

    def click_and_hold(self, locator, timeout=None):
        """
        Click and hold on an element.
        :param locator: Tuple(By.<method>, "locator")
        :param timeout: Max time to wait for element
        """
        try:
            log.info(f"Clicking and holding on element: {locator}")
            element = self._wait_for_condition(locator, EC.element_to_be_clickable, timeout)

            action_chains = ActionChains(self.driver)
            action_chains.click_and_hold(element).perform()
            log.info(f"Successfully clicked and held on element: {locator}")
        except Exception as e:
            log.error(f"Failed to click and hold on element: {str(e)}")
            raise

    def release(self):
        """
        Release a held mouse button.
        """
        try:
            log.info("Releasing held mouse button")
            action_chains = ActionChains(self.driver)
            action_chains.release().perform()
            log.info("Successfully released held mouse button")
        except Exception as e:
            log.error(f"Failed to release mouse button: {str(e)}")
            raise

    def key_down(self, key, locator=None, timeout=None):
        """
        Press and hold a key, with optional element focus.
        :param key: Key to press (e.g., Keys.SHIFT)
        :param locator: Optional Tuple(By.<method>, "locator")
        :param timeout: Max time to wait for element
        """
        try:
            action_chains = ActionChains(self.driver)

            if locator:
                log.info(f"Pressing key {key} down on element: {locator}")
                element = self._wait_for_condition(locator, EC.visibility_of_element_located, timeout)
                action_chains.key_down(key, element).perform()
                log.info(f"Successfully pressed key {key} down on element: {locator}")
            else:
                log.info(f"Pressing key {key} down")
                action_chains.key_down(key).perform()
                log.info(f"Successfully pressed key {key} down")
        except Exception as e:
            log.error(f"Failed to press key down: {str(e)}")
            raise

    def key_up(self, key, locator=None, timeout=None):
        """
        Release a held key, with optional element focus.
        :param key: Key to release (e.g., Keys.SHIFT)
        :param locator: Optional Tuple(By.<method>, "locator")
        :param timeout: Max time to wait for element
        """
        try:
            action_chains = ActionChains(self.driver)

            if locator:
                log.info(f"Releasing key {key} on element: {locator}")
                element = self._wait_for_condition(locator, EC.visibility_of_element_located, timeout)
                action_chains.key_up(key, element).perform()
                log.info(f"Successfully released key {key} on element: {locator}")
            else:
                log.info(f"Releasing key {key}")
                action_chains.key_up(key).perform()
                log.info(f"Successfully released key {key}")
        except Exception as e:
            log.error(f"Failed to release key: {str(e)}")
            raise

    def send_keys_to_element(self, locator, *keys, timeout=None):
        """
        Send keys to an element using ActionChains.
        :param locator: Tuple(By.<method>, "locator")
        :param keys: Keys to send
        :param timeout: Max time to wait for element
        """
        try:
            log.info(f"Sending keys to element: {locator}")
            element = self._wait_for_condition(locator, EC.visibility_of_element_located, timeout)

            action_chains = ActionChains(self.driver)
            action_chains.send_keys_to_element(element, *keys).perform()
            log.info(f"Successfully sent keys to element: {locator}")
        except Exception as e:
            log.error(f"Failed to send keys to element: {str(e)}")
            raise

    def move_by_offset(self, x_offset, y_offset):
        """
        Move the mouse pointer by a given offset.
        :param x_offset: X coordinate offset to move to
        :param y_offset: Y coordinate offset to move to
        """
        try:
            log.info(f"Moving mouse by offset ({x_offset}, {y_offset})")
            action_chains = ActionChains(self.driver)
            action_chains.move_by_offset(x_offset, y_offset).perform()
            log.info(f"Successfully moved mouse by offset ({x_offset}, {y_offset})")
        except Exception as e:
            log.error(f"Failed to move mouse by offset: {str(e)}")
            raise

    def move_to_element_with_offset(self, locator, x_offset, y_offset, timeout=None):
        """
        Move to an element with a specific offset from its top-left corner.
        :param locator: Tuple(By.<method>, "locator")
        :param x_offset: X coordinate offset from element's left
        :param y_offset: Y coordinate offset from element's top
        :param timeout: Max time to wait for element
        """
        try:
            log.info(f"Moving to element {locator} with offset ({x_offset}, {y_offset})")
            element = self._wait_for_condition(locator, EC.visibility_of_element_located, timeout)

            action_chains = ActionChains(self.driver)
            action_chains.move_to_element_with_offset(element, x_offset, y_offset).perform()
            log.info(f"Successfully moved to element {locator} with offset ({x_offset}, {y_offset})")
        except Exception as e:
            log.error(f"Failed to move to element with offset: {str(e)}")
            raise

    def perform_actions(self, actions_func):
        """
        Perform a custom sequence of actions using ActionChains.
        :param actions_func: Function that accepts an ActionChains object and adds actions to it
        """
        try:
            log.info("Performing custom action sequence")
            action_chains = ActionChains(self.driver)
            actions_func(action_chains)
            action_chains.perform()
            log.info("Successfully performed custom action sequence")
        except Exception as e:
            log.error(f"Failed to perform custom action sequence: {str(e)}")
            raise

    # Alert handling methods

    def wait_for_alert(self, timeout=10):
        """
        Wait for an alert to be present and return it.
        :param timeout: Max time to wait for alert
        :return: Alert object
        """
        try:
            log.info(f"Waiting for alert to be present for {timeout} seconds")
            alert = WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
            log.info("Alert is present")
            return alert
        except TimeoutException:
            log.error(f"No alert appeared within {timeout} seconds")
            raise

    def accept_alert(self, timeout=10):
        """
        Accept (click OK) on an alert.
        :param timeout: Max time to wait for alert
        """
        try:
            log.info("Accepting alert")
            alert = self.wait_for_alert(timeout)
            alert.accept()
            log.info("Alert accepted successfully")
        except Exception as e:
            log.error(f"Failed to accept alert: {str(e)}")
            raise

    def dismiss_alert(self, timeout=10):
        """
        Dismiss (click Cancel) on an alert.
        :param timeout: Max time to wait for alert
        """
        try:
            log.info("Dismissing alert")
            alert = self.wait_for_alert(timeout)
            alert.dismiss()
            log.info("Alert dismissed successfully")
        except Exception as e:
            log.error(f"Failed to dismiss alert: {str(e)}")
            raise

    def get_alert_text(self, timeout=10):
        """
        Get the text from an alert.
        :param timeout: Max time to wait for alert
        :return: Alert text
        """
        try:
            log.info("Getting alert text")
            alert = self.wait_for_alert(timeout)
            text = alert.text
            log.info(f"Alert text: '{text}'")
            return text
        except Exception as e:
            log.error(f"Failed to get alert text: {str(e)}")
            raise

    def send_text_to_alert(self, text, timeout=10):
        """
        Send text to an alert prompt.
        :param text: Text to send
        :param timeout: Max time to wait for alert
        """
        try:
            log.info(f"Sending text '{text}' to alert")
            alert = self.wait_for_alert(timeout)
            alert.send_keys(text)
            log.info(f"Successfully sent text to alert")
        except Exception as e:
            log.error(f"Failed to send text to alert: {str(e)}")
            raise

    # Frame switching methods

    def switch_to_frame_by_index(self, index, timeout=10):
        """
        Switch to a frame by its index.
        :param index: Index of the frame
        :param timeout: Max time to wait
        """
        try:
            log.info(f"Switching to frame by index: {index}")
            WebDriverWait(self.driver, timeout).until(
                EC.frame_to_be_available_and_switch_to_it(index)
            )
            log.info(f"Successfully switched to frame with index: {index}")
        except Exception as e:
            log.error(f"Failed to switch to frame with index {index}: {str(e)}")
            raise
        return self

    def switch_to_frame_by_name_or_id(self, name_or_id, timeout=10):
        """
        Switch to a frame by its name or ID.
        :param name_or_id: Name or ID of the frame
        :param timeout: Max time to wait
        """
        try:
            log.info(f"Switching to frame by name/id: {name_or_id}")
            WebDriverWait(self.driver, timeout).until(
                EC.frame_to_be_available_and_switch_to_it(name_or_id)
            )
            log.info(f"Successfully switched to frame with name/id: {name_or_id}")
        except Exception as e:
            log.error(f"Failed to switch to frame with name/id {name_or_id}: {str(e)}")
            raise
        return self

    def switch_to_frame_by_locator(self, locator, timeout=10):
        """
        Switch to a frame using a locator.
        :param locator: Tuple(By.<method>, "locator")
        :param timeout: Max time to wait
        """
        try:
            log.info(f"Switching to frame by locator: {locator}")
            WebDriverWait(self.driver, timeout).until(
                EC.frame_to_be_available_and_switch_to_it(locator)
            )
            log.info(f"Successfully switched to frame with locator: {locator}")
        except Exception as e:
            log.error(f"Failed to switch to frame with locator {locator}: {str(e)}")
            raise
        return self

    def switch_to_frame_by_element(self, element):
        """
        Switch to a frame using a WebElement.
        :param element: WebElement representing the frame
        """
        try:
            log.info("Switching to frame by WebElement")
            self.driver.switch_to.frame(element)
            log.info("Successfully switched to frame by WebElement")
        except Exception as e:
            log.error(f"Failed to switch to frame by WebElement: {str(e)}")
            raise
        return self

    def switch_to_default_content(self):
        """
        Switch back to the default content (out of any frame).
        """
        try:
            log.info("Switching to default content")
            self.driver.switch_to.default_content()
            log.info("Successfully switched to default content")
        except Exception as e:
            log.error(f"Failed to switch to default content: {str(e)}")
            raise
        return self

    def switch_to_parent_frame(self):
        """
        Switch to the parent frame.
        """
        try:
            log.info("Switching to parent frame")
            self.driver.switch_to.parent_frame()
            log.info("Successfully switched to parent frame")
        except Exception as e:
            log.error(f"Failed to switch to parent frame: {str(e)}")
            raise
        return self

    # Window handling methods

    def get_window_handles(self):
        """
        Get handles of all open windows/tabs.
        :return: List of window handles
        """
        try:
            handles = self.driver.window_handles
            log.info(f"Got {len(handles)} window handles")
            return handles
        except Exception as e:
            log.error(f"Failed to get window handles: {str(e)}")
            raise

    def get_current_window_handle(self):
        """
        Get the handle of the current window.
        :return: Current window handle
        """
        try:
            handle = self.driver.current_window_handle
            log.info(f"Current window handle: {handle}")
            return handle
        except Exception as e:
            log.error(f"Failed to get current window handle: {str(e)}")
            raise

    def switch_to_window_by_handle(self, handle):
        """
        Switch to a window by its handle.
        :param handle: Window handle to switch to
        """
        try:
            log.info(f"Switching to window with handle: {handle}")
            self.driver.switch_to.window(handle)
            log.info(f"Successfully switched to window with handle: {handle}")
        except Exception as e:
            log.error(f"Failed to switch to window with handle {handle}: {str(e)}")
            raise
        return self

    def switch_to_window_by_index(self, index):
        """
        Switch to a window by its index.
        :param index: Index of the window (0-based)
        """
        try:
            handles = self.get_window_handles()
            if 0 <= index < len(handles):
                log.info(f"Switching to window with index: {index}")
                self.driver.switch_to.window(handles[index])
                log.info(f"Successfully switched to window with index: {index}")
            else:
                log.error(f"Invalid window index: {index}, total windows: {len(handles)}")
                raise IndexError(f"Invalid window index: {index}, total windows: {len(handles)}")
        except Exception as e:
            log.error(f"Failed to switch to window with index {index}: {str(e)}")
            raise
        return self

    def switch_to_window_by_title(self, title, partial_match=False, timeout=10):
        """
        Switch to a window by its title.
        :param title: Title of the window
        :param partial_match: If True, match partial title
        :param timeout: Max time to wait for window
        """
        try:
            log.info(f"Attempting to switch to window with title: '{title}'")
            start_time = time.time()
            while time.time() - start_time < timeout:
                current_handle = self.get_current_window_handle()
                for handle in self.get_window_handles():
                    self.switch_to_window_by_handle(handle)
                    current_title = self.get_title()

                    if (partial_match and title in current_title) or (not partial_match and title == current_title):
                        log.info(f"Successfully switched to window with title: '{current_title}'")
                        return self

                # If not found, switch back to original window and wait a bit
                self.switch_to_window_by_handle(current_handle)
                time.sleep(0.5)

            log.error(f"Failed to find window with title '{title}' within {timeout} seconds")
            raise TimeoutException(f"Failed to find window with title '{title}' within {timeout} seconds")
        except Exception as e:
            log.error(f"Error while switching to window by title '{title}': {str(e)}")
            raise

    def switch_to_window_by_url(self, url, partial_match=False, timeout=10):
        """
        Switch to a window by its URL.
        :param url: URL of the window
        :param partial_match: If True, match partial URL
        :param timeout: Max time to wait for window
        """
        try:
            log.info(f"Attempting to switch to window with URL: '{url}'")
            start_time = time.time()
            while time.time() - start_time < timeout:
                current_handle = self.get_current_window_handle()
                for handle in self.get_window_handles():
                    self.switch_to_window_by_handle(handle)
                    current_url = self.get_url()

                    if (partial_match and url in current_url) or (not partial_match and url == current_url):
                        log.info(f"Successfully switched to window with URL: '{current_url}'")
                        return self

                # If not found, switch back to original window and wait a bit
                self.switch_to_window_by_handle(current_handle)
                time.sleep(0.5)

            log.error(f"Failed to find window with URL '{url}' within {timeout} seconds")
            raise TimeoutException(f"Failed to find window with URL '{url}' within {timeout} seconds")
        except Exception as e:
            log.error(f"Error while switching to window by URL '{url}': {str(e)}")
            raise

    def switch_to_new_window(self, action_func, timeout=10):
        """
        Perform an action that opens a new window and switch to it.
        :param action_func: Function that will trigger opening a new window
        :param timeout: Max time to wait for new window
        """
        try:
            log.info("Setting up to detect new window")
            original_handles = set(self.get_window_handles())
            original_handle = self.get_current_window_handle()

            log.info("Executing action to open new window")
            action_func()

            log.info("Waiting for new window to appear")
            start_time = time.time()
            new_handle = None

            while time.time() - start_time < timeout:
                current_handles = set(self.get_window_handles())
                new_handles = current_handles - original_handles

                if new_handles:
                    new_handle = list(new_handles)[0]
                    log.info(f"New window detected with handle: {new_handle}")
                    break

                time.sleep(0.5)

            if new_handle:
                log.info(f"Switching to new window with handle: {new_handle}")
                self.driver.switch_to.window(new_handle)
                log.info("Successfully switched to new window")
                return self
            else:
                log.error(f"No new window appeared within {timeout} seconds")
                raise TimeoutException(f"No new window appeared within {timeout} seconds")
        except Exception as e:
            log.error(f"Error while switching to new window: {str(e)}")
            raise

    def close_current_window_and_switch_to(self, window_handle=None):
        """
        Close the current window and switch to a specified window or the first available one.
        :param window_handle: Handle of the window to switch to (optional)
        """
        try:
            log.info("Closing current window")
            self.driver.close()

            remaining_handles = self.get_window_handles()
            if not remaining_handles:
                log.warning("No windows remain open after closing current window")
                return self

            if window_handle and window_handle in remaining_handles:
                log.info(f"Switching to specified window handle: {window_handle}")
                self.driver.switch_to.window(window_handle)
            else:
                log.info(f"Switching to first available window handle: {remaining_handles[0]}")
                self.driver.switch_to.window(remaining_handles[0])

            log.info(f"Successfully switched to window with title: '{self.get_title()}'")
        except Exception as e:
            log.error(f"Error while closing current window and switching: {str(e)}")
            raise
        return self

    def wait_for_window_count(self, count, timeout=10):
        """
        Wait until the number of open windows/tabs matches the expected count.
        :param count: Expected number of windows
        :param timeout: Max time to wait
        :return: True if condition is met, False otherwise
        """
        try:
            log.info(f"Waiting for window count to be {count}")
            start_time = time.time()

            while time.time() - start_time < timeout:
                current_count = len(self.get_window_handles())
                if current_count == count:
                    log.info(f"Window count is now {count} as expected")
                    return True
                time.sleep(0.5)

            log.warning(f"Window count did not reach {count} within {timeout} seconds")
            return False
        except Exception as e:
            log.error(f"Error while waiting for window count: {str(e)}")
            return False

    def execute_script(self, script, *args):
        """
        Execute JavaScript in the current window/frame.
        :param script: JavaScript to execute
        :param args: Arguments to pass to the script
        :return: Result of the script execution
        """
        try:
            log.info(f"Executing JavaScript script")
            result = self.driver.execute_script(script, *args)
            log.info("JavaScript execution completed")
            return result
        except Exception as e:
            log.error(f"Failed to execute JavaScript: {str(e)}")
            raise

    def execute_async_script(self, script, *args):
        """
        Execute asynchronous JavaScript in the current window/frame.
        :param script: Asynchronous JavaScript to execute
        :param args: Arguments to pass to the script
        :return: Result of the script execution
        """
        try:
            log.info(f"Executing asynchronous JavaScript script")
            result = self.driver.execute_async_script(script, *args)
            log.info("Asynchronous JavaScript execution completed")
            return result
        except Exception as e:
            log.error(f"Failed to execute asynchronous JavaScript: {str(e)}")
            raise

    def take_screenshot(self, file_path):
        """
        Take a screenshot of the current page.
        :param file_path: Path to save the screenshot
        :return: True if successful, False otherwise
        """
        try:
            log.info(f"Taking screenshot and saving to {file_path}")
            self.driver.save_screenshot(file_path)
            log.info(f"Screenshot saved successfully to {file_path}")
            return True
        except Exception as e:
            log.error(f"Failed to take screenshot: {str(e)}")
            return False