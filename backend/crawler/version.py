import asyncio
import aiohttp
from bs4 import BeautifulSoup
import json
import time
import re
from urllib.parse import urljoin
import logging
import sys

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AdvancedWebAnalyzer:
    def __init__(self, url):
        self.url = url if url.startswith(('http://', 'https://')) else f'https://{url}'
        self.results = {'server': {}, 'os': None, 'technologies': []}

    async def analyze(self):
        async with aiohttp.ClientSession() as session:
            await asyncio.gather(
                self.analyze_tcp_ip(),
                self.analyze_http_response(session),
                self.analyze_error_pages(session),
                self.analyze_dynamic_content(session)
            )
        self.remove_duplicates()
        return self.results

    async def analyze_tcp_ip(self):
        try:
            start_time = time.time()
            reader, writer = await asyncio.open_connection(self.url.split('//')[1], 80)
            writer.close()
            end_time = time.time()
            rtt = end_time - start_time

            if rtt < 0.05:
                self.results['os'] = 'Likely Linux (Fast RTT)'
            elif rtt < 0.1:
                self.results['os'] = 'Possibly Windows or optimized Linux'
            else:
                self.results['os'] = 'Unknown (Slow RTT)'

        except Exception as e:
            print(f"Error in TCP/IP analysis: {e}")

    async def analyze_http_response(self, session):
        try:
            async with session.get(self.url) as response:
                headers = response.headers
                server = headers.get('Server', '')
                self.results['server']['name'] = server

                if 'nginx' in server.lower():
                    self.results['server']['type'] = 'Nginx'
                elif 'apache' in server.lower():
                    self.results['server']['type'] = 'Apache'
                elif 'iis' in server.lower():
                    self.results['server']['type'] = 'IIS'

                # Analyze other headers
                for header, value in headers.items():
                    if 'x-powered-by' in header.lower():
                        self.results['technologies'].append(value)

        except Exception as e:
            print(f"Error in HTTP response analysis: {e}")

    async def analyze_error_pages(self, session):
        error_paths = ['/nonexistent', '/admin', '/login', '/api']
        for path in error_paths:
            try:
                async with session.get(urljoin(self.url, path), allow_redirects=False) as response:
                    if response.status != 200:
                        content = await response.text()
                        if 'nginx' in content.lower():
                            self.results['server']['type'] = 'Nginx'
                        elif 'apache' in content.lower():
                            self.results['server']['type'] = 'Apache'
                        elif 'iis' in content.lower():
                            self.results['server']['type'] = 'IIS'
            except Exception as e:
                print(f"Error analyzing error page {path}: {e}")

    async def analyze_dynamic_content(self, session):
        try:
            async with session.get(self.url) as response:
                content = await response.text()
                soup = BeautifulSoup(content, 'html.parser')

                # Analyze script tags
                scripts = soup.find_all('script')
                for script in scripts:
                    if script.get('src'):
                        await self.analyze_external_script(session, script['src'])
                    else:
                        self.analyze_inline_script(script.string)

                # Analyze meta tags
                meta_tags = soup.find_all('meta')
                for tag in meta_tags:
                    if tag.get('name') == 'generator':
                        self.results['technologies'].append(tag.get('content'))

        except Exception as e:
            print(f"Error in dynamic content analysis: {e}")

    async def analyze_external_script(self, session, src):
        try:
            async with session.get(urljoin(self.url, src)) as response:
                script_content = await response.text()
                self.analyze_script_content(script_content)
        except Exception as e:
            print(f"Error analyzing external script {src}: {e}")

    def analyze_inline_script(self, content):
        if content:
            self.analyze_script_content(content)

    def analyze_script_content(self, content):
        tech_patterns = {
            'React': r'React',
            'Vue.js': r'Vue',
            'Angular': r'angular',
            'jQuery': r'jQuery',
            'Lodash': r'_\.',
            'Moment.js': r'moment',
            'Axios': r'axios'
        }

        for tech, pattern in tech_patterns.items():
            if re.search(pattern, content):
                self.results['technologies'].append(tech)

    def remove_duplicates(self):
        self.results['technologies'] = list(dict.fromkeys(self.results['technologies']))

async def main():
    url = input("Enter the URL to scan: ")
    analyzer = AdvancedWebAnalyzer(url)
    results = await analyzer.analyze()
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    asyncio.run(main())