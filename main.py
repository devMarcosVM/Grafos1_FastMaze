import streamlit as st
import numpy as np
from collections import deque
import time
import random
from PIL import Image

st.set_page_config(layout="wide")
st.title("🧭 Labirinto com BFS e DFS - Comparação")

# Configurações
HEIGHT, WIDTH = 25, 25
WHITE = [255, 255, 255]
BLACK = [0, 0, 0]
RED = [255, 0, 0]      # Início
BLUE = [0, 0, 255]     # Fim
GREEN = [0, 255, 0]    # BFS
PURPLE = [128, 0, 128] # DFS
YELLOW = [255, 255, 0] # Exploração
GRAY = [200, 200, 200] # Fronteira

# Inicialização
if "maze" not in st.session_state:
    st.session_state.maze = np.ones((HEIGHT, WIDTH, 3), dtype=np.uint8) * 255
    st.session_state.bfs_path = None
    st.session_state.dfs_path = None
    st.session_state.explored = set()
    st.session_state.frontier = set()
    st.session_state.img_placeholder = None
    st.session_state.current_algorithm = None
    st.session_state.start_pos = (0, 0)
    st.session_state.end_pos = (HEIGHT-1, WIDTH-1)
    st.session_state.start_y = 0
    st.session_state.start_x = 0
    st.session_state.end_y = HEIGHT-1
    st.session_state.end_x = WIDTH-1

def generate_maze():
    maze = np.ones((HEIGHT, WIDTH, 3), dtype=np.uint8) * 255
    for i in range(HEIGHT):
        for j in range(WIDTH):
            if random.random() < 0.3:  # 30% obstáculos
                maze[i, j] = BLACK
    
    # Garantir que as posições iniciais e finais estejam livres
    maze[st.session_state.start_pos] = WHITE
    maze[st.session_state.end_pos] = WHITE
    
    st.session_state.bfs_path = None
    st.session_state.dfs_path = None
    st.session_state.explored = set()
    st.session_state.frontier = set()
    st.session_state.current_algorithm = None
    return maze

def render_maze(maze, start, end, explored=None, frontier=None, bfs_path=None, dfs_path=None):
    display_maze = maze.copy()
    
    if frontier:
        for y, x in frontier:
            if (y, x) != start and (y, x) != end:
                display_maze[y, x] = GRAY
    
    if explored:
        for y, x in explored:
            if (y, x) != start and (y, x) != end:
                display_maze[y, x] = YELLOW
    
    if dfs_path:
        for y, x in dfs_path:
            if (y, x) != start and (y, x) != end:
                display_maze[y, x] = PURPLE
    if bfs_path:
        for y, x in bfs_path:
            if (y, x) != start and (y, x) != end:
                display_maze[y, x] = GREEN
    
    # Aplicar cores para início e fim
    display_maze[start[0], start[1]] = RED
    display_maze[end[0], end[1]] = BLUE
    
    img = Image.fromarray(display_maze, mode="RGB")
    img = img.resize((600, 600), resample=Image.NEAREST)
    return img

def update_positions():
    # Atualiza as posições apenas se os valores forem diferentes
    new_start_pos = (st.session_state.start_y, st.session_state.start_x)
    new_end_pos = (st.session_state.end_y, st.session_state.end_x)
    
    if new_start_pos != st.session_state.start_pos:
        st.session_state.start_pos = new_start_pos
    
    if new_end_pos != st.session_state.end_pos:
        st.session_state.end_pos = new_end_pos
    
    render_and_display()

def render_and_display():
    img = render_maze(
        st.session_state.maze, 
        st.session_state.start_pos, 
        st.session_state.end_pos, 
        st.session_state.explored, 
        st.session_state.frontier,
        st.session_state.bfs_path,
        st.session_state.dfs_path
    )
    st.session_state.img_placeholder.image(img, caption="Labirinto")

def is_accessible(maze, start, end):
    visited = set()
    queue = deque([start])
    
    while queue:
        current = queue.popleft()
        if current == end:
            return True
        if current in visited:
            continue
        visited.add(current)
        
        x, y = current
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < HEIGHT and 0 <= ny < WIDTH and not np.array_equal(maze[nx, ny], BLACK):
                queue.append((nx, ny))
    return False

