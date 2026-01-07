import os

import requests


class CriblAPI:
    """
    A client for interacting with the Cribl API.
    Assumes it is running on the leader node.
    """

    def __init__(self, base_url="http://localhost:9000", token=None):
        """
        Initializes the CriblAPI client.

        Args:
            base_url (str): The base URL of the Cribl API. Defaults to http://localhost:9000.
            token (str): The authentication token.
        """
        self.base_url = base_url
        if token:
            self.headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            }
        else:
            # for on-prem, if you are on the master node, you might not need a token
            self.headers = {"Content-Type": "application/json"}

    def _get(self, endpoint):
        """
        Performs a GET request to the specified endpoint.
        """
        url = self.base_url + endpoint
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
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

    return CriblAPI(base_url, token)
