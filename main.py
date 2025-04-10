import streamlit as st
import numpy as np
from collections import deque
import time

st.title("🖌️ Paint Bucket BFS animado")


HEIGHT, WIDTH = 100, 100 


if "image" not in st.session_state:
    # Inicia imagem branca
    st.session_state.image = np.ones((HEIGHT, WIDTH, 3), dtype=np.uint8) * 255

    # Desenha um quadrado preto como contorno
    st.session_state.image[25:75, 25] = [0, 0, 0]
    st.session_state.image[25:75, 74] = [0, 0, 0]
    st.session_state.image[25, 25:75] = [0, 0, 0]
    st.session_state.image[74, 25:75] = [0, 0, 0]

image = st.session_state.image

# Mostra imagem
img_placeholder = st.image(image, width=400, caption="Imagem pixelada")

# Cor escolhida
color = st.color_picker("Escolha uma cor para preencher", "#ff0000")
r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)

# Ponto de partida
x = st.number_input("X (coluna)", min_value=0, max_value=WIDTH - 1, step=1)
y = st.number_input("Y (linha)", min_value=0, max_value=HEIGHT - 1, step=1)

# Função para construir o grafo
def build_graph():
    graph = {}
    for i in range(HEIGHT):
        for j in range(WIDTH):
            neighbors = []
            if i > 0: neighbors.append((i-1, j))  # Cima
            if i < HEIGHT - 1: neighbors.append((i+1, j))  # Baixo
            if j > 0: neighbors.append((i, j-1))  # Esquerda
            if j < WIDTH - 1: neighbors.append((i, j+1))  # Direita
            graph[(i, j)] = neighbors
    return graph


def bfs_fill(start_y, start_x, new_color):
    image = st.session_state.image
    graph = build_graph()
    original_color = image[start_y, start_x].tolist()
    # Verifica se a cor original é igual à nova cor ou se é contorno
    # Se for, não faz nada, pq é um contorno
    if original_color == list(new_color) or original_color == [0, 0, 0]:
        return
    
    queue = deque()
    queue.append((start_y, start_x))
    visited = set()
    
    while queue:
        y, x = queue.popleft()
        if (y, x) in visited:
            continue
        visited.add((y, x))
        
        if image[y, x].tolist() == original_color:
            image[y, x] = new_color
            img_placeholder.image(image, width=400, caption="Imagem pixelada")  # Atualiza imagem
            time.sleep(0.02)  # Pequena pausa para efeito visual
            for neighbor in graph[(y, x)]:
                queue.append(neighbor)
    
    st.session_state.image = image

def dfs_fill(start_y, start_x, new_color):
    image = st.session_state.image
    graph = build_graph()
    original_color = image[start_y, start_x].tolist()
    if original_color == list(new_color) or original_color == [0, 0, 0]:  # Não pinta se já for colorido ou for contorno
        return
    
    stack = [(start_y, start_x)]  # Pilha para DFS
    visited = set()
    
    while stack:
        y, x = stack.pop()
        if (y, x) in visited:
            continue
        visited.add((y, x))
        
        if image[y, x].tolist() == original_color:
            image[y, x] = new_color
            img_placeholder.image(image, width=400, caption="Imagem pixelada")  # Atualiza imagem
            time.sleep(0.02)  # Pequena pausa para efeito visual
            for neighbor in graph[(y, x)]:
                stack.append(neighbor)
    
    st.session_state.image = image

# Botão para pintar com bfs
if st.button("Pintar com BFS"):
    bfs_fill(int(y), int(x), [r, g, b])

# Botão para pintar com dfs
if st.button("Pintar com DFS"):
    dfs_fill(int(y), int(x), [r, g, b])