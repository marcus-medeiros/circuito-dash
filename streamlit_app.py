import math
import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx

st.set_page_config(page_title="Topologia de Transformador", page_icon="🔌", layout="centered")
st.title("🔌 Topologia de Transformador")

# ======================
# Painel lateral (inputs)
# ======================
modo = st.sidebar.radio("Modo de visualização", ["Esquemático", "Grafo"])

tipo = st.sidebar.selectbox("Tipo", ["Monofásico", "Trifásico"])

if tipo == "Trifásico":
    prim = st.sidebar.selectbox("Ligação Primário", ["Y", "Δ"])
    sec = st.sidebar.selectbox("Ligação Secundário", ["Y", "Δ", "Zig-Zag (Yz)"])
    neutro_prim = st.sidebar.checkbox("Neutro no Primário (se Y)", value=True)
    neutro_sec = st.sidebar.checkbox("Neutro no Secundário (se Y/Zig-Zag)", value=True)
else:  # Monofásico
    prim = "Série"
    sec = st.sidebar.selectbox("Config. Secundário", ["Simples", "Tap central (CT)"])

tap_pos = st.sidebar.slider("Posição do TAP (±%)", -10, 10, 0, step=1)
mostrar_polaridade = st.sidebar.checkbox("Mostrar polaridade (•)", value=True)
mostrar_terra = st.sidebar.checkbox("Mostrar aterramento no neutro", value=True if tipo=="Trifásico" else False)
relacao = st.sidebar.text_input("Relação de Espiras (Np:Ns)", "10:1")

# ======================
# Helpers de desenho
# ======================
def draw_core(ax, x=0, y=0, w=2.2, h=3.0, t=0.3):
    # núcleo em C simples
    ax.add_patch(plt.Rectangle((x, y), w, h, fill=False, linewidth=2))
    ax.add_patch(plt.Rectangle((x+t, y+t), w-2*t, h-2*t, fill=False, linewidth=2))

def draw_coil(ax, cx, y1, y2, turns=6, label="", polarity=False, side="left"):
    # bobina como arcos
    r = 0.18
    ys = [y1 + i*(y2-y1)/turns for i in range(turns)]
    for y in ys:
        theta = [i/40*math.pi for i in range(41)]
        if side == "left":
            xs = [cx - r*math.cos(t) for t in theta]
        else:
            xs = [cx + r*math.cos(t) for t in theta]
        ys_ = [y + r*math.sin(t) for t in theta]
        ax.plot(xs, ys_, linewidth=2)

    if label:
        ax.text(cx + (0.45 if side=="right" else -0.45), (y1+y2)/2, label,
                ha="center", va="center", fontsize=11, bbox=dict(boxstyle="round,pad=0.2", fc="w", ec="0.6"))

    if polarity:
        ax.plot([cx + (0.42 if side=="right" else -0.42)], [(y2-0.15)],
                marker="o", markersize=5)

def draw_terminal(ax, x, y, name=None):
    ax.plot([x-0.2, x], [y, y], linewidth=2)
    ax.plot(x, y, marker="o")
    if name:
        ax.text(x+0.1, y, name, va="center", fontsize=10)

def draw_ground(ax, x, y):
    ax.plot([x, x], [y, y-0.25], linewidth=2)
    ax.plot([x-0.2, x+0.2], [y-0.25, y-0.25], linewidth=2)
    ax.plot([x-0.15, x+0.15], [y-0.32, y-0.32], linewidth=2)
    ax.plot([x-0.1, x+0.1], [y-0.39, y-0.39], linewidth=2)

def draw_tap(ax, x, y, label):
    ax.plot([x, x+0.5], [y, y], linestyle="--")
    ax.text(x+0.55, y, label, va="center", fontsize=9)

# ======================
# Esquemático
# ======================
def view_monofasico():
    fig, ax = plt.subplots(figsize=(7,5))
    ax.axis("off")
    ax.set_xlim(-4, 6.5)
    ax.set_ylim(-2, 5)

    # Núcleo
    draw_core(ax, x=-1.2, y=0.1, w=2.4, h=3.6, t=0.35)

    # Primário (esq)
    draw_coil(ax, cx=-1.5, y1=0.6, y2=3.2, turns=8, label="Nₚ", polarity=mostrar_polaridade, side="left")
    draw_terminal(ax, x=-3.0, y=3.0, name="P1")
    draw_terminal(ax, x=-3.0, y=0.8, name="P2")
    ax.plot([-3.0, -1.7], [3.0, 3.0], linewidth=2)
    ax.plot([-3.0, -1.7], [0.8, 0.8], linewidth=2)

    # Secundário (dir)
    draw_coil(ax, cx=1.2, y1=0.6, y2=3.2, turns=8, label="Nₛ", polarity=mostrar_polaridade, side="right")
    if sec == "Tap central (CT)":
        # terminais S1, CT, S2
        y_top, y_bot = 3.0, 0.8
        y_ct = (y_top + y_bot)/2
        draw_terminal(ax, x=3.0, y=y_top, name="S1")
        draw_terminal(ax, x=3.0, y=y_ct, name="CT")
        draw_terminal(ax, x=3.0, y=y_bot, name="S2")
        ax.plot([1.4, 3.0], [y_top, y_top], linewidth=2)
        ax.plot([1.4, 3.0], [y_ct, y_ct], linewidth=2)
        ax.plot([1.4, 3.0], [y_bot, y_bot], linewidth=2)
    else:
        draw_terminal(ax, x=3.0, y=3.0, name="S1")
        draw_terminal(ax, x=3.0, y=0.8, name="S2")
        ax.plot([1.4, 3.0], [3.0, 3.0], linewidth=2)
        ax.plot([1.4, 3.0], [0.8, 0.8], linewidth=2)

    # TAP (indicativo de posição)
    if tap_pos != 0:
        draw_tap(ax, x=-2.8, y=3.4, label=f"TAP {tap_pos:+d}%")

    # Relação
    ax.text(-3.0, 4.2, f"Relação Np:Ns = {relacao}", fontsize=11)

    st.pyplot(fig)

