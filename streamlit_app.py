import matplotlib.pyplot as plt

def bloco(ax, x, y, w=1.0, h=0.4, orientation="h", label=""):
    """
    Desenha um bloco retangular representando impedância.
    orientation: "h" horizontal ou "v" vertical
    """
    if orientation == "h":
        rect = plt.Rectangle((x, y-h/2), w, h, fill=False, edgecolor="black", lw=2)
        ax.add_patch(rect)
        ax.text(x+w/2, y+h, label, ha="center", va="bottom", fontsize=10)
        ax.plot([x-w*0.2, x],[y, y], color="black", lw=2) # entrada
        ax.plot([x+w, x+w+w*0.2],[y, y], color="black", lw=2) # saída
    else:
        rect = plt.Rectangle((x-h/2, y-w), h, w, fill=False, edgecolor="black", lw=2)
        ax.add_patch(rect)
        ax.text(x+h, y-w/2, label, va="center", ha="left", fontsize=10)
        ax.plot([x, x],[y, y-w*0.2], color="black", lw=2)
        ax.plot([x, x],[y-w, y-w-w*0.2], color="black", lw=2)

fig, ax = plt.subplots(figsize=(7,6))
ax.axis("off")

# Fonte
ax.plot([0,0],[0,2], color="black", lw=2)
ax.text(-0.4,1,"Fonte\n60Hz", va="center")

# Bloco 1: 1kΩ
bloco(ax, 0, 2, w=1.5, label="1kΩ")

# Bloco 2: 1H
bloco(ax, 2, 2, w=1.5, label="1H")

# Nó superior
ax.plot([3.5,3.5],[2,3], color="black", lw=2)

# Primeiro ramo paralelo (cima: 1H + 1kΩ)
bloco(ax, 3.5, 3, w=1.5, label="1H")
bloco(ax, 5.2, 3, w=1.5, label="1kΩ")
ax.plot([6.7,6.7],[3,2.5], color="black", lw=2)

# Segundo ramo paralelo (baixo: 1H + 1kΩ)
bloco(ax, 3.5, 2, w=1.5, label="1H")
bloco(ax, 5.2, 2, w=1.5, label="1kΩ")

# Fechando circuito
ax.plot([6.7,6.7],[2,0], color="black", lw=2)
ax.plot([6.7,0],[0,0], color="black", lw=2)
ax.plot([0,0],[0,0], color="black", lw=2)

ax.set_xlim(-1,8)
ax.set_ylim(-1,4)

plt.show()
