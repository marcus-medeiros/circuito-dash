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
V = 220
f = 60

def bloco(ax, x, y, w=1.0, h=0.2, label="", rot=0):
    # Cria retângulo
    rect = plt.Rectangle((x, y-h/2), w, h, fill=False, edgecolor="black", lw=2)
    
    if rot != 0:
        # Rotaciona o retângulo em torno do centro
        t = transforms.Affine2D().rotate_deg_around(x + w/2, y, rot) + ax.transData
        rect.set_transform(t)
    
    ax.add_patch(rect)
    
    # Adiciona texto rotacionado
    ax.text(x + w/2, y + h, label, ha="center", va="bottom", fontsize=10, rotation=rot)
    
    # Linhas de entrada e saída (não rotacionadas, pois geralmente são horizontais)
    ax.plot([x - w*0.2, x], [y, y], color="black", lw=2)   # entrada
    ax.plot([x + w, x + w + w*0.2], [y, y], color="black", lw=2)  # saída


# Criar figura
fig, ax = plt.subplots(figsize=(7,6))
ax.axis("off")

# Fonte
ax.plot([0,0],[0,4], color="black", lw=0)
ax.text(0.0, 1, f"V = {V} V\n  {f} Hz", va="center", ha="left")

# Série
bloco(ax, 0, 3, w=1, label=f"{z1} Ω")
bloco(ax, 2, 3, w=1, label=z2)

ax.plot([3,4],[3,3], color="red", lw=2)

# Nó superior
ax.plot([4,4],[3,2.8], color="red", lw=2)

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
