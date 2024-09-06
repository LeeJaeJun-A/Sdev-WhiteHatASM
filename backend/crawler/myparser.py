import aiohttp
from bs4 import BeautifulSoup

class Parser:
    @staticmethod
    def get_soup(html_content):
        return BeautifulSoup(html_content, 'html.parser')

    @staticmethod
    async def extract_page_data(url, html_content, response):
        soup = Parser.get_soup(html_content)

        page_data = {
            'url': url,
            'title': soup.title.string if soup.title else 'No Title',
            'csrf_token': Parser.extract_csrf_token(soup),
            'cookies': {cookie.key: cookie.value for cookie in response.cookies.values()},
            'input_tags': [{'name': input.get('name', ''), 'type': input.get('type', ''), 'id': input.get('id', ''), 'value': input.get('value', '')}
                           for input in soup.find_all('input')]
        }

        return page_data

    @staticmethod
    def extract_csrf_token(soup):
        # Find various tags
        potential_names = ['csrf-token', 'csrf_token', 'authenticity_token', 'xsrf-token']

        # Find from  Meta tag
        for name in potential_names:
            csrf_meta = soup.find('meta', attrs={'name': name})
            if csrf_meta:
                return csrf_meta.get('content')

        # Find from  Input tag
        for name in potential_names:
            csrf_input = soup.find('input', attrs={'name': name})
            if csrf_input:
                return csrf_input.get('value')

        return None
