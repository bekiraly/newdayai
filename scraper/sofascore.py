"""
Dummy sofascore module.
Gerçek Sofascore API kullanılmadığı için bu dosya sadece import hatalarını önler.
"""

def get_last_five_matches(*args, **kwargs):
    return {
        "team": None,
        "form": "",
        "matches": []
    }

def get_team_id(*args, **kwargs):
    return None

def get_super_lig_league_and_season(*args, **kwargs):
    return None
