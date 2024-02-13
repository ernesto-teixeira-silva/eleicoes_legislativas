import tabula
import pandas as pd
import os
import json

# Define e caminho do ficheiro 'resultados_2022.pdf'
path_file = '../docs/resultados_2022.pdf'

# Lê todas as tabelas no dataframe
df = tabula.read_pdf(path_file, pages='all', stream=True)

# CRIA O DATAFRAME COM OS DADOS GERAIS
linhas_geral = ['Inscritos', 'Votantes (VTT)', 'Brancos', 'Nulos', 'Votos Val. Exp.']
df_geral = df[0].loc[df[0]['Unnamed: 0'].isin(linhas_geral)]

# Nomeia as colunas
colunas = ['Partido', 'Número', 'Aveiro', 'Beja', 'Braga', 'Bragança', 'Castelo Branco', 'Coimbra', 'Évora', 'Faro',
'Guarda', 'Leiria', 'Lisboa', 'Portalegre', 'Porto', 'Santarém', 'Setúbal', 'Viana do Castelo',
'Vila Real', 'Viseu', 'RA Açores', 'RA Madeira', 'Europa', 'Fora da Europa', 'Total']
df_geral.columns = colunas

# Elimina as colunas sem dados
df_geral = df_geral.dropna(axis=1)

# CRIA O DATAFRAME COM OS DADOS VOTOS
# Define as linhas do DataFrame
partidos = [  'A', 'ADN', 'BE', 'CDS', 'CH', 'E', 'IL','JPP', 'L', 'MAS',
            'MPT','NC', 'PAN', 'PCP/PEV/CDU', 'PCTP/MRPP', 'PPD/PSD',
            'PPD/PSD/CDS-PP', 'PPD/PSD/CDS-PP/PPM-AD', 'PPM', 'PS',
            'PTP', 'RIR', 'VP']

# Extrai dados da primeira tabela do ficheiro pdf
resultados_01 = df[0].loc[df[0]['Unnamed: 1'] == 'Número']
resultados_01.columns = colunas

# Extrai dados da segunda tabela do ficheiro pdf
resultados_02 = df[1].loc[df[1]['Unnamed: 2'] == 'Número'].dropna(axis=1)
resultados_02.columns = colunas

# Extrai dados da terceira tabela do ficheiro pdf
resultados_03 = df[2].loc[df[2]['Unnamed: 1'] == 'Número']
resultados_03.columns = colunas

# Junta as tabelas
df_votos = pd.concat([resultados_01, resultados_02, resultados_03])

# Elimina a coluna 'Número'
df_votos = df_votos.drop(columns=['Número'])

# Reseta o indice e altera o nome das linhas
df_votos = df_votos[4:].reset_index(drop=True)
df_votos['Partido'] = partidos

# Substitui o caracter '.' por ''
df_geral[df_geral.columns[1:]] = df_geral[df_geral.columns[1:]].apply(lambda x: x.str.replace('.', ''))
df_votos[df_votos.columns[1:]] = df_votos[df_votos.columns[1:]].apply(lambda x: x.str.replace('.', ''))

# Substitui o caracter '–' por '0'
df_votos[df_votos.columns[1:]] = df_votos[df_votos.columns[1:]].apply(lambda x: x.str.replace('–', '0'))

# Altera o tipo de dados
df_geral[df_geral.columns[1:]] = df_geral[df_geral.columns[1:]].astype(int)
df_votos[df_votos.columns[1:]] = df_votos[df_votos.columns[1:]].astype(int)

# Cria ficheiro '.json' com os resultados
df_votos.to_json('../data/resultados_2022.json', orient='records')
