# Functionality: scrap all listing from acquire.com


import requests
import pandas as pd

class AcquireScrap:
    def __init__(self, auth_token: str, cookie: str):
        self.auth_token = auth_token
        self.cookie = cookie

    def transformation(self, response: dict) -> pd.DataFrame:
      df_choose = pd.json_normalize((response.json()['result']['marketplace']['results']))
      df = df_choose[['listingHeadline', 'techStack', 'askingPrice', 'revenue', 'annualProfit', 'customers', 'type', 'team', 'dateFounded', 'location',
        'totalRevenueAnnual', 'totalProfitAnnual', 'totalGrowthAnnual', 'revenueMultiple', 'profitMultiple',
        'businessVerified', 'keywords', 'businessModel', 'growthAnnual', 'weeklyViews', 'competitors',
        'about', 'status',
            ]]
      return df


    def scrap_data(self):
      url = "https://us-central1-microacquire.cloudfunctions.net/v1-search"
      headers = {
          "Authorization": f"Bearer {self.auth_token}",
          "Content-Type": "application/json",
          "Origin": "https://app.acquire.com",
          "Referer": "https://app.acquire.com/",
          "User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 14541.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
      }
      payload = {'data': {'marketplace': {'query': {'ids': {'exclude': [], 'only': None},
          'dateFounded': [{'range': {'gte': None, 'lte': 1711797751543},
            'type': 'and'}]},
        'skip': 0,
        'take': 1852,
        'order': [{'by': 'date', 'order': 'desc', 'salt': None}]},
        '__meta': {'referrer': 'https://app.acquire.com/all-listing',
        'cookie': f'{self.cookie}'}}}
      response = requests.post(url, json=payload, headers=headers)
      return self.transformation(response)


AUTH_TOKEN = '' # PLACE_AUTH_TOKEN_HERE
COOKIE - '' # PLACE_COOKIE_HERE
if not AUTH_TOKEN:
    raise ValueError('Please provide an auth token.')
if not COOKIE:
    raise ValueError('Please provide a cookie.')
get_data = AcquireScrap(auth_token , COOKIE)
df = get_data.scrap_data()
