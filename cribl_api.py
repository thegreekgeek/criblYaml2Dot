import os
import requests

from requests import Session


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
        self.session = Session()
        self.session.headers.update({"Content-Type": "application/json"})

        if token:
            if token.startswith("Bearer "):
                self.session.headers["Authorization"] = token
            else:
                self.session.headers["Authorization"] = f"Bearer {token}"
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
            response = self.session.post(url, json=payload)
            response.raise_for_status()
            try:
                return response.json()
            except requests.exceptions.JSONDecodeError as e:
                print(
                    f"Failed to decode JSON from response. Status: {response.status_code}, Body: {response.text}"
                )
                raise e
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                print(
                    f"Authentication failed for {url}. Please check your credentials "
                    "(CRIBL_USERNAME, CRIBL_PASSWORD) or auth token (CRIBL_AUTH_TOKEN)."
                )
            print(f"HTTP error connecting to Cribl API at {url}: {e}")
            raise
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
        if token and not token.startswith("Bearer "):
            token = f"Bearer {token}"
        self.session.headers["Authorization"] = token
        print("Successfully authenticated and retrieved token.")

    def _get(self, endpoint):
        """
        Performs a GET request to the specified endpoint.
        """
        url = self.base_url + endpoint
        try:
            response = self.session.get(url)
            response.raise_for_status()
            try:
                return response.json()
            except requests.exceptions.JSONDecodeError as e:
                print(
                    f"Failed to decode JSON from response. Status: {response.status_code}, Body: {response.text}"
                )
                raise e
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                print(
                    f"Authentication failed for {url}. Please check your credentials "
                    "(CRIBL_USERNAME, CRIBL_PASSWORD) or auth token (CRIBL_AUTH_TOKEN)."
                )
            print(f"HTTP error connecting to Cribl API at {url}: {e}")
            raise
        except requests.exceptions.RequestException as e:
            print(f"Error connecting to Cribl API at {url}: {e}")
            raise

    def get_worker_groups(self):
        """
        Retrieves all worker groups.
        Assumes the endpoint is /api/v1/master/groups.
        """
        return self._get("/api/v1/master/groups")

    def get_sources(self, group_id):
        """
        Retrieves all sources (inputs) for a given worker group.
        Assumes the endpoint is /api/v1/m/<group_id>/system/inputs.
        """
        return self._get(f"/api/v1/m/{group_id}/system/inputs")

    def get_destinations(self, group_id):
        """
        Retrieves all destinations (outputs) for a given worker group.
        Assumes the endpoint is /api/v1/m/<group_id>/system/outputs.
        """
        return self._get(f"/api/v1/m/{group_id}/system/outputs")

    def get_pipelines(self, group_id):
        """
        Retrieves all pipelines for a given worker group.
        Assumes the endpoint is /api/v1/m/<group_id>/pipelines.
        """
        return self._get(f"/api/v1/m/{group_id}/pipelines")


def get_api_client_from_env():
    """
    Creates a CriblAPI client from environment variables.
    """
    base_url = os.environ.get("CRIBL_BASE_URL", "http://localhost:9000")
    token = os.environ.get("CRIBL_AUTH_TOKEN")
    username = os.environ.get("CRIBL_USERNAME")
    password = os.environ.get("CRIBL_PASSWORD")

    return CriblAPI(base_url, username=username, password=password, token=token)


# Global variable to cache the API client
_cached_api_client = None


def get_cached_api_client():
    """
    Returns a cached CriblAPI client, initializing it if necessary.
    """
    global _cached_api_client
    if _cached_api_client is None:
        _cached_api_client = get_api_client_from_env()
    return _cached_api_client
