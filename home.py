import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Dashboard de vendas - 2022",
    page_icon=":bar_chart",
    layout="wide"
)

# Leitura de Excel com cache do ficheiro
@st.cache
def get_data_from_excel():
    df = pd.read_excel(
        io='vendas_supermercado.xlsx',
        engine='openpyxl',
        sheet_name='Vendas',
        skiprows=3,
        usecols='B:R',
        nrows=1000,
    )
    # Adicionar coluna "hora" no dataframe
    df["hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour
    return df

df = get_data_from_excel()


# -----Sidebar
st.sidebar.header("Por favor, seleciona o filtro:")
cidade = st.sidebar.multiselect(
    "Seleciona a Cidade:",
    options=df['City'].unique(),
    default=df['City'].unique()
)

tipo_cliente = st.sidebar.multiselect(
    "Seleciona o tipo de cliente:",
    options=df['Customer_type'].unique(),
    default=df['Customer_type'].unique()
)

sexo = st.sidebar.multiselect(
    "Seleciona o sexo:",
    options=df['Gender'].unique(),
    default=df['Gender'].unique()
)

selecao = df.query(
    "City == @cidade & Customer_type == @tipo_cliente & Gender == @sexo"
)

#st.dataframe(selecao)

# ----------Main page
st.title(":bar_chart: Dashboard de Vendas - 2022")
st.markdown("##")

# Calculo de TOP KPI's
total_vendas = int(selecao["Total"].sum())
taxa_media = round(selecao["Rating"].mean(), 1)
taxa_star = ":star:" * int(round(taxa_media, 0))
media_vendas_transacao = round(selecao["Total"].mean(), 2)

# ---Montagem da page
left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total de Vendas:")
    st.subheader(f"MZN {total_vendas: ,}")
with middle_column:
   st.subheader("Taxa Média:")
   st.subheader(f"{taxa_media} {taxa_star}")
with right_column:
    st.subheader("Média Por Transação")
    st.subheader(f"MZN {media_vendas_transacao}")

st.markdown("---")

# Vendas por Produto (Grafico de Barras)
vendas_produto_linha = (
    selecao.groupby(by=["Product line"]).sum()[["Total"]].sort_values(by="Total")
)
fig_vendas_produto = px.bar(
    vendas_produto_linha,
    x="Total",
    y=vendas_produto_linha.index,
    orientation="h",
    title="<b>Vendas por linha</b>",
    color_discrete_sequence=["#0083BB"] * len(vendas_produto_linha),
    template="plotly_white",
)
fig_vendas_produto.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)
#st.plotly_chart(fig_vendas_produto)

# Vendas por Hora (Grafico de Barras)
vendas_hora = selecao.groupby(by=["hour"]).sum()[["Total"]]
fig_vendas_hora = px.bar(
  vendas_hora,
  x=vendas_hora.index,
  y="Total",
  title="<b>Vendas por hora</b>",
  color_discrete_sequence=["#0083B8"] * len(vendas_hora),
  template="plotly_white",
)
fig_vendas_hora.update_layout(
    xaxis = dict(tickmode="linear"),
    plot_bgcolor = "rgba(0,0,0,0)",
    yaxis = (dict(showgrid=False)),
)
#st.plotly_chart(fig_vendas_hora)
left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_vendas_hora, use_container_width=True)
right_column.plotly_chart(fig_vendas_produto, use_container_width=True)

st.title("Tabela de dados")
st.markdown("###")
st.dataframe(selecao)

# Hide Streamlite style
hide_st_styles = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_styles, unsafe_allow_html=True)