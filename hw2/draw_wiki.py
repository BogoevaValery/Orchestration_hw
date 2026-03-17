import json
import networkx as nx
import matplotlib.pyplot as plt

# Ваши данные (можно загрузить из файла или использовать переменную)
with open("/home/lerathebest/Documents/Programming/net_graph_AB.json", "r", encoding="utf-8") as inp:
    data = json.load(inp)

# Создаём ориентированный граф (если ссылки направленные)
G = nx.DiGraph()

# Добавляем рёбра: для каждой статьи и каждого её соседа
for source, targets in data.items():
    for target in targets:
        G.add_edge(source, target)

# Визуализация
plt.figure(figsize=(15, 15))  # размер полотна

# Выбираем способ расположения узлов (spring layout хорошо подходит для небольших графов)
pos = nx.spring_layout(G, k=0.5, iterations=50)  # k регулирует расстояние между узлами

# Рисуем узлы и рёбра
nx.draw_networkx_nodes(G, pos, node_size=50, node_color='skyblue', alpha=0.8)
nx.draw_networkx_edges(G, pos, edge_color='gray', arrows=True, arrowsize=10, alpha=0.5)

# Добавляем подписи только для узлов с большой степенью (чтобы не загромождать)
labels = {node: node for node in G.nodes() if G.degree(node) > 1}  # можно настроить порог
nx.draw_networkx_labels(G, pos, labels, font_size=8)

plt.title("Граф ссылок между статьями Википедии")
plt.axis('off')
plt.tight_layout()
plt.show()