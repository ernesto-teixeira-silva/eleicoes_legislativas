import streamlit as st
import json
import pandas as pd
import plotly.express as px

######################################### CONFIGURAÇÕES #####################################

st.set_page_config(page_title="Eleições Legislativas 2024")

# Chama o ficheiro style.css
with open('./static/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Definição de cores
cores = {   'PS': 'rgb(244, 54, 116)',
            'PPD/PSD': 'rgb(241, 139, 53)',
            'PPD/PSD/CDS-PP': 'rgb(241, 139, 53)',
            'PPD/PSD/CDS-PP/PPM-AD': 'rgb(241, 139, 53)',
            'CH': 'rgb(45, 54, 87)',
            'PCP/PEV/CDU': 'rgb(4, 60, 135)',
            'IL': 'rgb(34, 194, 254)',
            'BE': 'rgb(11, 11, 11)',
            'L':'rgb(90, 181, 102)',
            'PAN': 'rgb(144, 204, 197)'
        }

##################################### CARREGAMENTO DOS DADOS #################################

# Define funcões
@st.cache_data
def carregar_eleitos():
    with open('./data/eleitos_2022.json', 'r') as ficheiro:
        eleitos2022_dic = json.load(ficheiro)
    df = pd.DataFrame(eleitos2022_dic)
    return df

@st.cache_data
def carregar_circulos():
    circulos = carregar_eleitos().columns
    return circulos

@st.cache_data
def carregar_resultados():
    with open('./data/resultados_2022.json', 'r') as ficheiro:
        resultados = json.load(ficheiro)
    df = pd.DataFrame(resultados)
    return df

@st.cache_data
def carregar_numMandatos2024():
    with open('./data/numero_deputados_2024.json', 'r') as ficheiro:
        res = json.load(ficheiro)
    df = pd.DataFrame(res).set_index('circulo').to_dict()['nr_deputados']
    return df


# Carrega circulos, eleitos e votos
df_circulos = carregar_circulos()
df_eleitos = carregar_eleitos()
df_votos = carregar_resultados()
df_mandatos = carregar_numMandatos2024()

#################################### APRESENTAÇÃO DA APP #####################################

with st.container():
    st.markdown("<h1 style='text-align: center;'>Eleições Legislativas 2024</h1><br><br>", unsafe_allow_html=True)
    #st.subheader("Dashboard Eleitos em 2022")
    """Com esta app é possivel simular o número de mandatos a eleger por círculo editando o formulário **votação** na secção **Simulação de votação 2024**."""
    """Selecionando círculo, a app mostrará por defeito no formulário **votação** os resultados referente às **Eleições Legislativas de 2022** permitindo ao utilizador poder editá-los."""
     
    """Automáticamente, é possivel visualizar o número de deputados a eleger por partido para o círculo selecionado."""

    """Em complemento é também possivel observar os quocientes ordenados, apurados pelo **Método da média mais alta de Hondt**, que corresponde à forma de apuramento do número de deputados eleitos por círculo eleitoral utilizado no [Sistema Eleitoral Português](https://www.parlamento.pt/Parlamento/Paginas/SistemaEleitoral.aspx)"""


    st.write("Código fonte em: [https://github.com/ernesto-teixeira-silva](https://github.com/ernesto-teixeira-silva)")

st.write("---")

#################################### FILTROS DE PESQUISA #####################################

# Filtro de pesquisa
circulo = st.selectbox("Selecione o distrito", df_circulos, index=7) # Por defeito aparece o circulo de Faro

st.write("---")

#################################### DATAFRAMES FILTRADOS #####################################

# Dataframe com número de eleitos em 2022 por partido e filtrado por círculo
df_eleitos_filtered = df_eleitos[circulo]
df_eleitos_filtered = df_eleitos_filtered.loc[df_eleitos_filtered > 0]

# Número de deputados a eleger por círculo em 2022
mandatos = df_mandatos[circulo]

# Dataframe com número de votos em 2022 por paritdo e filtrado por círculo
df_votos_filtered = df_votos[['Partido', circulo]].set_index('Partido')
df_votos_filtered = df_votos_filtered.sort_values(circulo, ascending=False)
df_votos_filtered = df_votos_filtered.head(8)

################################# SIMULAÇÃO RESULTADOS 2024 ###################################

# Titulo da seccão
st.markdown("<h2 style='text-align: center;'>Simulação da votação 2024</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'> Votos -> Mandatos</p>", unsafe_allow_html=True)

st.write(mandatos)

col1, col2, col3 = st.columns([2, 4, 2])

# Cria e apresenta o dicionários com a votação editada
with col1:
    st.subheader("Votos")
    df_votos_edited = st.data_editor(df_votos_filtered, num_rows="dynamic")
    dic_votos_edited = df_votos_edited.to_dict()[circulo]

# Cria dataframe com quocientes ordenados e apresenta
with col3:
    st.subheader("Quocientes")
    dic_quocientes = {}
    partidos = dic_votos_edited.keys()
    for partido in partidos:
        votos = dic_votos_edited[partido]
        quocientes = [int(votos / x) for x in range(1, mandatos +1)]
        dic_quocientes[partido] = quocientes

    df_quocientes_ordenados = pd.DataFrame(dic_quocientes)
    df_quocientes_ordenados = pd.DataFrame(df_quocientes_ordenados.stack(), columns=['Quocientes']).reset_index().sort_values('Quocientes', ascending=False).head(mandatos)
    df_quocientes_ordenados = df_quocientes_ordenados.rename(columns={'level_1': 'Partido'}).drop('level_0', axis=1)
    st.dataframe(df_quocientes_ordenados.set_index('Partido'))

# Apresenta o número de mandatos a eleger por partido
with col2:
    st.subheader("Mandatos")  
    nr_deputados = df_quocientes_ordenados.groupby('Partido')['Partido'].count().sort_values(ascending=False)
    fig = px.bar(   nr_deputados,
                    text=nr_deputados.values,
                    color=nr_deputados.index,
                    color_discrete_map=cores,
                    orientation='v')
   
    fig.update_traces(texttemplate='%{text}', textposition='outside')
    fig.update_layout(showlegend=False, hovermode=False) 
    fig.update_xaxes(title = None) 
    fig.update_yaxes(visible = False) 
    st.plotly_chart(fig, theme=None, use_container_width=True)
    


st.write("---")

####################################### RESULTADOS 2022 ###########################################

# Titulo da seccão
st.markdown("<h2 style='text-align: center;'>Resultados 2022</h2>", unsafe_allow_html=True)

# Dividir a tela em duas colunas
col1, col2= st.columns([3, 1])

# Plot eleitos
with col1:

    fig = px.bar(   df_eleitos_filtered,
                    text=df_eleitos_filtered.values,
                    color=df_eleitos_filtered.index,
                    color_discrete_map=cores,
                    orientation='h')
    fig.update_layout(title = "Mandatos<br>- " + circulo + ' -', title_x=0.5)
    fig.update_traces(texttemplate='%{text}', textposition='outside')
    fig.update_layout(showlegend=False, hovermode=False) 
    fig.update_yaxes(title = None) 
    fig.update_xaxes(visible = False) 
    st.plotly_chart(fig, theme=None, use_container_width=True, width=300)

# Plot resultados (votos)
with col2:
    st.write('Votos')
    st.write('')

    st.write(df_votos_filtered)

st.write("---")