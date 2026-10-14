import os

import requests
import pandas as pd
from dotenv import load_dotenv

# load ACCESS_TOKEN from the .env file into the environment
load_dotenv()


class Genius:
    """client for Genius API"""

    # all Genius API endpoints start with this URL
    BASE_URL = "https://api.genius.com"

    def __init__(self, access_token):
        # save the token so every request can use it
        self.access_token = access_token

    def _get(self, path, params=None):
        """Send a GET request to a Genius API path and return the full JSON"""
        # pass the token in the header
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.get(self.BASE_URL + path,
                                params=params, headers=headers)

        # raise an error if the request failed
        response.raise_for_status()

        return response.json()

    def search(self, search_term, per_page=10):
        """Search Genius and return the list of hits"""
        data = self._get("/search", params={"q": search_term,
                                            "per_page": per_page})
        # the hits are nested under the "response" key
        return data["response"]["hits"]

    def get_artist_id(self, search_term):
        """Get the primary artist ID from the first hit"""
        hits = self.search(search_term, per_page=1)

        # no results means there is no artist to look up
        if not hits:
            return None

        # grab the song's primary artist from each hit
        return hits[0]["result"]["primary_artist"]["id"]

    def get_artist(self, search_term):
        """Get information about the artist"""
        artist_id = self.get_artist_id(search_term)

        if artist_id is None:
            return {}

        # look up the artist's details using their ID
        return self._get(f"/artists/{artist_id}")

    def get_artists(self, search_terms):
        """Build a DataFrame of artist info for a list of search terms"""
        # build one row (dict) per search term
        rows = [self._artist_row(term) for term in search_terms]
        return pd.DataFrame(rows)

    def _artist_row(self, search_term):
        """Create a single DataFrame row"""
        artist = self.get_artist(search_term).get("response", {}).get("artist", {})

        # use .get() so missing values become None instead of an error
        return {
            "search_term": search_term,
            "artist_name": artist.get("name"),
            "artist_id": artist.get("id"),
            "followers_count": artist.get("followers_count"),
        }
