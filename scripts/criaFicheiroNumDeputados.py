import tabula
import pandas as pd

# Escolha o ano do dataset a construir
ano = 2024

# Lê o pdf
df = tabula.read_pdf('../docs/numero_deputados_circulo_' + str(ano) + '.pdf', pages='all')

# Extrai a informaçao referente à primeira tabela
df = df[0]

# Trata a coluna com o nome dos círculos (Nome da coluna diferente em cada um dos anos)
try:
    df['Círculos eleitorais'] = [x.split('.')[0].rstrip() for x in df['Círculos eleitorais'].to_list()]
except:
    df['Círculos Eleitorais'] = [x.split('.')[0].rstrip() for x in df['Círculos Eleitorais'].to_list()]

# Renomeia as colunas
df.columns = 'circulo nr_eleitores nr_deputados'.split()

# Retira a linha total
df = df.loc[df.circulo != 'Total']

# Trata a coluna nr_eleitores
df['nr_eleitores'] = df['nr_eleitores'].str.replace(' ', '').astype(int)

# Cria ficheiro '.json' com o número de deputados a eleger por círculo
df[['circulo', 'nr_deputados']].to_json('../data/numero_deputados_' + str(ano) + '.json', orient='records')




