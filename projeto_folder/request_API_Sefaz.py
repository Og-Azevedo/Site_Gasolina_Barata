import json
import requests
from dotenv import load_dotenv
import os

lista_bairros_mcz = ['AL 101-SUL', 'ALTO DA SAUDADE', 'ANTARES', 'ANTONIO LINS DE SOUZA', 'BARRO DURO', 'BOM PARTO', 'CENTRO', 'CIDADE ALTA', 'CIDADE UNIVERSITARIA', 'CLIMA BOM', 'CRUZ DAS ALMAS', 'FAROL', 'FEITOSA', 'FRANCES', 'GRUTA DE LOURDES', 'ILHA DE SANTA RITA', 'JACARECICA', 'JACINTINHO', 'JARAGUA', 'JARDIM PETROPOLIS', 'JATIUCA', 'JOSE PAULINO', 'LEVADA', 'MANGABEIRA', 'MANGABEIRAS', 'PAJUCARA', 'PETROPOLIS', 'PINHEIRO', 'POCO', 'PONTA GROSSA', 'PONTA VERDE', 'POVOADO DO FRANCES', 'PRADO', 'PRIMAVERA', 'RIACHO DOCE', 'RIO NOVO', 'SANTA AMELIA', 'SANTA LUCIA', 'SANTO AMARO', 'SANTOS DUMONT', 'SAO JORGE', 'SERRARIA', 'TAB DO MARTINS', 'TAB DOS MARTINS', 'TAB.DOS MARTINS', 'TABULEIRO DO MARTINS', 'TABULEIRO DOS MARTINS', 'TRAPICHE DA BARRA', 'VERGEL DO LAGO', 'ZONA URBANA']

load_dotenv()
API_KEY = os.getenv("API_KEY")


def fazer_request():
    # BUSCAR OS PRECOS DA GASOLINA
    headers = {'appToken': API_KEY, 'content-type': 'application/json'}
    payload = {
        "codTipoCombustivel": "1",
        "dias": 2,
        "latitude": -9.6432331,
        "longitude": -35.7190686,
        "raio": 15
    }
    precos = requests.post(url='http://api.sefaz.al.gov.br/sfz_nfce_api/api/public/consultarPrecosCombustivel',
                           headers=headers, data=json.dumps(payload))

    return precos.json()

def organizar_request():

    postos_dic = fazer_request()
    list_postos_organizada = []


    for posto in postos_dic:
        # print(posto)
        dic_modelo = {'preco': "", 'bairro': "", 'link': "",'tel':""}
        maps = '{},{},{}'.format(posto['nomLogradouro'],posto['numImovel'],posto['nomBairro'])
        maps_link_limpo = maps.replace(' ','+')

        dic_modelo['preco'] = 'R${:5.3f}'.format(posto['valUltimaVenda'])
        dic_modelo['bairro'] = posto['nomBairro']
        dic_modelo['link'] = f'https://www.google.com.br/maps/place/{maps_link_limpo}'
        dic_modelo['tel'] = posto['numTelefone']

        list_postos_organizada.append(dic_modelo)

        # range += 1
        # if range >=10:
        #     break

    return list_postos_organizada


def filtrar(lista_postos, bairro=''):

    lista_postos_filtrada =[]
    if bairro:
        for posto in lista_postos:
            if posto['bairro'] in bairro:
                lista_postos_filtrada.append(posto)
        return lista_postos_filtrada[:10]
    else:
        return lista_postos[:10]



