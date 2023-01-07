import requests

class WebPage:
    def __init__(self, url):
        self.url = url

    def get_page_content(self):
        # Set the timeout for the HTTP request to 5 seconds
        timeout = 5

        # Make the HTTP request to the specified URL
        try:
            response = requests.get(self.url, timeout=timeout)
        except requests.exceptions.RequestException:
            # If the request fails, retry the request until it succeeds
            while True:
                try:
                    response = requests.get(self.url, timeout=timeout)
                    break
                except requests.exceptions.RequestException:
                    continue

        # Return the content of the page
        return response.content