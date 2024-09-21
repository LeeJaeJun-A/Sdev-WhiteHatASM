import asyncio
import aiohttp
from bs4 import BeautifulSoup
import json
import re
from urllib.parse import urljoin
import logging
import sys
import hashlib
import struct
import socket

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AdvancedWebAnalyzer:
    def __init__(self, url):
        self.url = url if url.startswith(('http://', 'https://')) else f'https://{url}'
        self.results = {'server': {}, 'os': None, 'technologies': [], 'frameworks': []}
        self.ip = None

    async def analyze(self):
        try:
            self.ip = socket.gethostbyname(self.url.split('//')[1].split('/')[0])
        except Exception as e:
            logger.error(f"Error resolving IP: {e}")
            return self.results

        async with aiohttp.ClientSession() as session:
            await asyncio.gather(
                self.analyze_http_response(session),
                self.analyze_error_pages(session),
                self.analyze_dynamic_content(session),
                self.analyze_static_files(session),
                self.analyze_tcp_ip()
            )
        self.remove_duplicates()
        return self.results

    async def analyze_http_response(self, session):
        try:
            async with session.get(self.url) as response:
                headers = response.headers
                self.analyze_server_header(headers)
                self.analyze_other_headers(headers)
                self.analyze_os_from_headers(headers)
                
        except Exception as e:
            logger.error(f"Error in HTTP response analysis: {e}")

    def analyze_server_header(self, headers):
        server_header = headers.get('Server', '')
        self.results['server']['name'] = server_header

        server_patterns = {
            'nginx': r'nginx(?:/(\d+\.\d+\.\d+))?',
            'apache': r'Apache(?:/(\d+\.\d+\.\d+))?',
            'iis': r'Microsoft-IIS(?:/(\d+\.\d+))?',
            'lighttpd': r'lighttpd(?:/(\d+\.\d+\.\d+))?',
            'openresty': r'openresty(?:/(\d+\.\d+\.\d+))?',
            'tomcat': r'Apache-Coyote(?:/(\d+\.\d+))?',
            'node.js': r'Node\.js',
            'gunicorn': r'gunicorn(?:/(\d+\.\d+\.\d+))?',
            'caddy': r'Caddy',
        }

        for server, pattern in server_patterns.items():
            match = re.search(pattern, server_header, re.IGNORECASE)
            if match:
                self.results['server']['type'] = server
                if match.group(1):
                    self.results['server']['version'] = match.group(1)
                break

    def analyze_other_headers(self, headers):
        header_indicators = {
            'X-Powered-By': lambda v: self.results['technologies'].append(v),
            'X-AspNet-Version': lambda v: self.results['technologies'].append(f"ASP.NET {v}"),
            'X-Rails-Version': lambda v: self.results['frameworks'].append(f"Ruby on Rails {v}"),
            'X-Django-Version': lambda v: self.results['frameworks'].append(f"Django {v}"),
            'X-Generator': lambda v: self.results['technologies'].append(v),
        }

        for header, value in headers.items():
            if header in header_indicators:
                header_indicators[header](value)

    def analyze_os_from_headers(self, headers):
        server_header = headers.get('Server', '').lower()
        
        if 'win' in server_header:
            self.results['os'] = 'Windows'
        elif any(os in server_header for os in ['unix', 'linux', 'debian', 'ubuntu', 'centos']):
            self.results['os'] = 'Unix/Linux'
        elif 'darwin' in server_header:
            self.results['os'] = 'macOS'
        else:
            self.analyze_os_from_other_indicators(headers)

    def analyze_os_from_other_indicators(self, headers):
        # Additional OS detection logic
        if 'X-Powered-By' in headers:
            powered_by = headers['X-Powered-By'].lower()
            if 'php' in powered_by:
                self.results['os'] = 'Unix/Linux (probable)'
            elif 'asp.net' in powered_by:
                self.results['os'] = 'Windows'
        
        # Check for specific headers that might indicate OS
        if 'X-AspNet-Version' in headers:
            self.results['os'] = 'Windows'
        elif 'X-Linux-Expires' in headers:
            self.results['os'] = 'Linux'

    async def analyze_error_pages(self, session):
        error_paths = ['/nonexistent', '/admin', '/login', '/api']
        for path in error_paths:
            try:
                async with session.get(urljoin(self.url, path), allow_redirects=False) as response:
                    if response.status != 200:
                        content = await response.text()
                        self.analyze_error_content(content)
            except Exception as e:
                logger.error(f"Error analyzing error page {path}: {e}")

    def analyze_error_content(self, content):
        error_patterns = {
            'nginx': r'nginx/(\d+\.\d+\.\d+)',
            'apache': r'Apache/(\d+\.\d+\.\d+)',
            'iis': r'Microsoft-IIS/(\d+\.\d+)',
            'php': r'PHP/(\d+\.\d+\.\d+)',
            'tomcat': r'Apache Tomcat/(\d+\.\d+\.\d+)',
            'django': r'Django',
            'laravel': r'Laravel',
            'symfony': r'Symfony',
        }

        for tech, pattern in error_patterns.items():
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                if tech in ['nginx', 'apache', 'iis', 'tomcat']:
                    self.results['server']['type'] = tech
                    self.results['server']['version'] = match.group(1)
                elif tech == 'php':
                    self.results['technologies'].append(f"PHP {match.group(1)}")
                else:
                    self.results['frameworks'].append(tech)

        # OS detection from error pages
        if 'windows' in content.lower():
            self.results['os'] = 'Windows'
        elif any(os in content.lower() for os in ['linux', 'unix', 'debian', 'ubuntu', 'centos']):
            self.results['os'] = 'Unix/Linux'

    async def analyze_dynamic_content(self, session):
        try:
            async with session.get(self.url) as response:
                content = await response.text()
                soup = BeautifulSoup(content, 'html.parser')

                self.analyze_meta_tags(soup)
                await self.analyze_script_tags(soup, session)
                self.analyze_link_tags(soup)
                self.analyze_inline_styles(soup)
                self.analyze_html_structure(soup)

        except Exception as e:
            logger.error(f"Error in dynamic content analysis: {e}")

    def analyze_meta_tags(self, soup):
        meta_indicators = {
            'generator': lambda v: self.results['technologies'].append(v),
            'application-name': lambda v: self.results['technologies'].append(v),
        }

        for tag in soup.find_all('meta'):
            name = tag.get('name', '').lower()
            content = tag.get('content', '')
            if name in meta_indicators and content:
                meta_indicators[name](content)

    async def analyze_script_tags(self, soup, session):
        for script in soup.find_all('script'):
            if script.get('src'):
                await self.analyze_external_script(session, script['src'])
            else:
                self.analyze_inline_script(script.string)

    async def analyze_external_script(self, session, src):
        try:
            async with session.get(urljoin(self.url, src)) as response:
                script_content = await response.text()
                self.analyze_script_content(script_content)
        except Exception as e:
            logger.error(f"Error analyzing external script {src}: {e}")

    def analyze_inline_script(self, content):
        if content:
            self.analyze_script_content(content)

    def analyze_script_content(self, content):
        framework_patterns = {
            'React': r'(?:React\.|ReactDOM\.|jsx)',
            'Vue.js': r'(?:Vue\.|Vuex\.|v-bind:|v-on:)',
            'Angular': r'(?:angular\.|ng-app|ng-controller)',
            'jQuery': r'(?:\$\(|jQuery\()',
            'Lodash': r'_\.',
            'Moment.js': r'moment\(',
            'Axios': r'axios\.',
            'D3.js': r'd3\.',
            'Backbone.js': r'Backbone\.',
            'Ember.js': r'Ember\.',
            'Svelte': r'svelte\.',
            'Next.js': r'next/|useRouter\(\)',
            'Nuxt.js': r'nuxt\.|useNuxt\(\)',
            'Alpine.js': r'x-data|x-bind',
            'Meteor': r'Meteor\.',
            'Polymer': r'Polymer\(',
        }

        for framework, pattern in framework_patterns.items():
            if re.search(pattern, content):
                self.results['frameworks'].append(framework)

        version_patterns = {
            'React': r'React\.version\s*=\s*[\'"](\d+\.\d+\.\d+)[\'"]',
            'Vue.js': r'Vue\.version\s*=\s*[\'"](\d+\.\d+\.\d+)[\'"]',
            'Angular': r'angular\.version\.full\s*=\s*[\'"](\d+\.\d+\.\d+)[\'"]',
            'jQuery': r'jQuery\.fn\.jquery\s*=\s*[\'"](\d+\.\d+\.\d+)[\'"]',
        }

        for framework, pattern in version_patterns.items():
            match = re.search(pattern, content)
            if match:
                self.results['frameworks'].append(f"{framework} {match.group(1)}")

    def analyze_link_tags(self, soup):
        for link in soup.find_all('link'):
            href = link.get('href', '')
            rel = link.get('rel', [])
            
            if 'stylesheet' in rel:
                if 'bootstrap' in href:
                    self.results['frameworks'].append('Bootstrap')
                elif 'foundation' in href:
                    self.results['frameworks'].append('Foundation')
                elif 'materialize' in href:
                    self.results['frameworks'].append('Materialize')
                elif 'bulma' in href:
                    self.results['frameworks'].append('Bulma')

    def analyze_inline_styles(self, soup):
        inline_styles = soup.find_all('style')
        for style in inline_styles:
            content = style.string
            if content:
                if re.search(r'\.col-[sm|md|lg|xl]', content):
                    self.results['frameworks'].append('Bootstrap (probable)')
                elif re.search(r'\.pure-', content):
                    self.results['frameworks'].append('Pure.css')

    def analyze_html_structure(self, soup):
        if soup.select('[ng-app]') or soup.select('[ng-controller]'):
            self.results['frameworks'].append('Angular.js')
        if soup.select('[v-app]') or soup.select('[v-bind]'):
            self.results['frameworks'].append('Vue.js')
        if soup.select('[data-reactroot]') or soup.select('[data-reactid]'):
            self.results['frameworks'].append('React')

    async def analyze_static_files(self, session):
        common_paths = [
            '/robots.txt',
            '/sitemap.xml',
            '/crossdomain.xml',
            '/favicon.ico',
            '/ads.txt',
        ]

        for path in common_paths:
            try:
                async with session.get(urljoin(self.url, path)) as response:
                    if response.status == 200:
                        content = await response.read()
                        self.analyze_static_file_content(path, content)
            except Exception as e:
                logger.error(f"Error analyzing static file {path}: {e}")

    def analyze_static_file_content(self, path, content):
        if path == '/favicon.ico':
            favicon_hash = hashlib.md5(content).hexdigest()
            known_favicons = {
                '88733ee53676a47fc354a61c32516e82': 'WordPress',
                'b167e729e045acc459f64b3558d0fbd8': 'Joomla',
                '21aca_1668_18': 'Drupal',
            }
            if favicon_hash in known_favicons:
                self.results['technologies'].append(known_favicons[favicon_hash])

        elif path == '/robots.txt':
            if b'Wordpress' in content:
                self.results['technologies'].append('WordPress')
            elif b'Drupal' in content:
                self.results['technologies'].append('Drupal')

    async def analyze_tcp_ip(self):
        try:
            reader, writer = await asyncio.open_connection(self.ip, 80)
            
            # Send a minimal HTTP request
            writer.write(b"GET / HTTP/1.0\r\nHost: " + self.url.encode() + b"\r\n\r\n")
            await writer.drain()

            # Read the response
            data = await reader.read(4096)
            writer.close()
            await writer.wait_closed()

            # Analyze the TCP/IP characteristics
            if data:
                self.analyze_tcp_fingerprint(data)
        except Exception as e:
            logger.error(f"Error in TCP/IP analysis: {e}")

    def analyze_tcp_fingerprint(self, data):
        try:
            # Extract initial TTL
            ttl = struct.unpack('!B', data[8:9])[0]
            
            # Extract TCP options
            tcp_options = data[40:60]  # Assuming TCP options are within this range
            
            # Window size
            window_size = struct.unpack('!H', data[34:36])[0]

            # Analyze these characteristics
            if 32 <= ttl <= 64:
                os = 'Unix/Linux'
            elif 64 < ttl <= 128:
                os = 'Windows'
            elif ttl > 128:
                os = 'Cisco/Network Device'
            else:
                os = 'Unknown'

            # Refine based on TCP options and window size
            if b'\x02\x04' in tcp_options:  # MSS option
                if window_size == 8192:
                    os = 'Windows (newer versions)'
                elif window_size == 65535:
                    os = 'Unix/Linux (newer versions)'
            
            # Update the result only if we couldn't determine OS from headers
            if self.results['os'] is None:
                self.results['os'] = os

        except Exception as e:
            logger.error(f"Error in TCP fingerprint analysis: {e}")

    def remove_duplicates(self):
        self.results['technologies'] = list(dict.fromkeys(self.results['technologies']))
        self.results['frameworks'] = list(dict.fromkeys(self.results['frameworks']))

async def main():
    url = input("Enter the URL to scan: ")
    analyzer = AdvancedWebAnalyzer(url)
    results = await analyzer.analyze()
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    asyncio.run(main())