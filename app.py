
import streamlit as st
from datetime import date

st.set_page_config(
    page_title="Prime Cars | Locadora",
    page_icon="🚗",
    layout="wide"
)

# CORES E ESTILO
st.markdown("""
<style>
.stApp {
    background-color: #101820;
    color: white;
}
h1, h2, h3, p, label {
    color: white !important;
}
.carro {
    background: #202d38;
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 10px;
}
.stButton button {
    background-color: #00a86b;
    color: white;
    border-radius: 10px;
    border: none;
    width: 100%;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# DADOS DA LOCADORA
PIX = "52146865873"


carros = {
    # ECONÔMICOS
    "Fiat Mobi": {"preco": 120, "emoji": "🚗"},
    "Renault Kwid": {"preco": 120, "emoji": "🚗"},
    "Fiat Argo": {"preco": 150, "emoji": "🚗"},
    "Hyundai HB20": {"preco": 170, "emoji": "🚗"},
    "Chevrolet Onix": {"preco": 160, "emoji": "🚗"},
    "Volkswagen Polo": {"preco": 190, "emoji": "🚗"},

    # SEDANS
    "Toyota Corolla": {"preco": 280, "emoji": "🚘"},
    "Honda Civic": {"preco": 300, "emoji": "🚘"},
    "Chevrolet Cruze": {"preco": 260, "emoji": "🚘"},
    "Nissan Versa": {"preco": 210, "emoji": "🚘"},

    # SUVs
    "Jeep Renegade": {"preco": 280, "emoji": "🚙"},
    "Jeep Compass": {"preco": 350, "emoji": "🚙"},
    "Hyundai Creta": {"preco": 300, "emoji": "🚙"},
    "Honda HR-V": {"preco": 320, "emoji": "🚙"},
    "Toyota Corolla Cross": {"preco": 380, "emoji": "🚙"},
    "Volkswagen T-Cross": {"preco": 290, "emoji": "🚙"},

    # LUXO
    "BMW 320i": {"preco": 650, "emoji": "🏎️"},
    "Mercedes-Benz C200": {"preco": 700, "emoji": "🏎️"},
    "Audi A3": {"preco": 550, "emoji": "🏎️"},
    "Porsche Macan": {"preco": 950, "emoji": "🏎️"},

    # PICAPES
    "Fiat Toro": {"preco": 350, "emoji": "🛻"},
    "Toyota Hilux": {"preco": 500, "emoji": "🛻"},
    "Ford Ranger": {"preco": 480, "emoji": "🛻"},

    # 7 LUGARES
    "Chevrolet Spin": {"preco": 280, "emoji": "🚐"},
    "Mitsubishi Outlander": {"preco": 450, "emoji": "🚙"},
}


# CABEÇALHO
st.title("🚗 PRIME CARS")
st.subheader("Sua liberdade começa aqui!")
st.write("Alugue seu carro com facilidade, segurança e praticidade.")

st.divider()

# MENU
pagina = st.sidebar.radio(
    "MENU",
    ["Início", "Nossos carros", "Alugar carro", "Minha reserva"]
)

if "reservas" not in st.session_state:
    st.session_state.reservas = []

# INÍCIO
if pagina == "Início":

    st.title("Bem-vindo à Prime Cars!")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Modelos disponíveis", len(carros))

    with c2:
        st.metric("Preço inicial", "R$ 120/dia")

    with c3:
        st.metric("Formas de pagamento", "PIX e cartão")

    st.divider()

    st.subheader("Encontre seu próximo carro")

    if st.button("ALUGAR AGORA"):
        st.session_state.pagina = "Alugar carro"
        st.rerun()

    st.info("Escolha seu veículo, faça sua reserva e selecione entrega ou retirada.")

# CATÁLOGO
elif pagina == "Nossos carros":

    st.title("🚘 Nossa frota")

    colunas = st.columns(3)

    for i, (nome, dados) in enumerate(carros.items()):

        with colunas[i % 3]:
            st.markdown('<div class="carro">', unsafe_allow_html=True)

            st.markdown(f"## {dados['emoji']}")
            st.subheader(nome)
            st.write(f"R$ {dados['preco']},00 por dia")

            st.markdown('</div>', unsafe_allow_html=True)

# ALUGUEL
elif pagina == "Alugar carro":

    st.title("📋 Faça sua reserva")

    with st.form("formulario_reserva"):

        nome = st.text_input("Nome completo")
        telefone = st.text_input("Telefone / WhatsApp")

        carro = st.selectbox(
            "Escolha seu veículo",
            list(carros.keys())
        )

        retirada = st.date_input(
            "Data de retirada",
            value=date.today()
        )

        devolucao = st.date_input(
            "Data de devolução",
            value=date.today()
        )

        st.subheader("Como deseja receber o carro?")

        entrega = st.radio(
            "Escolha uma opção",
            ["Retirar na locadora", "Receber no meu endereço"]
        )

        endereco = ""

        if entrega == "Receber no meu endereço":
            endereco = st.text_input("Endereço completo para entrega")

        st.subheader("💳 Forma de pagamento")

        pagamento = st.radio(
            "Escolha como deseja pagar",
            ["PIX", "Cartão"]
        )

        enviar = st.form_submit_button("CONFIRMAR RESERVA")

    if enviar:

        if not nome or not telefone:
            st.error("Preencha seu nome e telefone.")

        elif devolucao <= retirada:
            st.error("A devolução deve ser depois da retirada.")

        elif entrega == "Receber no meu endereço" and not endereco:
            st.error("Informe o endereço de entrega.")

        else:

            dias = (devolucao - retirada).days
            valor = dias * carros[carro]["preco"]

            reserva = {
                "nome": nome,
                "telefone": telefone,
                "carro": carro,
                "retirada": str(retirada),
                "devolucao": str(devolucao),
                "dias": dias,
                "valor": valor,
                "entrega": entrega,
                "endereco": endereco,
                "pagamento": pagamento
            }

            st.session_state.reservas.append(reserva)

            st.session_state.ultima_reserva = reserva

            st.success("Reserva registrada com sucesso!")

            st.write("### Resumo da reserva")
            st.write("Cliente:", nome)
            st.write("Carro:", carro)
            st.write("Quantidade de dias:", dias)
            st.write("Valor total: R$", valor)
            st.write("Recebimento:", entrega)

            if pagamento == "PIX":
                st.subheader("💚 Pagamento via PIX")
                st.code(PIX)
                st.write("Chave PIX informada pela locadora.")
                st.warning("Confira o nome do destinatário antes de realizar o pagamento. A confirmação do PIX ainda precisa ser feita pela locadora.")

            else:
                st.subheader("💳 Pagamento com cartão")
                st.info("Sua solicitação de pagamento foi registrada. O pagamento deverá ser concluído por um link ou sistema de cartão seguro.")

# MINHAS RESERVAS
elif pagina == "Minha reserva":

    st.title("📑 Reservas registradas")

    if not st.session_state.reservas:
        st.info("Nenhuma reserva registrada ainda.")

    for i, reserva in enumerate(st.session_state.reservas):

        with st.expander(f"Reserva {i + 1} - {reserva['nome']}"):

            st.write("Cliente:", reserva["nome"])
            st.write("Telefone:", reserva["telefone"])
            st.write("Carro:", reserva["carro"])
            st.write("Retirada:", reserva["retirada"])
            st.write("Devolução:", reserva["devolucao"])
            st.write("Dias:", reserva["dias"])
            st.write("Entrega:", reserva["entrega"])
            st.write("Endereço:", reserva["endereco"])
            st.write("Pagamento:", reserva["pagamento"])
            st.write("Total: R$", reserva["valor"])

st.divider()

st.caption("PRIME CARS © 2026 - Sua melhor escolha para alugar carros.")
