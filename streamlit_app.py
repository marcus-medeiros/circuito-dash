import matplotlib.pyplot as plt

def resistor(ax, x, y, length=1.0, orientation="h", label=""):
    """
    Desenha um símbolo de resistor (zig-zag simplificado).
    orientation: "h" horizontal ou "v" vertical
    """
    if orientation == "h":
        ax.plot([x, x+length], [y, y], color="black", lw=2, zorder=2)
        ax.text(x+length/2, y+0.2, label, ha="center")
    else:
        ax.plot([x, x], [y, y-length], color="black", lw=2, zorder=2)
        ax.text(x+0.2, y-length/2, label, va="center")

fig, ax = plt.subplots(figsize=(6,6))
ax.axis("off")

# Fonte
ax.plot([0,0],[0,2], color="black", lw=2)
ax.text(-0.4,1,"Fonte\n60Hz", va="center")

# Resistor (1k)
resistor(ax,0,2,length=1.5,orientation="h",label="1kΩ")

# Indutor (1H representado como resistor)
resistor(ax,1.5,2,length=1.5,orientation="h",label="1H")

# Nó superior
ax.plot([3,3],[2,3], color="black", lw=2)

# Primeiro ramo paralelo (topo)
resistor(ax,3,3,length=1.5,orientation="h",label="1H")
resistor(ax,4.5,3,length=1.5,orientation="h",label="1kΩ")

# Conexão descendo
ax.plot([6,6],[3,2.5], color="black", lw=2)

# Segundo ramo paralelo (baixo)
resistor(ax,3,2,length=1.5,orientation="h",label="1H")
resistor(ax,4.5,2,length=1.5,orientation="h",label="1kΩ")

# Fechando circuito
ax.plot([6,6],[2,0], color="black", lw=2)
ax.plot([6,0],[0,0], color="black", lw=2)

ax.set_xlim(-1,7)
ax.set_ylim(-1,4)

plt.show()
