import oracledb
import csv
import os
from dotenv import load_dotenv

load_dotenv()
# ==========================================
# 1. Credenciais e Configurações
# ==========================================
USUARIO = os.getenv("DB_USER")
PALAVRA_PASSE = os.getenv("DB_PASSWORD")
CONNECTION_STRING = os.getenv("DB_CONNECTION_STRING")
CAMINHO_WALLET = "./wallet"
PALAVRA_PASSE_WALLET = os.getenv("WALLET_PASSWORD")

#caminho do CSV
CAMINHO_CSV = "./creditcard.csv"

# Tamanho do lote (inserir de 10 mil em 10 mil linhas evita estouro de memória)
TAMANHO_LOTE = 10000 

# ==========================================
# 2. Query de Inserção
# ==========================================
SQL_INSERT = """
    INSERT INTO credit_card_transactions (
        transaction_time, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, 
        v11, v12, v13, v14, v15, v16, v17, v18, v19, v20, 
        v21, v22, v23, v24, v25, v26, v27, v28, amount, transaction_class
    ) VALUES (
        :1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, 
        :12, :13, :14, :15, :16, :17, :18, :19, :20, :21, 
        :22, :23, :24, :25, :26, :27, :28, :29, :30, :31
    )
"""

# ==========================================
# 3. Execução
# ==========================================
try:
    print("Conectando ao banco de dados...")
    connection = oracledb.connect(
    user=USUARIO,
    password=PALAVRA_PASSE,
    dsn=CONNECTION_STRING,             
    config_dir=CAMINHO_WALLET,         
    wallet_location=CAMINHO_WALLET,   
    wallet_password=PALAVRA_PASSE_WALLET
)
    cursor = connection.cursor()
    print("Conexão bem-sucedida!\n")

    print(f"Lendo o arquivo: {CAMINHO_CSV}")
    
    lote_atual = []
    linhas_inseridas = 0

    with open(CAMINHO_CSV, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        
        # Pula a primeira linha (cabeçalho)
        next(csv_reader) 
        
        for row in csv_reader:
            # Converte as strings do CSV para números (float para os dados, int para a classe)
            # row[:-1] pega de Time até Amount, row[-1] pega a Class
            linha_convertida = [float(valor) for valor in row[:-1]]
            
            # Limpa aspas da coluna Class (caso existam) e converte para inteiro
            classe_limpa = int(row[-1].replace('"', '').strip())
            linha_convertida.append(classe_limpa)
            
            # Adiciona a tupla formatada no lote
            lote_atual.append(tuple(linha_convertida))
            
            # Se o lote atingiu o limite, faz a inserção no banco
            if len(lote_atual) == TAMANHO_LOTE:
                cursor.executemany(SQL_INSERT, lote_atual)
                linhas_inseridas += len(lote_atual)
                print(f"Inseridas {linhas_inseridas} linhas...")
                lote_atual.clear() # Limpa o lote para a próxima rodada

        # Insere as linhas restantes que não completaram um lote inteiro
        if len(lote_atual) > 0:
            cursor.executemany(SQL_INSERT, lote_atual)
            linhas_inseridas += len(lote_atual)
            print(f"Inseridas {linhas_inseridas} linhas...")

    # Efetiva a gravação no banco de dados (IMPORTANTE)
    connection.commit()
    print("\nCarga finalizada com sucesso! Todos os dados foram gravados.")

except Exception as e:
    print("\nOcorreu um erro durante a execução:")
    print(e)
    # Em caso de erro, desfaz qualquer inserção parcial
    if 'connection' in locals():
        connection.rollback()

finally:
    # Garante que os recursos serão liberados
    if 'cursor' in locals():
        cursor.close()
    if 'connection' in locals():
        connection.close()
        print("Conexão com o banco fechada.")