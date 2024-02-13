import json
import pandas as pd

# Carrega o ficheiro com os resultados de 2022 e o ficheiro com o número de deputados a eleger
df_resultados = pd.read_json('../data/resultados_2022.json')
df_num_deputados = pd.read_json('../data/numero_deputados_2022.json')

# Trata a coluna 'circulo' do dataframe `df_num_deputados` para haver correspondência com df_resultados
df_num_deputados['circulo'] = df_num_deputados['circulo'].str.replace('Madeira', 'RA Madeira')
df_num_deputados['circulo'] = df_num_deputados['circulo'].str.replace('Açores', 'RA Açores')

# Cria dicionário para o número de deputados a eleger
dic_num_deputados = df_num_deputados.set_index('circulo').to_dict()['nr_deputados']

################################# Dataset ELEITOS_2022.json ###################################

dic_eleitos2022 = {}

# itera todos os circulos constantes no dicionário `dic_num_deputados`
for circulo, nr_deputados in dic_num_deputados.items():

    circulo = circulo
    nr_deputados = nr_deputados

    # Cria um dataframe para cada circulo com os resultados por partido
    df_eleitos_res = df_resultados[['Partido', circulo]].loc[df_resultados[circulo] != 0]

    # Para cada circulo cria um dicionário vazio para ir adicionando o nr de eleitos por partido ao dicionário dic_eleitos2022
    dic = {}

    # Para cada partido cria o dataframe com os quocientes ordenados 
    for index, partido in df_eleitos_res.iterrows():
        # Para cada partido calcula os quocientes (método da média mais alta de Hondt)
        part = partido[0]
        votos = partido[1]
        quocientes = [ votos/divisor for divisor in range(1, nr_deputados + 1)]

        # Cria dataframe com os quocientes
        dic[part] = quocientes
        df_quocientes = pd.DataFrame(dic)
        
        # Cria dataframe com quocientes ordenados
        df_quocientes_ordenado= pd.DataFrame(df_quocientes.stack(), columns=['votos']).reset_index().sort_values('votos', ascending=False).head(nr_deputados)

    # Para cada circulo cria um dicionário com os mandatos eleitos por partido
    dic_eleitos2022[circulo] = df_quocientes_ordenado.groupby('level_1')['votos'].count().sort_values(ascending = False).to_dict()
    

# Cria ficheiro '.json' com o número de deputados eleitos por círculo
with open('../data/eleitos_2022.json', "w") as ficheiro:
    json.dump(dic_eleitos2022, ficheiro)