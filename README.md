# OBJETIVO

Este projeto tem como objetivo simular o número de mandatos eleitos por círculo, atendendo ao número de votos obtidos por cada partido.

Selecionando o círculo, a app mostra os resultados referente às **Eleições Legislativas de 2022** e permite ao utilizador editar os mesmos e efetuar uma simulação dos mandatos a eleger para o ano de 2024.

# Fonte dos dados

Os datsets utilizados neste projeto foram criados tendo por base a informação oficial publicada no Diário da República pela **Comissão Nacional de Eleições** referente às  [Eleições Legislativas de 2022](https://www.cne.pt/sites/default/files/dl/2022ar_mapa_oficial_resultados.pdf), bem como ao número de deputados a eleger para as eleiçoes de [2022](https://www.cne.pt/sites/default/files/dl/ar2022-mapa-deputados-1-c-2021.pdf) e [2024](https://www.cne.pt/sites/default/files/dl/eleicoes/2024_ar/docs_geral/2024_ar_mapa_deputados.pdf). Informação constante na pasta ``.\docs\``.

Na construção dos datasets foi explorado o **Método da média mais alta de Hondt** que corresponde à forma de apuramento do número de deputados eleitos por círculo eleitoral utilizado no [Sistema Eleitoral Português](https://www.parlamento.pt/Parlamento/Paginas/SistemaEleitoral.aspx).

# Estrutura de Pastas e Ficheiros

- `.venv/`: Contém o ambiente virtual criado para o projeto.
- `data/`: Contém os datasets criados e que serviram de base ao projeto (código fonte em ``scripts/``):
    - `eleitos_2022.json`: Mandatos eleitos por círculo e partido em 2022.
    - `numero_deputados_2022.json`: Mandatos a eleger por círculo em 2022.
    - `numero_deputados_2024.json`: Mandatos a eleger por círculo em 2024.
    - `resultados_2022.json`: Resultados das eleições de 2022 (votos por partido e círculo)
- `docs/`: Contém os dados oficiais fonte dos datatasets criados (em `data/`)
- `scripts/`: Contém scripts auxiliares para tarefas de construção dos datasets (em `data/`).
- `static/`: Contém os recursos estáticos, como ficheiros ``.css``, etc.
- `tests/`: Contém notebook para explorar a forma de apuramento do número de deputados eleitos por círculo eleitoral utilizado no sistema eleitoral português - **Método da média mais alta de Hondt**


# Executar a aplicação
Comece por instalar as dependências e só depois inicie a aplicação.

## Instalar as dependências

1. No terminal **navegue até à pasta do projeto**
2. **Crie um ambiente virtual**: ```python -m venv <nome-do-ambiente>```
3. **Ative o ambiente virtual**: ```..\<nome_do_projeto>\Scripts\activate.bat```
4. **Instale as dependências**: Na raiz do projeto e com o ambiente virtual activado execute o comando ```(<nome-do-ambiente>)..\<nome_do_projeto>\pip install -r requirements.txt```

## Iniciar a aplicação
Com o ambiente virtual ativado e na pasta raiz do projeto execute o comando: ```streamlit run app.py```