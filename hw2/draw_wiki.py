import json
import networkx as nx
import matplotlib.pyplot as plt  # только для цветовой карты, можно и без неё

# 1. Загружаем данные (пример: из переменной или файла)
with open("/home/lerathebest/Documents/Programming/Orchestration_hw/hw2/wiki_links_from_guar.json", "r", encoding="utf-8") as inp:
    data = json.load(inp)

# 2. Создаём ориентированный граф
G = nx.DiGraph()
for source, targets in data.items():
    for target in targets:
        G.add_edge(source, target)

# 3. Фильтрация узлов
threshold = 5
nodes_to_keep = [node for node in G.nodes() if G.degree(node) >= threshold]
print(f"Всего узлов: {G.number_of_nodes()}, после фильтрации: {len(nodes_to_keep)}")

# Создаём подграф
G_sub = G.subgraph(nodes_to_keep).copy() 

# 4. Вычисляем координаты узлов
pos = nx.spring_layout(G_sub, k=1.5, iterations=50, seed=42)  # k регулирует расстояние

# 5. Рисование с помощью matplotlib
plt.figure(figsize=(16, 10))

labels = {node: node.replace('_', ' ') for node in G_sub.nodes()}
nx.draw(G_sub, pos, labels=labels, node_size=500, font_size=8, arrows=True)
plt.axis('off')
plt.savefig('draw_wiki_graph.png', dpi=600)
plt.show()