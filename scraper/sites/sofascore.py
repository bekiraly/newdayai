from scraper.sites.base import BaseSiteScraper


class SofaScoreScraper(BaseSiteScraper):
    """
    Sofascore scraping işlemleri.
    Sadece structure oluşturduk, gerçek scraping Browser sınıfında yapılacak.
    """

    async def get_last_5_matches(self, team: str) -> dict:
        """
        Takımın son 5 maç formunu döner.
        Şimdilik dummy veri dönüyoruz.
        Browser scraper tamamlanınca gerçek veri gelecek.
        """
        return {
            "team": team,
            "form": ["G", "B", "M", "G", "M"],
            "scores": ["2-1", "1-1", "0-2", "3-0", "1-2"],
        }
