import json
import networkx as nx
import plotly.graph_objects as go
import matplotlib.pyplot as plt  # только для цветовой карты, можно и без неё

# 1. Загружаем данные (пример: из переменной или файла)
with open("/home/lerathebest/Documents/Programming/net_graph_AB.json", "r", encoding="utf-8") as inp:
    data = json.load(inp)

# Если данные сохранены в JSON-файле:
# with open("net_graph_ABC.json", "r", encoding="utf-8") as f:
#     data = json.load(f)

# 2. Создаём ориентированный граф NetworkX
G = nx.DiGraph()
for source, targets in data.items():
    for target in targets:
        G.add_edge(source, target)

# 3. Фильтрация узлов (оставляем только те, у которых степень >= порога)
#    Порог можно подобрать экспериментально (например, 3 или 5)
threshold = 3
nodes_to_keep = [node for node in G.nodes() if G.degree(node) >= threshold]
print(f"Всего узлов: {G.number_of_nodes()}, после фильтрации: {len(nodes_to_keep)}")

# Создаём подграф
G_sub = G.subgraph(nodes_to_keep).copy()  # .copy() чтобы не было проблем с layout

# Если подграф слишком мал, можно уменьшить порог или убрать фильтрацию
if G_sub.number_of_nodes() == 0:
    print("Порог слишком высок, использую все узлы.")
    G_sub = G

# 4. Вычисляем координаты узлов (2D-компоновка)
pos = nx.spring_layout(G_sub, k=1.5, iterations=50, seed=42)  # k регулирует расстояние

# 5. Подготовка данных для Plotly
#    Рёбра: создаём список линий (каждое ребро — отдельный отрезок)
edge_trace = []
for edge in G_sub.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    # Добавляем None, чтобы разделить отрезки
    edge_trace.append(go.Scatter(
        x=[x0, x1, None],
        y=[y0, y1, None],
        mode='lines',
        line=dict(color='gray', width=0.8),
        hoverinfo='none',
        showlegend=False
    ))

# Узлы: координаты и подписи
node_x = []
node_y = []
node_text = []
for node in G_sub.nodes():
    x, y = pos[node]
    node_x.append(x)
    node_y.append(y)
    node_text.append(node)

# Цвет узлов можно сделать зависящим от степени (например, от количества связей)
# Для этого используем колорбар или просто зададим один цвет
node_degrees = [G_sub.degree(node) for node in G_sub.nodes()]
# Нормируем для цветовой шкалы (опционально)
node_colors = node_degrees

node_trace = go.Scatter(
    x=node_x,
    y=node_y,
    mode='markers+text',
    marker=dict(
        size=8,
        color=node_colors,
        colorscale='Viridis',
        showscale=True,
        colorbar=dict(title="Степень узла")
    ),
    text=node_text,
    textposition="top center",
    textfont=dict(size=8),
    hoverinfo='text',
    showlegend=False
)

# 6. Сборка фигуры
fig = go.Figure(data=edge_trace + [node_trace])

# Настройка внешнего вида
fig.update_layout(
    title='Граф ссылок между статьями Википедии (интерактивная версия)',
    title_font_size=16,
    showlegend=False,
    hovermode='closest',
    margin=dict(b=20, l=5, r=5, t=40),
    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    width=1800,
    height=900
)

# 7. Отображение в браузере
fig.show()

# Для сохранения в HTML (можно открыть без запуска Python):
# fig.write_html("graph_plotly.html")