from typing import Protocol, List, Optional
from api.models import TeamFormData, MatchResult, RawAggregateData


class SiteScraper(Protocol):
    """
    Her site için ortak interface.
    """

class BaseSiteScraper:
    def __init__(self, browser):
        self.browser = browser

    def get_team_form(self, team_name: str) -> Optional[TeamFormData]:
        ...

    def get_match_odds(self, home: str, away: str) -> Optional[dict]:
        ...


def safe_str(s: str | None) -> str:
    return (s or "").strip()
