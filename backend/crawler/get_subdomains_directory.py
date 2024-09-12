import asyncio
import aiohttp
from urllib.parse import urljoin, urlparse
import json
import logging
from backend.crawler.myparser import Parser

logging.basicConfig(level=logging.INFO)

class SubdomainDirectoryCrawler:
    def __init__(self, start_url, max_depth=0):
        self.start_url = start_url
        self.base_domain = urlparse(start_url).netloc
        self.max_depth = max_depth

    async def extract_links_and_parse(self, url, session):
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    html_content = await response.text()
                    soup = Parser.get_soup(html_content)
                    links = set()

                    # get href tag
                    for link in soup.find_all('a', href=True):
                        absolute_url = urljoin(url, link.get('href'))
                        if urlparse(absolute_url).netloc == self.base_domain:
                            links.add(absolute_url)

                    page_data = await Parser.extract_page_data(url, html_content, response)
                    return list(links), page_data
                else:
                    logging.warning(f"ERROR: status code {response.status}")
                    return [], None
        except Exception as e:
            logging.error(f"ERROR: {e}")
            return [], None

    async def crawl_bfs(self, session):
        visited = set()
        queue = [(self.start_url, 0)]
        result_tree = {"url": self.start_url, "details": None, "children": []}

        while queue:
            url, depth = queue.pop(0)

            # depth check
            if url in visited or (self.max_depth > 0 and depth > self.max_depth):
                continue

            visited.add(url)
            logging.info(f"{url}   depth {depth}")

            links, page_data = await self.extract_links_and_parse(url, session)

            current_node = self.find_node(result_tree, url)
            if current_node:
                current_node["details"] = page_data
                current_node["children"] = []

                for link in links:
                    if link not in visited and urlparse(link).netloc == self.base_domain:
                        queue.append((link, depth + 1))
                        child_node = {"url": link, "details": None, "children": []}
                        current_node["children"].append(child_node)

        return result_tree

    def find_node(self, tree, target_url):
        if tree["url"] == target_url:
            return tree
        for child in tree.get("children", []):
            result = self.find_node(child, target_url)
            if result:
                return result
        return None

    async def run(self):
        async with aiohttp.ClientSession() as session:
            logging.info(f"======== START {self.start_url} ========")
            result_tree = await self.crawl_bfs(session)

        # save as JSON
        if result_tree:
            output_file = f"{self.base_domain}_parsed_data.json"
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(result_tree, f, indent=2)
            logging.info(f"saved {output_file}")
        return result_tree
