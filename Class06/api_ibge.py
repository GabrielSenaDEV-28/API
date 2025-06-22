import requests
from pprint import pprint
import pandas as pd
import streamlit as st

url = (f'https://servicodados.ibge.gov.br/api/v1/localidades/estados')
params = {
    'view': 'nivelado',
}
def make_request(url, params=None):
    answer = requests.get(url, params=params)
    try:
        answer.raise_for_status()
    except requests.HTTPError as error:
        print(f'Erro no request: {error}')
        result = None
    else:
        result = answer.json()
        return result
    
def get_name_by_decade(nome):
    url = (f'https://servicodados.ibge.gov.br/api/v2/censos/nomes/{nome}')
    decade_data = make_request(url)
    if not decade_data:
        return {}
    dict_decade = {}
    for data in decade_data[0]['res']:
        decade = data['periodo']
        quantity = data['frequencia']
        dict_decade[decade] = quantity    
    return dict_decade

def main():
    st.title('Web App Nomes')
    st.write(f'Dados do IBGE: (https://servicodados.ibge.gov.br/api/docs/nomes?versao=2)')
    nome = st.text_input('Digite um nome: ')
    if not nome:
        st.stop()

    dict_decade = get_name_by_decade(nome)
    if not dict_decade:
        st.warning(f'Nenhum dado encontrado')
        st.stop()
    df = pd.DataFrame.from_dict(dict_decade, orient='index')
    col01, col02 = st.columns([0.3, 0.7])
    with col01:
        st.write('Frequência por decada')
        st.dataframe(df)
    with col02:
        st.write('Evolução ao longo dos anos')
        st.line_chart(df)
    
if __name__ == '__main__':
        main()
