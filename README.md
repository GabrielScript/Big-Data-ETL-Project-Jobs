# Análise de Vagas no LinkedIn com Big Data

## Introdução

Este projeto realiza uma análise exploratória de dados de vagas de emprego publicadas no LinkedIn, com foco em posições na área de Ciência de Dados e IA. Utilizando o Apache Spark para processamento de grandes volumes de dados, o projeto demonstra um fluxo de trabalho de Big Data, desde a ingestão e transformação de dados até a análise e extração de insights.

O objetivo principal é identificar tendências de mercado, como as tecnologias mais demandadas, a distribuição de salários e o impacto do trabalho remoto na disponibilidade de vagas.

## Estrutura do Projeto

O projeto está organizado da seguinte forma:

```
C:\Users\Big Data - Projeto\
├───.gitignore
├───docker-compose.yml

├───README.md
├───requirements.txt
└───Projeto Final\
    ├───ETL.ipynb
     ├───transformed_postings.csv
    └───Linkedin_dataset\
        ├───postings.csv
        ├───companies\
        │   ├───companies.csv
        │   ├───company_industries.csv
        │   ├───company_specialities.csv
        │   └───employee_counts.csv
        ├───jobs\
        │   ├───benefits.csv
        │   ├───job_industries.csv
        │   ├───job_skills.csv
        │   └───salaries.csv
        └───mappings\
            ├───industries.csv
            └───skills.csv
```

- **`docker-compose.yml`**: Arquivo de configuração para orquestração de contêineres Docker, que pode ser usado para configurar ambientes de banco de dados ou outros serviços necessários.
- **`Projeto Final/ETL.ipynb`**: Notebook Jupyter contendo todo o processo de ETL (Extração, Transformação e Carga) e análise dos dados.
- **`Projeto Final/Linkedin_dataset.zip`**: Arquivo compactado com o dataset original.
- **`Projeto Final/Linkedin_dataset/`**: Diretório contendo o dataset descompactado.
- **`Projeto Final/transformed_postings.csv`**: O dataset resultante após o processamento e limpeza.
- **`requirements.txt`**: Arquivo com as dependências do projeto.
- **`README.md`**: Esta documentação.

## Tecnologias Utilizadas

- **Apache Spark**: Ferramenta de processamento distribuído para lidar com grandes volumes de dados.
- **Python**: Linguagem de programação principal do projeto.
- **Pandas**: Biblioteca para manipulação e análise de dados em Python.
- **PyArrow**: Biblioteca para interoperabilidade de dados em memória.
- **Jupyter Notebook**: Ambiente interativo para desenvolvimento e apresentação da análise.
- **Docker / Docker Compose**: Para orquestração de contêineres e gerenciamento de serviços (se aplicável para o ambiente de execução).

## Como Executar o Projeto

1.  **Pré-requisitos**:
    *   Python 3.x
    *   Java 8 ou superior (necessário para o Spark)
    *   Docker e Docker Compose (opcional, se for utilizar serviços dockerizados)

2.  **Configuração do Ambiente (Opcional - com Docker Compose)**:
    Se o projeto depender de serviços dockerizados (como bancos de dados), inicie-os com:
    ```bash
    docker-compose up -d
    ```
    Isso iniciará os serviços definidos no `docker-compose.yml` em segundo plano.

3.  **Instalação das dependências**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Execução do notebook**:
    *   Abra o Jupyter Notebook:
        ```bash
        jupyter notebook
        ```
    *   Navegue até o diretório `Projeto Final/` e abra o arquivo `ETL.ipynb`.
    *   Execute as células do notebook para realizar o processo de ETL e análise.

## Dados

O dataset utilizado neste projeto foi extraído do LinkedIn e contém informações sobre vagas de emprego, empresas, salários, habilidades e outros detalhes relevantes. O arquivo original, `postings.csv`, possui aproximadamente 600 MB.

## Metodologia

O processo de análise foi dividido nas seguintes etapas:

1.  **Extração**: Leitura dos dados do arquivo `postings.csv` utilizando o Spark.
2.  **Limpeza e Transformação**:
    *   Conversão dos tipos de dados para formatos adequados (e.g., de string para numérico ou data).
    *   Tratamento de valores nulos e inconsistentes.
    *   Extração de tecnologias e habilidades a partir da descrição das vagas.
3.  **Análise Exploratória**:
    *   Análise de salários (mínimo, médio, máximo, normalizado).
    *   Identificação das habilidades mais requeridas.
    *   Análise do número de visualizações e aplicações por vaga.
    *   Verificação da prevalência de trabalho remoto.
    *   Filtros para isolar vagas de Ciência de Dados e IA.
4.  **Carregamento**: O DataFrame final, após o processamento, é salvo no arquivo `transformed_postings.csv`, com um tamanho reduzido para 10 MB.

## Principais Resultados

- **Muitos valores nulos** na base original — exigiu tratamento e imputação.
- **Tecnologias**:
  - Vagas de Ciência de Dados e IA mencionam mais **R** que **Python** e **SQL**.
  - No entanto, **salário médio** foi maior em vagas que exigiam Python e SQL.
- **Salários**:
  - Grande parte das vagas com `normalized_salary > 100 000 USD/ano`.
  - Ao aplicar o filtro de trabalho remoto, **restam pouquíssimas vagas**.
- **Profissões**:
  - **Data Scientist** foi a função mais frequente.
  - A maioria das vagas é para **nível Sênior**.
- **Habilidades interpessoais** (“soft skills”):
  - Comunicação, colaboração e outras “People Skills” foram as mais demandadas.
- **Redução de tamanho**:
  - O dataset passou de **600 MB** para **10 MB** após limpeza e transformação.

## Considerações Finais

- O alto volume de valores faltantes destaca a importância de **imputação** e **filtragem** criteriosa.
- A predominância de R em vagas de IA aponta para demandas específicas de mercado em 2023.
- O filtro de remoto revelou um mercado restrito para posições de alta remuneração.
- Soft skills continuam sendo um diferencial decisivo em processos seletivos de TI.
