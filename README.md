# Grafos1_FastMaze

**Número da Lista**: X<br>
**Conteúdo da Disciplina**: Grafos 1<br>

## Alunos
|Matrícula | Aluno |
| -- | -- |
| 22/2021890  |  Manuella Magalhães Valadares |
| 22/2021906  |  Marcos Vieira Marinho |

## ℹ️ Sobre o Fast Maze
Fast Maze é um jogo de labirinto que permite visualizar e comparar o desempenho dos algoritmos BFS (Busca em Largura) e DFS (Busca em Profundidade) na busca por um caminho até o alvo.

O labirinto começa em branco, possibilitando que você observe o funcionamento dos algoritmos em um ambiente livre de obstáculos. Também é possível carregar diferentes labirintos para testar como cada algoritmo se comporta em cenários variados.

Você pode definir manualmente a posição inicial e o alvo, tornando o jogo personalizável, assim como a velocidade que o algoritmo vai rodar. As cores exibidas seguem uma legenda pré-dedfinida, facilitando a compreensão do trajeto percorrido e da eficiência de cada algoritmo durante a busca.

## Screenshots
#### Labirinto em branco
![Captura de tela de 2025-04-17 21-01-49](https://github.com/user-attachments/assets/626955e9-43dd-4c8c-b56a-c47d0c2f042b)
#### Resultado DFS
![Captura de tela de 2025-04-17 21-14-30](https://github.com/user-attachments/assets/d6d3da1b-3d0c-498d-b99a-38c5a97abd4b)
#### Resultado BFS
![Captura de tela de 2025-04-17 21-14-55](https://github.com/user-attachments/assets/f3cee539-3909-4e26-bf4f-09398dbf69ec)
#### Legenda de cores 
![Captura de tela de 2025-04-17 21-01-25](https://github.com/user-attachments/assets/0e8dce95-6526-4615-8f9a-8f665b69ea31)



## Instalação 
**Linguagem**: Python<br>
**Framework**: Streamlit<br>
**Pré-requisitos**: Python 3.8+

1. **Clone o repositório:**
```bash
git clone https://github.com/projeto-de-algoritmos-2025/Grafos1_FastMaze.git
cd Grafos1_FastMaze
```
2. **Instale as dependências:**
```bash
pip install streamlit numpy pillow
```
## Uso 
Depois de instalar tudo corretamente, execute o seguinte comando no terminal:
```bash
streamlit run main.py
```
### Na interface web:

- Ajuste as posições iniciais e finais do labirinto usando os campos numéricos.

- Defina a velocidade da animação.

- Clique em "🔍 Resolver com BFS" ou "🔍 Resolver com DFS" para visualizar os algoritmos em ação.


## Outros 
- O labirinto é gerado de forma **aleatória** a cada execução da aplicação.

- Caso não exista um caminho acessível entre o início e o fim, será exibida uma mensagem de erro.
