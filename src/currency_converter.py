import requests
from bs4 import BeautifulSoup

class CurrencyConverter:
    def __init__(self):
        self.url = 'https://www.x-rates.com/calculator/'
    
    def _fetch_rate(self, from_currency, to_currency):
        params = {
            'from': from_currency,
            'to': to_currency,
            'amount': 1
        }
        response = requests.get(self.url, params=params)
        if response.status_code != 200:
            raise ValueError('Failed to retrieve conversion rate')
        
        soup = BeautifulSoup(response.text, 'html.parser')
        result = soup.find(class_='ccOutputRslt')
        rate = result.text.strip().split()[0]
        return float(rate)
    
    def convert(self, amount, from_currency, to_currency):
        if not isinstance(amount, (int, float)):
            raise TypeError('Amount must be a numeric value')
        rate = self._fetch_rate(from_currency, to_currency)
        return amount * rate

