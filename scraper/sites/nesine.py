from scraper.sites.base import BaseSiteScraper


class NesineScraper(BaseSiteScraper):
    """
    Nesine scraping henüz aktif değil.
    Şimdilik dummy oran döndürüyoruz.
    """

    async def get_last_5_matches(self, team: str):
        # Nesine üzerinden form çekmek için iskelet
        return {
            "team": team,
            "form": ["G", "B", "M", "G", "B"],
            "scores": ["2-0", "1-1", "0-1", "3-1", "2-2"]
        }

    async def get_odds(self, home: str, away: str):
        # Dummy odds (gerçek scraping daha sonra eklenecek)
        return {
            "home": 1.85,
            "draw": 3.10,
            "away": 2.55
        }
