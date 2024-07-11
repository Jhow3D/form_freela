import streamlit as st
import sqlite3
from datetime import datetime

# Conectar ao banco de dados SQLite (ou criar se não existir)
conn = sqlite3.connect('freelas.db')
c = conn.cursor()

# Criar tabelas se não existirem
c.execute('''
CREATE TABLE IF NOT EXISTS freelas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    email TEXT,
    telefone TEXT,
    funcao TEXT,
    departamento TEXT,
    cliente TEXT
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS contratos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    freela_id INTEGER,
    data_inicio TEXT,
    data_fim TEXT,
    valor REAL,
    FOREIGN KEY(freela_id) REFERENCES freelas(id)
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS historico_mudancas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    freela_id INTEGER,
    nucleo TEXT,
    gestor TEXT,
    cpf_gestor TEXT,
    funcao TEXT,
    departamento TEXT,
    cliente TEXT,
    data_inicio TEXT,
    data_fim TEXT,
    data_mudanca TEXT,
    FOREIGN KEY(freela_id) REFERENCES freelas(id)
)
''')

conn.commit()

st.title("Gerenciamento de Freelas")

with st.expander("Contratação de Freelas"):
    # Coletar informações do usuário
    nome = st.text_input("Qual o nome do Freela?")
    email = st.text_input("Qual o e-mail para contato do Freela?")
    telefone = st.text_input("Qual o número para contato do Freela?")
    nucleo = st.multiselect("Qual o núcleo do Freela?", ["Núcleo 1", "Núcleo 2", "Núcleo 3", "Núcleo 4", "Ampla ES"])
    gestor = st.text_input("Quem é o gestor responsável?")
    cpf_gestor = st.text_input("Qual é o CPF do gestor responsável?")
    funcao = st.text_input("Qual a função do Freela?")
    departamento = st.text_input("Qual é o departamento que o Freela ficará?")
    cliente = st.text_input("Qual o cliente que o Freela atenderá as demandas?")
    data_inicio = st.date_input("Qual a data de início do contrato do Freela?")
    data_fim = st.date_input("Qual a data final do contrato do Freela?")
    valor = st.number_input("Qual o valor do período contratado?", format="%.2f")

    if st.button("Salvar Contratação"):
        # Inserir os dados do freela na tabela freelas
        c.execute('''
        INSERT INTO freelas (nome, email, telefone, funcao, departamento, cliente)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (nome, email, telefone, funcao, departamento, cliente))
        
        freela_id = c.lastrowid

        # Formatar as datas no formato dd/mm/yyyy
        data_inicio_str = data_inicio.strftime('%d/%m/%Y')
        data_fim_str = data_fim.strftime('%d/%m/%Y')

        # Inserir os dados do contrato na tabela contratos
        c.execute('''
        INSERT INTO contratos (freela_id, data_inicio, data_fim, valor)
        VALUES (?, ?, ?, ?)
        ''', (freela_id, data_inicio_str, data_fim_str, valor))
        
        # Inserir os dados iniciais na tabela historico_mudancas
        data_mudanca_str = datetime.now().strftime('%d/%m/%Y')
        c.execute('''
        INSERT INTO historico_mudancas (freela_id, nucleo, gestor, cpf_gestor, funcao, departamento, cliente, data_inicio, data_fim, data_mudanca)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (freela_id, ', '.join(nucleo), gestor, cpf_gestor, funcao, departamento, cliente, data_inicio_str, data_fim_str, data_mudanca_str))
        
        conn.commit()
        st.success("Dados salvos com sucesso!")

with st.expander("Renovação de Contrato Freelas"):
    # Selecionar o freela
    freelas = c.execute('SELECT id, nome FROM freelas').fetchall()
    freela_selecionado = st.selectbox("Selecione o Freela", [f"{freela[1]} (ID: {freela[0]})" for freela in freelas])

    if freela_selecionado:
        freela_id = int(freela_selecionado.split("ID: ")[1].split(')')[0])

        # Obter informações atuais do freela
        freela_info = c.execute('SELECT nucleo, gestor, cpf_gestor, funcao, departamento, cliente, data_inicio, data_fim FROM historico_mudancas WHERE freela_id = ? ORDER BY id DESC LIMIT 1', (freela_id,)).fetchone()
        
        nucleo_atual = freela_info[0]
        gestor_atual = freela_info[1]
        cpf_gestor_atual = freela_info[2]
        funcao_atual = freela_info[3]
        departamento_atual = freela_info[4]
        cliente_atual = freela_info[5]
        data_inicio_atual = datetime.strptime(freela_info[6], '%d/%m/%Y')
        data_fim_atual = datetime.strptime(freela_info[7], '%d/%m/%Y')

        # Mostrar campos para atualização
        nucleo_novo = st.multiselect("Qual o novo núcleo do Freela?", ["Núcleo 1", "Núcleo 2", "Núcleo 3", "Núcleo 4", "Ampla ES"], default=nucleo_atual.split(", "))
        gestor_novo = st.text_input("Quem é o novo gestor responsável?", value=gestor_atual)
        cpf_gestor_novo = st.text_input("Qual é o novo CPF do gestor responsável?", value=cpf_gestor_atual)
        funcao_nova = st.text_input("Qual a nova função do Freela?", value=funcao_atual)
        departamento_novo = st.text_input("Qual o novo departamento que o Freela ficará?", value=departamento_atual)
        cliente_novo = st.text_input("Qual o novo cliente que o Freela atenderá as demandas?", value=cliente_atual)
        
        data_inicio_renovacao = st.date_input("Qual a nova data de início do contrato?", value=data_inicio_atual)
        data_fim_renovacao = st.date_input("Qual a nova data final do contrato?", value=data_fim_atual)
        valor_renovacao = st.number_input("Qual o valor do novo período contratado?", format="%.2f")

        if st.button("Salvar Renovação"):
            # Formatar as datas no formato dd/mm/yyyy
            data_inicio_renovacao_str = data_inicio_renovacao.strftime('%d/%m/%Y')
            data_fim_renovacao_str = data_fim_renovacao.strftime('%d/%m/%Y')

            # Inserir os dados da renovação na tabela contratos
            c.execute('''
            INSERT INTO contratos (freela_id, data_inicio, data_fim, valor)
            VALUES (?, ?, ?, ?)
            ''', (freela_id, data_inicio_renovacao_str, data_fim_renovacao_str, valor_renovacao))
            
            # Registrar mudanças na tabela historico_mudancas
            data_mudanca_str = datetime.now().strftime('%d/%m/%Y')
            c.execute('''
            INSERT INTO historico_mudancas (freela_id, nucleo, gestor, cpf_gestor, funcao, departamento, cliente, data_inicio, data_fim, data_mudanca)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (freela_id, ', '.join(nucleo_novo), gestor_novo, cpf_gestor_novo, funcao_nova, departamento_novo, cliente_novo, data_inicio_renovacao_str, data_fim_renovacao_str, data_mudanca_str))

            conn.commit()
            st.success("Renovação salva com sucesso!")

# Fechar a conexão com o banco de dados
conn.close()
