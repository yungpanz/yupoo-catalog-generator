import re

class ExtractPrice:
    def __init__(self):
        # Regular expression to match prices in yen
        self.price_regex = re.compile(r'(?:￥|¥)?(?P<price>\d+(?:[.,]\d+)?)')
        
    def extract(self, text):
        price_match = self.price_regex.search(text)
        if price_match:
            price = price_match.group('price')
            text = self.price_regex.sub('', text)
            #replace any punctuation with empty char to remove it
            price = float(price.replace(',','').replace('.',''))
            # removing leading and trailing white spaces
            text = text.strip()
            return {'price':price, 'name':text}
        else:
            return {'price': None, 'name': text}
