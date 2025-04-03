
import streamlit as st
from pathlib import Path
from fpdf import FPDF

st.set_page_config(page_title="Chatbot de Rastreamento", layout="centered")
st.title("🩺 Chatbot de Rastreamento com Diretrizes – Versão Final")

st.markdown("### ✅ Preencha os dados do paciente:")

with st.form("formulario"):
    sexo = st.selectbox("Sexo:", ["", "Feminino", "Masculino"])
    idade = st.number_input("Idade:", 0, 120, step=1)
    col1, col2 = st.columns(2)
    with col1:
        imc_alto = st.checkbox("IMC ≥ 25")
        tabagista = st.checkbox("Tabagista ou ex-tabagista")
        historico_metabolico = st.checkbox("Doenças metabólicas (diabetes, HAS)")
    with col2:
        ca_mama = st.checkbox("Histórico familiar de câncer de mama")
        ca_prostata = st.checkbox("Histórico familiar de câncer de próstata")
        ca_colon = st.checkbox("Histórico familiar de câncer colorretal")
    submit = st.form_submit_button("Gerar Recomendações")

def gerar_pdf(titulo, linhas):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, titulo, ln=True)
    pdf.set_font("Arial", "", 12)
    for linha in linhas:
        pdf.multi_cell(0, 10, linha)
    nome_pdf = "resumo_rastreamento.pdf"
    pdf.output(nome_pdf)
    return nome_pdf

if submit:
    respostas = []

    if sexo == "Feminino":
        if 40 <= idade <= 74:
            respostas.append("✔️ Mamografia anual (40–74 anos). Encaminhar ao Ambulatório de Mastologia, se necessário.")
        if ca_mama and idade >= 35:
            respostas.append("✔️ Mamografia antecipada por histórico familiar (≥ 35 anos). Encaminhar ao Ambulatório de Mastologia.")
        if 25 <= idade <= 65:
            respostas.append("✔️ Papanicolau recomendado (25–65 anos). Encaminhar ao Ambulatório de Ginecologia.")

    if sexo == "Masculino":
        if idade >= 50:
            respostas.append("✔️ PSA e USG prostático (≥ 50 anos). Encaminhar ao Ambulatório de Urologia.")
        if ca_prostata and idade >= 45:
            respostas.append("✔️ Rastreamento antecipado de próstata por histórico (≥ 45 anos). Encaminhar ao Ambulatório de Urologia.")

    if ca_colon and idade >= 38:
        respostas.append("✔️ Colonoscopia antecipada por histórico familiar de câncer colorretal. Encaminhar ao Ambulatório de Proctologia.")

    if tabagista:
        if 50 <= idade <= 80:
            respostas.append("✔️ TC de tórax de baixa dose (50–80 anos, tabagista). Encaminhar ao Ambulatório de Pneumologia.")
        else:
            respostas.append("ℹ️ Tabagismo presente, mas rastreio com TC de tórax é indicado entre 50 e 80 anos.")

    if imc_alto or historico_metabolico:
        respostas.append("✔️ Avaliação metabólica: perfil lipídico, glicemia, hemoglobina glicada, HOMA-IR, TSH. Encaminhar ao Centro de Obesidade.")

    if idade >= 50:
        respostas.append("✔️ Rastreio de gamopatias monoclonais (≥ 50 anos): eletroforese e imunofixação. Encaminhar ao Ambulatório de Hematologia.")

    if respostas:
        st.subheader("📋 Recomendações:")
        for r in respostas:
            st.markdown(f"- {r}")
        if st.button("📄 Gerar PDF com resumo"):
            nome_pdf = gerar_pdf("Resumo de Rastreamento", respostas)
            with open(nome_pdf, "rb") as f:
                st.download_button("⬇️ Baixar PDF", f, file_name=nome_pdf)
    else:
        st.warning("⚠️ Nenhuma recomendação foi identificada com os dados fornecidos. Reavalie faixa etária, histórico familiar ou fatores clínicos.")
