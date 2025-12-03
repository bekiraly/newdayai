from api.models import RawAggregateData, TeamFormData
from scraper.sites.sofascore import SofaScoreScraper
from scraper.sites.nesine import NesineScraper
from scraper.browser import Browser


async def analyze_match(home: str, away: str) -> RawAggregateData:
    """
    Tüm sitelerden veri toplayıp tekleştiriyoruz.
    """

    async with Browser() as browser:
        ss = SofaScoreScraper(browser)
        ns = NesineScraper(browser)

        # Sofascore form
        form_home = await ss.get_team_form(home)
        form_away = await ss.get_team_form(away)

        # Nesine oranları
        odds = await ns.get_odds(home, away)

        return RawAggregateData(
            home=home,
            away=away,
            form_home=form_home,
            form_away=form_away,
            odds=odds,
        )
