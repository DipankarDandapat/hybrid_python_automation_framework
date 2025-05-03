"""
API Client Module.

This module provides a client for making API requests with various HTTP methods.
It supports request customization, response validation, and error handling.
"""
import json
from typing import Optional, Dict, Any, Union
from src.utils import logger
log = logger.customLogger()


class APIClient:
    """API Client for making HTTP requests."""

    def __init__(self, session):
        """
        Initialize API client with session.

        Args:
            session: Request session object
        """
        self.session = session
        self.method_map = {
            'GET': self.get_request,
            'POST': self.post_request,
            'PUT': self.put_request,
            'PATCH': self.patch_request,
            'DELETE': self.delete_request
        }
        log.info("Initialized API client")

    def make_request(self, base_url: str, api_endpoint: str, method: str = 'GET',path_params: Optional[Dict] = None, **kwargs) -> Any:
        """
        Generic method to make API requests based on the specified method.

        Args:
            base_url: Base URL of the API
            api_endpoint: API endpoint (may contain placeholders like {id})
            method: HTTP method (GET, POST, PUT, PATCH, DELETE)
            path_params: Dictionary to replace path placeholders in api_endpoint
            api_endpoint = "/api/v1/todos/{id}"  # Must include {id}
            path_params = {"id": "123"}  # Key must match the placeholder
            **kwargs: Additional arguments to pass to the request method

        Returns:
            Response object

        Raises:
            ValueError: If unsupported HTTP method is provided
            KeyError: If path_params is missing a required placeholder
        """
        method = method.upper()
        if method not in self.method_map:
            raise ValueError(f"Unsupported HTTP method: {method}")

        if path_params:

            try:
                log.info(f"Before replacement: {api_endpoint}, path_params: {path_params}")
                api_endpoint = api_endpoint.format(**path_params)
                log.info(f"After replacement: {api_endpoint}")
            except KeyError as e:
                log.error(f"Missing path parameter: {e}")
                raise
            except Exception as e:
                log.error(f"Error formatting path parameters: {e}")
                raise

        log.info(f"Making {method} request to {base_url}{api_endpoint}")
        return self.method_map[method](base_url, api_endpoint, **kwargs)



    def get_request(self, base_url: str, api_endpoint: str, header: Optional[Dict] = None,
                    query_params: Optional[Dict] = None) -> Any:
        """
        Perform a GET request.

        Args:
            base_url: Base URL of the API
            api_endpoint: API endpoint
            header: Optional headers
            query_params: Optional query parameters

        Returns:
            Response object
        """
        try:
            log.info(f"Request Method: GET")
            url = f"{base_url}{api_endpoint}"
            log.info(f"Constructed URL: {url}")

            if query_params:
                log.info(f"Query Parameters: {query_params}")
            else:
                log.info("No query parameters provided.")

            if header:
                log.info(f"Request Headers: {header}")
            else:
                log.info("No headers provided.")

            response = self.session.get(url, headers=header, params=query_params, timeout=None)
            return response

        except Exception as e:
            log.error(f"An error occurred during the GET request: {str(e)}")
            raise

    def post_request(self, base_url: str, api_endpoint: str, header: Optional[Dict] = None,
                     param: Optional[Dict] = None, payload: Optional[Union[Dict, str]] = None,
                     file: Optional[Dict] = None) -> Any:
        """
        Perform a POST request.

        Args:
            base_url: Base URL of the API
            api_endpoint: API endpoint
            header: Optional headers
            param: Optional query parameters
            payload: Optional request payload
            file: Optional files to upload

        Returns:
            Response object
        """
        url = f"{base_url}{api_endpoint}"
        log.info(f"Request Type: POST")
        log.info(f"Request URL: {url}")

        if header:
            log.info(f"Request Headers: {header}")
        else:
            log.warning("No headers provided.")

        if param:
            log.info(f"Query Parameters: {param}")
        else:
            log.warning("No query parameters provided.")

        if payload:
            log.info(f"Request Payload: {payload}")
        else:
            log.warning("No payload provided.")

        if file:
            log.info("File included in the request.")
        else:
            log.info("No file included in the request.")

        try:
            if file is not None:
                response = self.session.post(url, headers=header, data=payload,
                                             params=param, files=file, timeout=None)
            else:
                response = self.session.post(url, headers=header, data=json.dumps(payload),
                                             params=param, timeout=None)
            return response

        except Exception as e:
            log.error(f"Error occurred during the POST request: {str(e)}")
            raise

    def put_request(self, base_url: str, api_endpoint: str, header: Optional[Dict] = None,
                    payload: Optional[Dict] = None, param: Optional[Dict] = None) -> Any:
        """
        Perform a PUT request.

        Args:
            base_url: Base URL of the API
            api_endpoint: API endpoint
            header: Optional headers
            payload: Optional request payload
            param: Optional query parameters

        Returns:
            Response object
        """
        url = f"{base_url}{api_endpoint}"
        log.info(f"Request Type: PUT")
        log.info(f"Request URL: {url}")

        if header:
            log.info(f"Request Headers: {header}")
        else:
            log.warning("No headers provided.")

        if param:
            log.info(f"Query Parameters: {param}")
        else:
            log.warning("No query parameters provided.")

        if payload:
            log.info(f"Request Payload: {payload}")
        else:
            log.warning("No payload provided.")

        try:
            response = self.session.put(url, headers=header, data=json.dumps(payload),
                                        params=param, timeout=None)
            return response

        except Exception as e:
            log.error(f"Error occurred during the PUT request to {url}: {str(e)}")
            raise

    def patch_request(self, base_url: str, api_endpoint: str, header: Optional[Dict] = None,
                      payload: Optional[Dict] = None) -> Any:
        """
        Perform a PATCH request.

        Args:
            base_url: Base URL of the API
            api_endpoint: API endpoint
            header: Optional headers
            payload: Optional request payload

        Returns:
            Response object
        """
        url = f"{base_url}{api_endpoint}"
        log.info(f"Request Type: PATCH")
        log.info(f"Request URL: {url}")

        if header:
            log.info(f"Request Headers: {header}")
        else:
            log.warning("No headers provided.")

        if payload:
            log.info(f"Request Payload: {payload}")
        else:
            log.warning("No payload provided.")

        try:
            response = self.session.patch(url, headers=header, data=json.dumps(payload), timeout=None)
            return response

        except Exception as e:
            log.error(f"Error occurred during the PATCH request to {url}: {str(e)}")
            raise

    def delete_request(self, base_url: str, api_endpoint: str, header: Optional[Dict] = None,
                       payload: Optional[Dict] = None, query_params: Optional[Dict] = None) -> Any:
        """
        Perform a DELETE request.

        Args:
            base_url: Base URL of the API
            api_endpoint: API endpoint
            header: Optional headers
            payload: Optional request payload
            query_params: Optional query parameters

        Returns:
            Response object
        """
        url = f"{base_url}{api_endpoint}"
        log.info(f"Request Type: DELETE")
        log.info(f"Request URL: {url}")

        if header:
            log.info(f"Request Headers: {header}")
        else:
            log.warning("No headers provided.")

        if payload:
            log.info(f"Request Payload: {payload}")
        else:
            log.warning("No payload provided.")

        if query_params:
            log.info(f"Query Parameters: {query_params}")
        else:
            log.warning("No query parameters provided.")

        try:
            response = self.session.delete(url, headers=header, params=query_params, timeout=None)
            return response

        except Exception as e:
            log.error(f"Error occurred during the DELETE request to {url}: {str(e)}")
            raise
