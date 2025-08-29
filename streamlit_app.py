import streamlit as st
import matplotlib.pyplot as plt

st.title("🔋 Montagem de Circuitos Elétricos com Matplotlib")

# Sidebar para escolher elementos
resistores = st.sidebar.slider("Quantidade de Resistores", 0, 3, 2)
capacitores = st.sidebar.slider("Quantidade de Capacitores", 0, 2, 1)
fonte = st.sidebar.selectbox("Fonte", ["Nenhuma", "VCC", "AC"])

fig, ax = plt.subplots(figsize=(6,4))
ax.set_xlim(0,10)
ax.set_ylim(0,6)
ax.axis("off")

x = 1
y = 3

# Desenhar a fonte
if fonte == "VCC":
    ax.plot([x, x], [y-1, y+1], color="red", lw=2)
    ax.text(x-0.3, y+1.2, "VCC", color="red")
elif fonte == "AC":
    circ = plt.Circle((x, y), 0.5, fill=False, color="blue", lw=2)
    ax.add_patch(circ)
    ax.text(x-0.3, y+1.2, "AC", color="blue")
x += 2

# Resistores
for i in range(resistores):
    ax.plot([x, x+2], [y, y], color="black", lw=2)
    ax.text(x+1, y+0.3, f"R{i+1}")
    x += 2

# Capacitores
for i in range(capacitores):
    ax.plot([x, x], [y-0.5, y+0.5], color="black", lw=2)
    ax.plot([x+0.5, x+0.5], [y-0.5, y+0.5], color="black", lw=2)
    ax.text(x+0.25, y+0.7, f"C{i+1}")
    x += 2

# Fechar o circuito (linha de retorno)
ax.plot([x, x], [y, 1], color="black", lw=2)
ax.plot([x, 1], [1, 1], color="black", lw=2)
ax.plot([1, 1], [1, y], color="black", lw=2)

st.pyplot(fig)
