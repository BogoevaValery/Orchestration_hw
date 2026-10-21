#!/home/lerathebest/.local/share/virtualenvs/Orchestration_hw-na0ESBGG/bin/python

import re
from collections import deque
import json
import argparse
import requests
from bs4 import BeautifulSoup

def get_internal_links(base_url, target):
    my_headers = {"User-Agent": "Mozilla/5.0"}
    #full_url = requests.compat.urljoin(base_url, target)
    full_url = base_url + target
    print(f"Fetching {full_url}...")
    article = requests.get(full_url, headers=my_headers)
    
    print(f"Status code: {article.status_code}")
    
    bs = BeautifulSoup(article.text, "html.parser")
    
    pattern = re.compile(r"/wiki/((?![А-Яа-я:]|File:|Category:|Help:|Portal:|Wikipedia:|Special:|Template:|Talk:)(.*))")

    content = bs.find("div", id="bodyContent")
    
    if content is None:
        print(f"Предупреждение: bodyContent не найден на {full_url}")
        return []
    
    res = []
    for link in content.find_all("a", href=pattern):
        href = link["href"]
        match = pattern.search(href)
        if match:
            article = match.group(2)
            res.append(article)
    
    return list(set(res))

def walk_on_depth(url, max_depth):
    base_url = "https://en.wikipedia.org/wiki/"
    
    visited = set()       
    graph = {}            
    queue = deque()  
    src = url.split("/")[-1]       
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

print("Starting wiki crawler...")
parser = argparse.ArgumentParser(prog="My wiki crawler", description="Builds network graph of english wiki in some depth of some url")
parser.add_argument("--url", required=True, help="Link to wiki page")
parser.add_argument("--depth", type=int, default=3, help="Depth for walking from url")
parser.add_argument("--out_json", required=True,help="Name of output json")
args = parser.parse_args()
print(f"URL: {args.url}, Depth: {args.depth}, Output JSON: {args.out_json}")

print("Crawling Wikipedia...")
res = walk_on_depth(args.url, args.depth)
print(*res, sep="\n")
with open(args.out_json, "w", encoding="utf-8") as out:
    json.dump(res, out)