import streamlit as st
import matplotlib.pyplot as plt

st.title("🔌 Diagrama de Circuito com Impedâncias (Blocos Retangulares)")

# Entradas do usuário
z1 = st.text_input("Impedância série 1", "1kΩ")
z2 = st.text_input("Impedância série 2", "1H")
z3 = st.text_input("Impedância paralelo (ramo superior 1)", "1H")
z4 = st.text_input("Impedância paralelo (ramo superior 2)", "1kΩ")
z5 = st.text_input("Impedância paralelo (ramo inferior 1)", "1H")
z6 = st.text_input("Impedância paralelo (ramo inferior 2)", "1kΩ")
V = 220;

def bloco(ax, x, y, w=1.0, h=0.4, label=""):
    rect = plt.Rectangle((x, y-h/2), w, h, fill=False, edgecolor="black", lw=2)
    ax.add_patch(rect)
    ax.text(x+w/2, y+h, label, ha="center", va="bottom", fontsize=10)
    ax.plot([x-w*0.2, x],[y, y], color="black", lw=2) # entrada
    ax.plot([x+w, x+w+w*0.2],[y, y], color="black", lw=2) # saída

# Criar figura
fig, ax = plt.subplots(figsize=(7,6))
ax.axis("off")

# Fonte
ax.plot([0,0],[0,2], color="black", lw=0)
ax.text(0.0,1,"V = {V}, 60Hz", va="center")

# Série
bloco(ax, 0, 2, w=1.5, label=z1)
bloco(ax, 2, 2, w=1.5, label=z2)

# Nó superior
ax.plot([3.5,3.5],[2,3], color="black", lw=2)

# Ramo paralelo (cima)
bloco(ax, 3.5, 3, w=1.5, label=z3)
bloco(ax, 5.2, 3, w=1.5, label=z4)
ax.plot([6.7,6.7],[3,2.5], color="black", lw=2)

# Ramo paralelo (baixo)
bloco(ax, 3.5, 2, w=1.5, label=z5)
bloco(ax, 5.2, 2, w=1.5, label=z6)

# Fechar circuito
ax.plot([6.7,6.7],[2,0], color="black", lw=2)
ax.plot([6.7,0],[0,0], color="black", lw=2)

ax.set_xlim(-1,8)
ax.set_ylim(-1,4)

st.pyplot(fig)
