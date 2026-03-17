import requests
import re
from bs4 import BeautifulSoup

headers = {"User-Agent": "Mozilla/5.0"}
start_article = "https://en.wikipedia.org/wiki/American_Revolutionary_War"
r = requests.get(start_article, headers=headers)

#print("Status code:", r.status_code)
#print("First 500 characters of response:\n", r.text[:500])

bs = BeautifulSoup(r.text, "html.parser")
base_url = "https://en.wikipedia.org"
pattern = re.compile(r"^(/wiki/)((?!:).)*$")
content = bs.find("div", id="bodyContent")

res = {}

for link in content.find_all("a", href=pattern):
    node = link["href"]
    res[node] = dict()

