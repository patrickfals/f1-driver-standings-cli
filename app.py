"""
Display Formula 1 driver standings for a selected season.
"""

import pandas as pd
import requests
from requests.adapters import HTTPAdapter


def _get_json_content_from_url(url, *args, timeout: int = 15, **kwargs):
    """Fetch JSON data from Jolpica API with retry handling."""
    session = requests.Session()
    session.mount("https://api.jolpi.ca", HTTPAdapter(max_retries=2))
    return session.get(url, *args, timeout=timeout, **kwargs).json()


# Get the most recent F1 season from API
CURR_YEAR = int(
    _get_json_content_from_url(
        "https://api.jolpi.ca/ergast/f1/seasons.json?limit=200"
    )["MRData"]["SeasonTable"]["Seasons"][-1]["season"]
)


def driver_standings(year: int):
    """Return driver standings as DataFrame."""

    json_data = _get_json_content_from_url(
        f"https://api.jolpi.ca/ergast/f1/{year}/driverStandings.json"
    )

    standings_lists = json_data["MRData"]["StandingsTable"]["StandingsLists"]
    if not standings_lists:
        raise ValueError(f"No standings found for {year}.")

    # API returns standings in a list
    standings_json = standings_lists[0]["DriverStandings"]

    d_res = DriverResults(standings_json)

    return pd.DataFrame(
        zip(
            d_res.get_driver_positions(),
            d_res.get_driver_names(),
            d_res.get_driver_nationality(),
            d_res.get_driver_teams(),
            d_res.get_driver_points(),
            d_res.get_driver_wins(),
        ),
        columns=["POS", "Driver", "Nationality", "Constructor", "Points", "Wins"],
    )


class DriverResults:
    """Extract driver data from API."""

    def __init__(self, results):
        """Store raw standings data."""
        self.results = results

    def get_driver_positions(self):
        """Return driver positions."""
        return [i.get("position") or i.get("positionText") for i in self.results]

    def get_driver_names(self):
        """Return full driver names."""
        return [
            f"{i['Driver']['givenName']} {i['Driver']['familyName']}"
            for i in self.results
        ]

    def get_driver_points(self):
        """Return driver points."""
        return [i["points"] for i in self.results]

    def get_driver_teams(self):
        """Return constructor names."""
        return [i["Constructors"][0]["name"] for i in self.results]

    def get_driver_nationality(self):
        """Return driver nationalities."""
        return [i["Driver"]["nationality"] for i in self.results]

    def get_driver_wins(self):
        """Return total wins per driver."""
        return [i["wins"] for i in self.results]


if __name__ == "__main__":
    MAX_YEAR = 2025

    while True:
        user_input = input(f"Enter a year (1950–{MAX_YEAR}, default {MAX_YEAR}): ") or MAX_YEAR

        try:
            year = int(user_input)

            if 1950 <= year <= MAX_YEAR:
                break

            print(f"Year must be between 1950 and {MAX_YEAR}.")

        except ValueError:
            print("Please enter a valid number.")

    standings_df = driver_standings(year)

    # Print without the default DataFrame index column
    print(standings_df.to_string(index=False))