def _phase_coords(cx, cy, r, n):
    # posições circulares para 3 bobinas
    return [(cx + r*math.cos(2*math.pi*i/n + math.pi/2),
             cy + r*math.sin(2*math.pi*i/n + math.pi/2)) for i in range(n)]

def draw_phase_set(ax, centers, label_set, connection, side="left", polarity=False):
    # Desenha 3 bobinas com ligação Y/Δ/Zig-Zag simples
    # centers: list of (cx,cy) for A,B,C
    names = ["A", "B", "C"]
    terminals = {}

    # Desenho das 3 bobinas (uma por fase)
    for (cx, cy), ph in zip(centers, names):
        draw_coil(ax, cx=cx, y1=cy-0.6, y2=cy+0.6, turns=6, label=f"{label_set}{ph}", polarity=polarity, side=side)
        # terminais de cada bobina
        if side == "left":
            t1 = (cx-1.6, cy+0.5)
            t2 = (cx-1.6, cy-0.5)
        else:
            t1 = (cx+1.6, cy+0.5)
            t2 = (cx+1.6, cy-0.5)
        terminals[ph] = (t1, t2)
        draw_terminal(ax, *t1, name=f"{label_set}{ph}1")
        draw_terminal(ax, *t2, name=f"{label_set}{ph}2")
        ax.plot([t1[0], cx-(0.4 if side=="left" else -0.4)], [t1[1], cy+0.5], linewidth=2)
        ax.plot([t2[0], cx-(0.4 if side=="left" else -0.4)], [t2[1], cy-0.5], linewidth=2)

    # Conexão
    if connection == "Y":
        # une um lado das 3 bobinas no neutro
        # usar o "2" como neutro
        neutro_x = sum([terminals[p][1][0] for p in names])/3 - (0.4 if side=="left" else -0.4)
        neutro_y = sum([terminals[p][1][1] for p in names])/3 - 1.1
        for p in names:
            x2 = terminals[p][1][0] - (0.4 if side=="left" else -0.4)
            y2 = terminals[p][1][1]
            ax.plot([x2, neutro_x], [y2, neutro_y], linewidth=2)
        # terminal neutro
        draw_terminal(ax, neutro_x+(-0.2 if side=="left" else 0.2), neutro_y, name=f"{label_set}N")
        if mostrar_terra:
            draw_ground(ax, neutro_x+(-0.2 if side=="left" else 0.2), neutro_y-0.05)
    elif connection == "Δ":
        # liga em triângulo usando os terminais "1" ↔ "2" da próxima fase
        seq = ["A", "B", "C"]
        for i in range(3):
            p = seq[i]
            q = seq[(i+1)%3]
            p1 = terminals[p][0]  # p1
            q2 = terminals[q][1]  # q2
            ax.plot([p1[0], q2[0]], [p1[1], q2[1]], linewidth=2)
    elif connection.startswith("Zig-Zag"):
        # simplificação: conecte metade de cada fase ao neutro comum
        neutro_x = sum([terminals[p][1][0] for p in names])/3 - (0.4 if side=="left" else -0.4)
        neutro_y = sum([terminals[p][1][1] for p in names])/3 - 1.1
        for p in names:
            x2 = terminals[p][1][0] - (0.4 if side=="left" else -0.4)
            y2 = terminals[p][1][1]
            ax.plot([x2, neutro_x], [y2, neutro_y], linewidth=2)
        draw_terminal(ax, neutro_x+(-0.2 if side=="left" else 0.2), neutro_y, name=f"{label_set}N")
        if mostrar_terra:
            draw_ground(ax, neutro_x+(-0.2 if side=="left" else 0.2), neutro_y-0.05)

