import streamlit as st
import schemdraw
import schemdraw.elements as elm

st.title("🔌 Montagem de Circuitos Elétricos com Streamlit")

st.sidebar.header("Escolha os Componentes")

# Opções de componentes
resistores = st.sidebar.slider("Quantidade de Resistores", 0, 3, 2)
capacitores = st.sidebar.slider("Quantidade de Capacitores", 0, 2, 1)
fontes = st.sidebar.selectbox("Fonte de Alimentação", ["Nenhuma", "VCC", "Fonte AC"])

st.write("### Circuito Gerado:")

# Desenha o circuito com schemdraw
with schemdraw.Drawing() as d:
    # Fonte
    if fontes == "VCC":
        d += elm.SourceV().up().label("VCC")
    elif fontes == "Fonte AC":
        d += elm.SourceSin().up().label("AC")
    else:
        d += elm.Line().up()

    # Resistores
    for i in range(resistores):
        d += elm.Resistor().right().label(f"R{i+1}")

    # Capacitores
    for i in range(capacitores):
        d += elm.Capacitor().down().label(f"C{i+1}")

    d += elm.Line().left().to(d.here - (len(d.elements) - 1, 0))

    st.image(d.get_imagedata(), caption="Circuito Montado")

st.success("✅ Circuito montado com sucesso!")
