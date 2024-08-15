import streamlit as st


@st.cache_data(ttl=3600)
def app():
    st.header("Consulta CVM | Fundos")
    st.write(
        "O APP disponibiliza a consulta aos Fundos de Investimento registrados na CVM de forma gratuita."
    )
    st.write(
        "Podem ser obtidas todas as informações públicas dos fundos, tais como dados cadastrais, valor diário da cota e do patrimônio líquido, número de cotistas, valores captados e resgatados."
    )
    st.write(
        "Consulte, através dos ícones, os dados cadastrais dos fundos de investimento registrados na CVM e o INFORME DIÁRIO."
    )
    st.write(
        "Todos os dados são obtidos através do **Portal Dados Abertos CVM** e atualizados diariamente."
    )