def solve_bfs(start, end, speed):
    maze = st.session_state.maze
    graph = build_graph(maze)
    queue = deque([(start, [start])])
    visited = set()
    explored = set()
    frontier = set([start])
    st.session_state.current_algorithm = "BFS"
    
    while queue:
        current, path = queue.popleft()
        
        if current in frontier:
            frontier.remove(current)
        
        if current == end:
            st.session_state.bfs_path = path
            st.session_state.explored = explored
            st.session_state.frontier = set()
            return path
        
        if current in visited:
            continue
        
        visited.add(current)
        explored.add(current)
        
        for neighbor in graph.get(current, []):
            if neighbor not in visited:
                frontier.add(neighbor)
        
        img = render_maze(maze, start, end, explored, frontier, st.session_state.bfs_path, st.session_state.dfs_path)
        st.session_state.img_placeholder.image(img, caption="Explorando com BFS...")
        time.sleep(speed)
        
        for neighbor in graph.get(current, []):
            if neighbor not in visited:
                queue.append((neighbor, path + [neighbor]))
    
    return None

def solve_dfs(start, end, speed):
    maze = st.session_state.maze
    graph = build_graph(maze)
    stack = [(start, [start])]
    visited = set()
    explored = set()
    frontier = set([start])
    st.session_state.current_algorithm = "DFS"
    
    while stack:
        current, path = stack.pop()
        
        if current in frontier:
            frontier.remove(current)
        
        if current == end:
            st.session_state.dfs_path = path
            st.session_state.explored = explored
            st.session_state.frontier = set()
            return path
        
        if current in visited:
            continue
        
        visited.add(current)
        explored.add(current)
        
        for neighbor in reversed(graph.get(current, [])):
            if neighbor not in visited:
                frontier.add(neighbor)
        
        img = render_maze(maze, start, end, explored, frontier, st.session_state.bfs_path, st.session_state.dfs_path)
        st.session_state.img_placeholder.image(img, caption="Explorando com DFS...")
        time.sleep(speed)
        
        for neighbor in reversed(graph.get(current, [])):
            if neighbor not in visited:
                stack.append((neighbor, path + [neighbor]))
    
    return None

def build_graph(maze):
    graph = {}
    for i in range(HEIGHT):
        for j in range(WIDTH):
            if np.array_equal(maze[i, j], BLACK):
                continue
            neighbors = []
            for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                ni, nj = i + dy, j + dx
                if 0 <= ni < HEIGHT and 0 <= nj < WIDTH and not np.array_equal(maze[ni, nj], BLACK):
                    neighbors.append((ni, nj))
            graph[(i, j)] = neighbors
    return graph

# Layout principal
col1, col2 = st.columns([1, 1.5])

with col1:
    # Inicialização do labirinto
    if "maze" not in st.session_state:
        st.session_state.maze = generate_maze()
    
    # Renderização inicial
    st.session_state.img_placeholder = st.empty()
    render_and_display()

with col2:
    st.header("Controles")
    
    # Configurações de posição
    st.subheader("Posições")
    st.number_input("Linha inicial", min_value=0, max_value=HEIGHT-1, 
                  value=st.session_state.start_y, key="start_y",
                  on_change=update_positions)
    st.number_input("Coluna inicial", min_value=0, max_value=WIDTH-1, 
                  value=st.session_state.start_x, key="start_x",
                  on_change=update_positions)
    st.number_input("Linha final", min_value=0, max_value=HEIGHT-1, 
                  value=st.session_state.end_y, key="end_y",
                  on_change=update_positions)
    st.number_input("Coluna final", min_value=0, max_value=WIDTH-1, 
                  value=st.session_state.end_x, key="end_x",
                  on_change=update_positions)
    
    # Configurações de velocidade
    st.subheader("Configurações")
    speed = st.slider("Velocidade da animação (segundos por passo)", 0.01, 1.0, 0.1, 0.01)
    
    # Botões de controle
    st.subheader("Ações")
    if st.button("🔍 Resolver com BFS"):
        if not is_accessible(st.session_state.maze, st.session_state.start_pos, st.session_state.end_pos):
            st.error("Ponto final não acessível!")
        else:
            path = solve_bfs(st.session_state.start_pos, st.session_state.end_pos, speed)
            if path:
                render_and_display()
            else:
                st.error("Caminho não encontrado!")

    if st.button("🔍 Resolver com DFS"):
        if not is_accessible(st.session_state.maze, st.session_state.start_pos, st.session_state.end_pos):
            st.error("Ponto final não acessível!")
        else:
            path = solve_dfs(st.session_state.start_pos, st.session_state.end_pos, speed)
            if path:
                render_and_display()
            else:
                st.error("Caminho não encontrado!")

    if st.button("🔄 Novo Labirinto"):
        st.session_state.maze = generate_maze()
        render_and_display()
    
    # Legenda
    st.subheader("Legenda")
    st.markdown("""
    - 🔴 Vermelho: Ponto de início
    - 🔵 Azul: Ponto final
    - 🟡 Amarelo: Células exploradas
    - ⚪ Cinza: Fronteira (próximas a explorar)
    - 🟢 Verde: Caminho BFS
    - 🟣 Roxo: Caminho DFS
    - ⬛ Preto: Obstáculos
    """)