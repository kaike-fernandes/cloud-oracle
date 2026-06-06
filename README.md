# 🚀 Carga de Dados CSV para Oracle Database

Este projeto é um script em Python projetado para ler grandes volumes de dados de um arquivo CSV (como o dataset de transações de cartão de crédito) e inseri-los de forma eficiente e segura em um banco de dados Oracle Autonomous Database na Oracle Cloud Infrastructure (OCI).

O script utiliza inserção em lotes (*bulk insert*) para otimizar o uso de memória e maximizar a velocidade da carga.

---

## 🛠️ Tecnologias Utilizadas

* **Python 3.x**
* **oracledb:** Biblioteca oficial da Oracle para conexão com o banco de dados.
* **python-dotenv:** Gerenciamento de variáveis de ambiente de forma segura.
* **csv (Nativo):** Para leitura do arquivo com baixo consumo de memória.

---

## ⚙️ Passo a Passo para Execução

Siga as instruções abaixo para configurar o ambiente e rodar o projeto na sua máquina.

### 1. Clonar ou Baixar o Projeto
Certifique-se de que os arquivos do projeto (`importar_dados.py`, `requirements.txt` e o seu arquivo `.csv`) estão na mesma pasta.

### 2. Criar e Ativar o Ambiente Virtual (`myvenv`)
O ambiente virtual isola as dependências do projeto, evitando conflitos com o sistema operacional.

Abra o terminal na pasta do projeto e execute:

**No Linux / macOS:**
```bash
# Cria o ambiente virtual chamado 'myvenv'
python3 -m venv myvenv

# Ativa o ambiente virtual
source myvenv/bin/activate
