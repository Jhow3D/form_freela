import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# Função para converter datas
def convert_date(date_str):
    return datetime.strptime(date_str, '%d/%m/%Y')

# Conectar ao banco de dados SQLite (ou criar se não existir)
conn = sqlite3.connect('freelas.db')
c = conn.cursor()

# Função para buscar todas as mudanças registradas
def get_all_modifications():
    c.execute('''
    SELECT hm.id, f.nome AS nome_freela, hm.nucleo, hm.gestor, hm.cpf_gestor, hm.funcao, hm.departamento, hm.cliente, hm.data_inicio, hm.data_fim, hm.data_mudanca
    FROM historico_mudancas AS hm
    INNER JOIN freelas AS f ON hm.freela_id = f.id
    ''')
    return c.fetchall()

# Função para exibir os dados na página do administrador
def show_admin_page():
    st.title("Página do Administrador")

    st.header("Tabela Geral de Modificações")
    # Exibir tabela geral de modificações
    modifications = get_all_modifications()
    if modifications:
        df_modifications = pd.DataFrame(modifications, columns=['ID', 'Nome do Freela', 'Núcleo', 'Gestor', 'CPF do Gestor', 'Função', 'Departamento', 'Cliente', 'Data de Início', 'Data de Fim', 'Data de Modificação'])
        st.dataframe(df_modifications)
    else:
        st.warning("Nenhuma modificação encontrada.")

# Verificação de acesso como administrador (apenas exemplo simples, deve ser melhorado para um sistema real)
password = st.text_input("Digite a senha para acessar como administrador:")
if password == "admin":
    show_admin_page()
else:
    st.warning("Senha incorreta. Acesso negado.")

# Fechar a conexão com o banco de dados
conn.close()
