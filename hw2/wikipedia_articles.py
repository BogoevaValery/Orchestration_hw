import re
from collections import deque
import json
import requests
from bs4 import BeautifulSoup

def get_internal_links(base_url, href):
    full_url = requests.compat.urljoin(base_url, href)
    article = requests.get(full_url, headers=my_headers)
    
    print(f"Status code: {article.status_code}")
    
    bs = BeautifulSoup(article.text, "html.parser")
    #pattern = re.compile(r"^(/wiki/)[A,B,C]")  #((?!:).)*$")
    #pattern = re.compile(r"^(/wiki/)((?!:).)*$")
    pattern = re.compile(r"^/wiki/([AB].*)") #((?!:).*)$")
    content = bs.find("div", id="bodyContent")
    
    res = []
    for link in content.find_all("a", href=pattern):
        href = link["href"]
        match = pattern.match(href)
        if match:
            article = match.group(1)
            res.append(article)
    
    return list(set(res))


my_headers = {"User-Agent": "Mozilla/5.0"}
start_article = "https://en.wikipedia.org/wiki/American_Revolutionary_War"

#links = get_internal_links("https://en.wikipedia.org/", "wiki/American_Revolutionary_War")
#print(*links, sep="\n")

depth = 3

def walk_on_depth(base_url, src, max_depth):
    visited = set()       # уже обработанные страницы
    graph = {}            # результат: страница -> список ссылок
    queue = deque()       # очередь для BFS: (относительный_путь, глубина)
    queue.append((src, 0))

    while queue:
        current, depth = queue.popleft()   # извлекаем слева (FIFO)
        if current in visited:
            continue

        print(f"Обрабатываем {current} (глубина {depth})")
        links = get_internal_links(base_url, current)
        graph[current] = links
        visited.add(current)

        # Если не достигли максимальной глубины, добавляем ссылки в очередь
        if depth < max_depth:
            for link in links:
                if link not in visited:
                    queue.append((link, depth + 1))

        

    return graph

res = walk_on_depth("https://en.wikipedia.org/wiki/", "Guar", 2)
print(*res, sep="\n")
with open("net_graph_AB.json", "w", encoding="utf-8") as out:
    json.dump(res, out)