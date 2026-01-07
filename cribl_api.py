import os

import requests


class CriblAPI:
    """
    A client for interacting with the Cribl API.
    """

    def __init__(
        self, base_url="http://localhost:9000", username=None, password=None, token=None
    ):
        """
        Initializes the CriblAPI client.
        Authenticates and retrieves a token if username and password are provided.

        Args:
            base_url (str): The base URL of the Cribl API. Defaults to http://localhost:9000.
            username (str, optional): The username for authentication.
            password (str, optional): The password for authentication.
            token (str, optional): An existing authentication token.
        """
        self.base_url = base_url
        self.headers = {"Content-Type": "application/json"}

        if token:
            self.headers["Authorization"] = f"Bearer {token}"
        elif username and password:
            self.login(username, password)
        else:
            # for on-prem, if you are on the master node, you might not need a token
            pass

    def _post(self, endpoint, payload):
        """
        Performs a POST request to the specified endpoint.
        """
        url = self.base_url + endpoint
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            try:
                return response.json()
            except requests.exceptions.JSONDecodeError as e:
                print(
                    f"Failed to decode JSON from response. Status: {response.status_code}, Body: {response.text}"
                )
                raise e
        except requests.exceptions.RequestException as e:
            print(f"Error connecting to Cribl API at {url}: {e}")
            raise

    def login(self, username, password):
        """
        Logs in to the Cribl API and retrieves an authentication token.
        """
        auth_payload = {"username": username, "password": password}
        response = self._post("/api/v1/auth/login", auth_payload)
        token = response.get("token")
        if not token:
            raise Exception("Authentication failed: token not found in response.")
        self.headers["Authorization"] = f"Bearer {token}"
        print("Successfully authenticated and retrieved token.")

    def _get(self, endpoint):
        """
        Performs a GET request to the specified endpoint.
        """
        url = self.base_url + endpoint
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            try:
                return response.json()
            except requests.exceptions.JSONDecodeError as e:
                print(
                    f"Failed to decode JSON from response. Status: {response.status_code}, Body: {response.text}"
                )
                raise e
        except requests.exceptions.RequestException as e:
            print(f"Error connecting to Cribl API at {url}: {e}")
            raise

    def get_worker_groups(self):
        """
        Retrieves all worker groups.
        Assumes the endpoint is /api/v1/groups.
        """
        return self._get("/api/v1/groups")

    def get_sources(self, group_id):
        """
        Retrieves all sources (inputs) for a given worker group.
        Assumes the endpoint is /api/v1/groups/<group_id>/sources.
        """
        return self._get(f"/api/v1/groups/{group_id}/sources")

    def get_destinations(self, group_id):
        """
        Retrieves all destinations (outputs) for a given worker group.
        Assumes the endpoint is /api/v1/groups/<group_id>/destinations.
        """
        return self._get(f"/api/v1/groups/{group_id}/destinations")

    def get_pipelines(self, group_id):
        """
        Retrieves all pipelines for a given worker group.
        """
        return self._get(f"/api/v1/groups/{group_id}/pipelines")


def get_api_client_from_env():
    """
    Creates a CriblAPI client from environment variables.
    """
    base_url = os.environ.get("CRIBL_BASE_URL", "http://localhost:9000")
    token = os.environ.get("CRIBL_AUTH_TOKEN")
    username = os.environ.get("CRIBL_USERNAME")
    password = os.environ.get("CRIBL_PASSWORD")

    return CriblAPI(base_url, username=username, password=password, token=token)
