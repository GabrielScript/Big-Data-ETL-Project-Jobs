# Gabriel Estrela Lopes
# 20210161989
import yfinance as yf             
import pandas as pd                
import requests                  
import redis                      
from pymongo import MongoClient   
from cassandra.cluster import Cluster  
from neo4j import GraphDatabase   
from dotenv import load_dotenv    
import os                        

load_dotenv()                    
# Lista de tickers das ações da B3
acoes = ["ELET3.SA", "ELET6.SA", "CPLE6.SA", "TAEE11.SA"]

# Puxa os dados históricos das ações entre 01/01/2020 e 01/01/2023 com intervalo diário
df = yf.download(acoes, start="2020-01-01", end="2023-01-01", interval="1d")

# Calcula a média móvel de 20 dias para os preços de fechamento
ma_df = df["Close"].rolling(window=20).mean()
# Renomeia as colunas para indicar que são médias móveis de 20 dias
ma_df.columns = [f"{col}_20d_ma" for col in ma_df.columns]

print(ma_df)  
print(df)      

# Consulta os perfis das ações através da API do Financial Modeling Prep
api_key = "whghmm03gkH0pPM3hMOzOqJ83bQN0M9M"   
acoes_emp = ",".join(acoes)                     
url = f"https://financialmodelingprep.com/api/v3/profile/{acoes_emp}?apikey={api_key}"  
profile_data = requests.get(url).json()         
print(pd.DataFrame(profile_data))               

# Função para inserir dados no Redis
def ingest_redis(acoes, df):
    r = redis.Redis(host="localhost", port=6379, decode_responses=True) 
    for acao in acoes:
        if acao in df["Close"].columns:  
            # Obtém o último valor não nulo de fechamento e volume
            close_val = df["Close"][acao].dropna().iloc[-1]
            vol_val = df["Volume"][acao].dropna().iloc[-1]
            # Armazena os dados no Redis usando uma chave formatada
            r.set(f"stock:{acao}", f"close:{close_val}, volume:{vol_val}")
    return r  # Retorna a conexão com o Redis

# Função para inserir dados no MongoDB
def ingest_mongodb(acoes, df):
    client = MongoClient("mongodb://mongo:mongo@localhost:27017/")  

    db = client.finance        
    coll = db.stocks            
    for acao in acoes:
        if acao in df["Close"].columns:  
            # Converte os valores para os tipos adequados
            close_val = float(df["Close"][acao].dropna().iloc[-1])
            vol_val = int(df["Volume"][acao].dropna().iloc[-1])
            # Insere um documento na coleção com ticker, fechamento e volume
            coll.insert_one({"ticker": acao, "close": close_val, "volume": vol_val})
    return coll  

# Função para inserir dados no Cassandra
def ingest_cassandra(acoes, df):
    cluster = Cluster(["localhost"])
    session = cluster.connect()         
    # Cria o keyspace 'finance' se não existir, com replicação simples
    session.execute("CREATE KEYSPACE IF NOT EXISTS finance WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1}")
    session.set_keyspace("finance")     
    # Cria a tabela 'stocks' se não existir, com colunas para ticker, fechamento e volume
    session.execute("CREATE TABLE IF NOT EXISTS stocks (ticker text PRIMARY KEY, close float, volume int)")
    for acao in acoes:
        if acao in df["Close"].columns:  
            # Converte os valores para os tipos adequados
            close_val = float(df["Close"][acao].dropna().iloc[-1])
            vol_val = int(df["Volume"][acao].dropna().iloc[-1])
            # Insere os dados na tabela 'stocks'
            session.execute("INSERT INTO stocks (ticker, close, volume) VALUES (%s, %s, %s)", (acao, close_val, vol_val))
    return session  # Retorna a sessão do Cassandra

# Função para inserir dados no Neo4j
def ingest_neo4j(acoes, df):
    # Conecta ao banco Neo4j usando o protocolo bolt, com autenticação 
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", os.getenv("NEO4J_PASSWORD") or "P4sSw0rD"))

    # Função auxiliar para criar ou atualizar um nó para a ação no Neo4j
    def create_node(tx, acao, close_val):
        tx.run("MERGE (s:Stock {ticker: $ticker}) SET s.close = $close", ticker=acao, close=close_val)
    # Abre uma sessão no Neo4j para executar as operações
    with driver.session() as neo_session:
        for acao in acoes:
            if acao in df["Close"].columns:  
              
                close_val = float(df["Close"][acao].dropna().iloc[-1])
               
                neo_session.execute_write(create_node, acao, close_val)
    return driver 

# Chama as funções de ingestão para cada banco de dados e armazena as conexões/objetos resultantes
r = ingest_redis(acoes, df)
coll = ingest_mongodb(acoes, df)
session = ingest_cassandra(acoes, df)
driver = ingest_neo4j(acoes, df)



# Recupera e imprime os dados da primeira ação no Redis
print(r.get(f"stock:{acoes[0]}"))

# Busca e imprime o documento da primeira ação no MongoDB
print(coll.find_one({"ticker": acoes[0]}))

# Executa uma consulta no Cassandra para recuperar os dados da primeira ação e imprime cada linha
rows = session.execute(f"SELECT * FROM stocks WHERE ticker='{acoes[0]}'")
for row in rows:
    print(row)

# Executa uma consulta Cypher no Neo4j para recuperar todos os nós com a label 'Stock' e imprime cada registro
with driver.session() as neo_session:
    result = neo_session.run("MATCH (s:Stock) RETURN s.ticker as ticker, s.close as close")
    for record in result:
        print(record)
