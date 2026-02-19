from django.test import TestCase

def test_settings_loaded():
    from django.conf import settings
    assert settings.SCRAPE_INTERVAL_HOURS > 0
    assert settings.SCRAPE_TIMEZONE
    assert settings.PLAYWRIGHT_BROWSER