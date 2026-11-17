import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from datetime import date

# FinanceControl - Gerenciador de Finanças Pessoais
ARQUIVO_DADOS = Path(__file__).parent / "movimentacoes.csv"
COLUNAS = ["id", "data", "tipo", "descricao", "categoria", "valor"]

st.set_page_config(
    page_title="FinanceControl",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

def carregar_dados():
    """Carrega as movimentações salvas em CSV."""
    if ARQUIVO_DADOS.exists():
        try:
            dados = pd.read_csv(ARQUIVO_DADOS)
            for coluna in COLUNAS:
                if coluna not in dados.columns:
                    dados[coluna] = None
            dados["valor"] = pd.to_numeric(dados["valor"], errors="coerce").fillna(0)
            dados["data"] = pd.to_datetime(dados["data"], errors="coerce").dt.date
            return dados[COLUNAS]
        except Exception:
            st.warning("Não foi possível ler o arquivo de dados. Um novo histórico será iniciado.")
    return pd.DataFrame(columns=COLUNAS)

def salvar_dados(dados):
    """Salva as movimentações para que continuem disponíveis ao reabrir o app."""
    dados.to_csv(ARQUIVO_DADOS, index=False, encoding="utf-8")

def moeda(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

if "dados" not in st.session_state:
    st.session_state.dados = carregar_dados()

dados = st.session_state.dados

# Cabeçalho
st.title("💰 FinanceControl")
st.caption("Organize suas receitas, despesas e acompanhe sua vida financeira.")
st.divider()

# Indicadores
receitas = dados.loc[dados["tipo"] == "Receita", "valor"].sum()
despesas = dados.loc[dados["tipo"] == "Despesa", "valor"].sum()
saldo = receitas - despesas

c1, c2, c3 = st.columns(3)
c1.metric("💵 Saldo atual", moeda(saldo))
c2.metric("📈 Total de receitas", moeda(receitas))
c3.metric("📉 Total de despesas", moeda(despesas))

st.divider()

# Menu lateral
pagina = st.sidebar.radio(
    "Navegação",
    ["Visão geral", "Adicionar movimentação", "Histórico"]
)
st.sidebar.info("FinanceControl • Projeto escolar de Programação e Empreendedorismo")

if pagina == "Visão geral":
    st.subheader("Visão geral")
    if dados.empty:
        st.info("Ainda não existem movimentações. Acesse 'Adicionar movimentação' para começar.")
    else:
        esquerda, direita = st.columns(2)
        with esquerda:
            st.markdown("#### Receitas x despesas")
            resumo = pd.DataFrame({
                "Tipo": ["Receitas", "Despesas"],
                "Valor": [receitas, despesas]
            })
            fig = px.bar(
                resumo, x="Tipo", y="Valor", color="Tipo",
                color_discrete_map={"Receitas": "#16a34a", "Despesas": "#dc2626"},
                text_auto=".2s"
            )
            fig.update_layout(showlegend=False, yaxis_title="Valor (R$)", xaxis_title="")
            st.plotly_chart(fig, use_container_width=True)
        with direita:
            st.markdown("#### Despesas por categoria")
            despesas_cat = dados[dados["tipo"] == "Despesa"].groupby("categoria", as_index=False)["valor"].sum()
            if despesas_cat.empty:
                st.info("Cadastre despesas para visualizar este gráfico.")
            else:
                fig2 = px.pie(despesas_cat, names="categoria", values="valor", hole=0.45)
                st.plotly_chart(fig2, use_container_width=True)

        st.markdown("#### Últimas movimentações")
        recentes = dados.sort_values(["data", "id"], ascending=False).head(5)
        tabela = recentes[["data", "tipo", "descricao", "categoria", "valor"]].copy()
        tabela["valor"] = tabela["valor"].apply(moeda)
        st.dataframe(tabela, use_container_width=True, hide_index=True)

elif pagina == "Adicionar movimentação":
    st.subheader("Adicionar movimentação")
    st.write("Preencha os campos abaixo para registrar uma entrada ou saída de dinheiro.")
    with st.form("form_movimentacao", clear_on_submit=True):
        tipo = st.selectbox("Tipo de movimentação", ["Receita", "Despesa"])
        descricao = st.text_input("Descrição", placeholder="Ex.: Salário, mercado, transporte...")
        categoria = st.selectbox(
            "Categoria",
            ["Salário", "Alimentação", "Transporte", "Moradia", "Lazer",
             "Educação", "Saúde", "Contas", "Compras", "Outros"]
        )
        valor = st.number_input("Valor (R$)", min_value=0.01, step=1.0, format="%.2f")
        data_mov = st.date_input("Data", value=date.today(), format="DD/MM/YYYY")
        enviado = st.form_submit_button("Salvar movimentação", type="primary", use_container_width=True)

        if enviado:
            if not descricao.strip():
                st.error("Informe uma descrição para a movimentação.")
            elif valor <= 0:
                st.error("O valor precisa ser maior que zero.")
            else:
                proximo_id = int(pd.to_numeric(dados["id"], errors="coerce").max()) + 1 if not dados.empty else 1
                novo = pd.DataFrame([{
                    "id": proximo_id,
                    "data": data_mov,
                    "tipo": tipo,
                    "descricao": descricao.strip(),
                    "categoria": categoria,
                    "valor": float(valor)
                }])
                st.session_state.dados = pd.concat([dados, novo], ignore_index=True)
                salvar_dados(st.session_state.dados)
                st.success("Movimentação cadastrada com sucesso!")
                st.rerun()

elif pagina == "Histórico":
    st.subheader("Histórico de movimentações")
    if dados.empty:
        st.info("Seu histórico está vazio.")
    else:
        f1, f2 = st.columns(2)
        with f1:
            filtro_tipo = st.selectbox("Filtrar por tipo", ["Todos", "Receita", "Despesa"])
        with f2:
            categorias = ["Todas"] + sorted(dados["categoria"].dropna().unique().tolist())
            filtro_categoria = st.selectbox("Filtrar por categoria", categorias)

        filtrados = dados.copy()
        if filtro_tipo != "Todos":
            filtrados = filtrados[filtrados["tipo"] == filtro_tipo]
        if filtro_categoria != "Todas":
            filtrados = filtrados[filtrados["categoria"] == filtro_categoria]

        exibicao = filtrados.sort_values(["data", "id"], ascending=False).copy()
        exibicao["valor"] = exibicao["valor"].apply(moeda)
        st.dataframe(
            exibicao[["data", "tipo", "descricao", "categoria", "valor"]],
            use_container_width=True, hide_index=True
        )

        st.download_button(
            "⬇️ Baixar histórico em CSV",
            data=filtrados.to_csv(index=False).encode("utf-8-sig"),
            file_name="historico_financecontrol.csv",
            mime="text/csv"
        )

        st.divider()
        st.markdown("#### Excluir movimentação")
        opcoes = {
            f'#{int(linha["id"])} • {linha["descricao"]} • {moeda(float(linha["valor"]))}':
            int(linha["id"])
            for _, linha in filtrados.iterrows()
        }
        escolha = st.selectbox("Selecione um registro", list(opcoes.keys()))
        if st.button("Excluir registro selecionado", type="secondary"):
            id_excluir = opcoes[escolha]
            st.session_state.dados = st.session_state.dados[
                st.session_state.dados["id"].astype(int) != id_excluir
            ]
            salvar_dados(st.session_state.dados)
            st.success("Registro excluído.")
            st.rerun()

st.divider()
st.caption("FinanceControl — Os dados são armazenados em um arquivo CSV na pasta do projeto.")