def view_trifasico():
    fig, ax = plt.subplots(figsize=(9,6))
    ax.axis("off")
    ax.set_xlim(-10, 10)
    ax.set_ylim(-6, 6)

    # Núcleos (três colunas)
    for x in [-3, 0, 3]:
        draw_core(ax, x=x-1.0, y=-2.2, w=2.0, h=4.4, t=0.25)

    # Centros das fases (primário à esquerda, secundário à direita)
    centers_prim = [(-4.5, 2.5), (-1.5, 2.5), (1.5, 2.5)]
    centers_sec  = [(4.5, 2.5), (1.5, 0.0), (7.5, 0.0)]  # só para espaçar bem no desenho
    # Ajustar para linhas retas num layout mais limpo
    centers_prim = [(-4.5, 2.5), (-1.5, 0.0), (-4.5, -2.5)]
    centers_sec  = [(4.5, 2.5), (1.5, 0.0), (4.5, -2.5)]

    # Primário
    draw_phase_set(ax, centers_prim, label_set="P", connection=prim, side="left", polarity=mostrar_polaridade)
    if prim == "Y" and neutro_prim:
        ax.text(-6.5, 4.5, "Primário Y com Neutro", fontsize=11)

    # Secundário
    sec_conn = sec if sec != "Zig-Zag (Yz)" else "Zig-Zag"
    draw_phase_set(ax, centers_sec, label_set="S", connection=sec_conn, side="right", polarity=mostrar_polaridade)
    if (sec.startswith("Y") or sec.startswith("Zig-Zag")) and neutro_sec:
        ax.text(6.0, 4.5, "Secundário com Neutro", fontsize=11)

    # TAP indicador
    if tap_pos != 0:
        ax.text(0, 5.0, f"TAP {tap_pos:+d}%", ha="center", fontsize=12)

    # Relação
    ax.text(0, -5.3, f"Relação Np:Ns = {relacao}", ha="center", fontsize=11)

    st.pyplot(fig)

# ======================
# Grafo (topologia elétrica)
# ======================
def view_graph_monofasico():
    G = nx.Graph()
    # nós
    G.add_nodes_from(["P1","P2","S1","S2"])
    # arestas (núcleo não conduz, representamos apenas acoplamento por rótulo)
    G.add_edge("P1","P2", kind="winding_P")
    G.add_edge("S1","S2", kind="winding_S")
    pos = {"P1":(-1,1),"P2":(-1,-1),"S1":(1,1),"S2":(1,-1)}
    fig, ax = plt.subplots(figsize=(5,4))
    nx.draw(G, pos, with_labels=True, ax=ax)
    ax.set_title("Grafo da Topologia (Monofásico)")
    st.pyplot(fig)

def view_graph_trifasico():
    G = nx.Graph()
    phases = ["A","B","C"]
    # Primário
    if prim == "Y":
        G.add_node("NP")
        for ph in phases:
            G.add_edge(f"P{ph}1","P{ph}2")
            G.add_edge(f"P{ph}2","NP")
    elif prim == "Δ":
        for ph in phases:
            G.add_edge(f"P{ph}1", f"P{ph}2")
        # fechar delta: A2-B1, B2-C1, C2-A1
        G.add_edge("PA2","PB1"); G.add_edge("PB2","PC1"); G.add_edge("PC2","PA1")

    # Secundário
    if sec.startswith("Y"):
        G.add_node("NS")
        for ph in phases:
            G.add_edge(f"S{ph}1","S{ph}2")
            G.add_edge(f"S{ph}2","NS")
    elif sec.startswith("Δ"):
        for ph in phases:
            G.add_edge(f"S{ph}1", f"S{ph}2")
        G.add_edge("SA2","SB1"); G.add_edge("SB2","SC1"); G.add_edge("SC2","SA1")
    else:  # Zig-Zag simplificado como Y
        G.add_node("NS")
        for ph in phases:
            G.add_edge(f"S{ph}1","S{ph}2"); G.add_edge(f"S{ph}2","NS")

    # posições aproximadas
    pos = {f"P{ph}1":(-3, 2-2*i) for i,ph in enumerate(phases)}
    pos.update({f"P{ph}2":(-2, 2-2*i) for i,ph in enumerate(phases)})
    pos.update({f"S{ph}1":(2, 2-2*i) for i,ph in enumerate(phases)})
    pos.update({f"S{ph}2":(3, 2-2*i) for i,ph in enumerate(phases)})
    if "NP" in G.nodes: pos["NP"]=(-2.5, -4)
    if "NS" in G.nodes: pos["NS"]=(2.5, -4)

    fig, ax = plt.subplots(figsize=(7,5))
    nx.draw(G, pos, with_labels=True, ax=ax)
    ax.set_title("Grafo da Topologia (Trifásico)")
    st.pyplot(fig)

# ======================
# Render conforme escolhas
# ======================
if modo == "Esquemático":
    if tipo == "Monofásico":
        view_monofasico()
    else:
        view_trifasico()
else:
    if tipo == "Monofásico":
        view_graph_monofasico()
    else:
        view_graph_trifasico()

# rodapé
st.caption("Dica: a vista em grafo representa apenas a conectividade elétrica; o núcleo magnético é indicado no esquemático.")
