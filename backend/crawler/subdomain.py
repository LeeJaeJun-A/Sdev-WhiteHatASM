import asyncio
import aiohttp
import sys
import re
import json
import ssl
import tldextract
from urllib.parse import urlparse

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

class SubdomainScanner:
    def __init__(self, domain):
        self.domain = self.normalize_domain(domain)
        self.subdomains = set()
        self.session = None

    def normalize_domain(self, domain):
        # Remove protocol if present
        domain = re.sub(r'^https?://', '', domain)
        # Remove trailing slash if present
        domain = domain.rstrip('/')
        # Extract the main domain
        parts = domain.split('.')
        if len(parts) > 2:
            domain = '.'.join(parts[-2:])
        return domain

    def is_valid_subdomain(self, subdomain):
        # Check if subdomain is not just an IP address
        if re.match(r'^\d+\.\d+\.\d+\.\d+$', subdomain):
            return False
        # Check if subdomain ends with the main domain
        if not subdomain.endswith(self.domain):
            return False
        # Check if subdomain has at least one additional level
        if subdomain == self.domain:
            return False
        return True
    
    def is_valid_subdomain(self, subdomain):
        # TLD 추출을 위해 tldextract 사용
        ext = tldextract.extract(subdomain)
        
        # 메인 도메인과 일치하는지 확인
        if ext.domain != self.domain.split('.')[0] or ext.suffix != self.domain.split('.')[1]:
            return False
        
        # 서브도메인이 비어있으면 제외 (메인 도메인만 있는 경우)
        if not ext.subdomain:
            return False
        
        # 이메일 주소 형식 제외
        if '@' in subdomain:
            return False
        
        # 일반적인 이메일 관련 서브도메인 제외
        email_related = ['mail', 'email', 'smtp', 'pop', 'imap', 'webmail']
        if ext.subdomain in email_related:
            return False
        
        # 숫자로만 이루어진 서브도메인 제외
        if ext.subdomain.isdigit():
            return False
        
        # 특수문자가 포함된 서브도메인 제외 (하이픈 제외)
        if re.search(r'[^a-zA-Z0-9-]', ext.subdomain):
            return False
        
        # 길이가 너무 긴 서브도메인 제외 (예: 50자 이상)
        if len(ext.subdomain) > 50:
            return False

        return True

    async def scan(self):
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        conn = aiohttp.TCPConnector(ssl=ssl_context)
        async with aiohttp.ClientSession(connector=conn) as self.session:
            await asyncio.gather(
                self.search_crt_sh(),
                self.search_virustotal(),
                self.search_hackertarget(),
                self.search_threatcrowd(),
            )
        raw_subdomains = list(self.subdomains)
        filtered_subdomains = list(filter(self.is_valid_subdomain, raw_subdomains))
        
        print(f"Total subdomains found: {len(raw_subdomains)}")
        print(f"Valid subdomains after filtering: {len(filtered_subdomains)}")
        
        return sorted(filtered_subdomains)

    async def make_request(self, url, max_retries=3):
        for _ in range(max_retries):
            try:
                async with self.session.get(url, timeout=30) as response:
                    if response.status == 200:
                        return await response.text()
            except Exception as e:
                print(f"Error connecting to {url}: {e}")
                await asyncio.sleep(1)
        return None

    async def search_crt_sh(self):
        url = f"https://crt.sh/?q=%.{self.domain}&output=json"
        response = await self.make_request(url)
        if response:
            try:
                data = json.loads(response)
                for entry in data:
                    self.subdomains.add(entry['name_value'].lower())
            except json.JSONDecodeError:
                print("Error decoding JSON from crt.sh")

    async def search_virustotal(self):
        url = f"https://www.virustotal.com/ui/domains/{self.domain}/subdomains"
        response = await self.make_request(url)
        if response:
            try:
                data = json.loads(response)
                for item in data.get('data', []):
                    if 'id' in item:
                        self.subdomains.add(item['id'].lower())
            except json.JSONDecodeError:
                print("Error decoding JSON from VirusTotal")

    async def search_hackertarget(self):
        url = f"https://api.hackertarget.com/hostsearch/?q={self.domain}"
        response = await self.make_request(url)
        if response:
            subdomains = re.findall(r'(.*?)\,', response)
            self.subdomains.update(map(str.lower, subdomains))

    async def search_threatcrowd(self):
        url = f"https://www.threatcrowd.org/searchApi/v2/domain/report/?domain={self.domain}"
        response = await self.make_request(url)
        if response:
            try:
                data = json.loads(response)
                for subdomain in data.get('subdomains', []):
                    self.subdomains.add(subdomain.lower())
            except json.JSONDecodeError:
                print("Error decoding JSON from ThreatCrowd")

async def main():
    domain = input("Enter the domain to scan for subdomains: ")
    scanner = SubdomainScanner(domain)
    subdomains = await scanner.scan()
    result = {
        "domain": scanner.domain,
        "subdomains": subdomains
    }
    
    filename = f"{scanner.domain}_subdomains.json"
    with open(filename, 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"Scan complete. Results saved to {filename}")
    print(f"Found {len(subdomains)} valid subdomains.")

if __name__ == "__main__":
    asyncio.run(main())