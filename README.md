# FinanceControl

Gerenciador de finanças pessoais desenvolvido em Python com Streamlit.

## Funcionalidades
- Cadastro de receitas e despesas.
- Cálculo automático do saldo.
- Gráfico de receitas x despesas.
- Gráfico de despesas por categoria.
- Histórico com filtros.
- Exclusão de movimentações.
- Exportação do histórico em CSV.
- Salvamento local em `movimentacoes.csv`.

## Como executar no computador

1. Instale o Python 3.10 ou superior.
2. Extraia esta pasta.
3. Abra o terminal dentro da pasta `FinanceControl`.
4. Instale as bibliotecas:

   ```bash
   pip install -r requirements.txt
   ```

5. Inicie o sistema:

   ```bash
   streamlit run app.py
   ```

6. O navegador abrirá o FinanceControl. Se não abrir automaticamente, acesse o endereço local mostrado no terminal (normalmente `http://localhost:8501`).

## Publicar para o professor acessar

O GitHub Pages hospeda páginas estáticas e não executa diretamente uma aplicação Python/Streamlit. Para publicar este projeto:

1. Crie uma conta no GitHub e um repositório chamado `financecontrol`.
2. Envie `app.py`, `requirements.txt` e os demais arquivos do projeto para o repositório.
3. Entre em https://share.streamlit.io/ e conecte sua conta GitHub.
4. Escolha o repositório, a branch principal e o arquivo `app.py`.
5. Clique em Deploy. O Streamlit Community Cloud fornecerá um link público para compartilhar com o professor.

**Importante:** o arquivo CSV é adequado para demonstração local. Em uma publicação na nuvem, o armazenamento local pode não ser permanente entre reinicializações ou novas implantações. Para uso real com vários usuários, seria necessário conectar um banco de dados.

## Estrutura

- `app.py`: código principal do sistema.
- `requirements.txt`: bibliotecas necessárias.
- `relatorio.pdf`: documentação das três etapas do trabalho.
- `movimentacoes.csv`: criado automaticamente quando o primeiro registro é salvo.
