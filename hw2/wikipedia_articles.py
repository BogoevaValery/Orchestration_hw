import re
from collections import deque
import json
import argparse
import requests
from bs4 import BeautifulSoup

def get_internal_links(base_url, href):
    my_headers = {"User-Agent": "Mozilla/5.0"}
    full_url = requests.compat.urljoin(base_url, href)
    article = requests.get(full_url, headers=my_headers)
    
    print(f"Status code: {article.status_code}")
    
    bs = BeautifulSoup(article.text, "html.parser")
    
    pattern = re.compile(r"^(/wiki/)((?!:).)*$")
    content = bs.find("div", id="bodyContent")
    
    res = []
    for link in content.find_all("a", href=pattern):
        href = link["href"]
        match = pattern.match(href)
        if match:
            article = match.group(1)
            res.append(article)
    
    return list(set(res))

def walk_on_depth(src, max_depth):
    base_url = "https://en.wikipedia.org/wiki/"
    
    visited = set()       
    graph = {}            
    queue = deque()       
    queue.append((src, 1))

    while queue:
        current, depth = queue.popleft()   
        if current in visited:
            continue

        print(f"Обрабатываем {current} (глубина {depth})")
        links = get_internal_links(base_url, current)
        graph[current] = links
        visited.add(current)

        if depth < max_depth:
            for link in links:
                if link not in visited:
                    queue.append((link, depth + 1))
                    
    return graph

parser = argparse.ArgumentParser(prog="My wiki crawler", description="Builds network graph of english wiki in some depth of some url")
parser.add_argument("--url", required=True, help="Link to wiki page")
parser.add_argument("--depth", default=3, help="Depth for walking from url")
parser.add_argument("--out_json", required=True,help="Name of output json")
args = parser.parse_args()

res = walk_on_depth(parser.url, parser.depth)
print(*res, sep="\n")
with open(parser.out_json, "w", encoding="utf-8") as out:
    json.dump(res, out)