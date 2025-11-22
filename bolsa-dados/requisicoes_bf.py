import requests
import csv
import os
import time

def obter_municipios(uf):
    url = f"https://servicodados.ibge.gov.br/api/v1/localidades/estados/{uf}/municipios"
    response = requests.get(url)

    if response.status_code == 200:
        municipios = response.json()
        return [
            {
                "id_municipio": municipio['id'],
                "nome_municipio": municipio['nome'],
                "id_microrregiao": municipio['microrregiao']['id'],
                "nome_microregiao": municipio['microrregiao'].get('nome', "Não informado")
            }
            for municipio in municipios
        ]
    else:
        print(f"Erro ao acessar a API do IBGE: {response.status_code}")
        return []

def obter_beneficios(municipio_id, ano_mes):
    # url = f"https://api.portaldatransparencia.gov.br/api-de-dados/bolsa-familia-por-municipio?mesAno={ano_mes}&codigoIbge={municipio_id}&pagina=1"
    # url = f"https://api.portaldatransparencia.gov.br/api-de-dados/auxilio-brasil-por-municipio?mesAno={ano_mes}&codigoIbge={municipio_id}&pagina=1"
    # url = f"https://api.portaldatransparencia.gov.br/api-de-dados/novo-bolsa-familia-por-municipio?mesAno={ano_mes}&codigoIbge={municipio_id}&pagina=1"
    url = f"https://api.portaldatransparencia.gov.br/api-de-dados/bpc-por-municipio?mesAno={ano_mes}&codigoIbge={municipio_id}&pagina=1"
    
    headers = {
        "chave-api-dados": "c3a4d060f5e621198572ce60034d8884"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        try:
            data = response.json()
            if data:
                print(f"Benefícios para município ID {municipio_id}, período {ano_mes} recebidos com sucesso.")
                return [
                    {
                        "ano_mes_referencia": item.get('dataReferencia'),
                        "valor_pago": item.get('valor'),
                        "total_beneficiarios": item.get('quantidadeBeneficiados')
                    }
                    for item in data
                ]
            else:  # Em caso da requisição retornar vazia
                print(f"Nenhum dado encontrado para município ID {municipio_id}, período {ano_mes}.")
                return []
        except requests.JSONDecodeError as e:
            print(f"Erro ao decodificar JSON para município ID {municipio_id}, período {ano_mes}: {e}")
            return []
    else:
        print(f"Erro na requisição para município ID {municipio_id}, período {ano_mes}: {response.status_code} - {response.text}")
        return []

def inicializar_csv(caminho, campos):
      print(f"Inicializando arquivo CSV em: {caminho}")
      with open(caminho, mode='w', newline='', encoding='utf-8') as file:
          writer = csv.DictWriter(file, fieldnames=campos)
          writer.writeheader()

def salvar_csv_incremental(dado, caminho):  # Salva dados no arquivo
    with open(caminho, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=dado.keys())
        writer.writerow(dado)

if __name__ == "__main__":
    estado = 43  # Número do estado no IBGE
    diretorio = r"C:\Users\loren\OneDrive\Área de Trabalho\bolsa-dados"  # Diretório onde se deseja salvar o arquivo
    caminho_csv = os.path.join(diretorio, "beneficios_municipios.csv")
    campos_csv = ["id_municipio", "nome_municipio", "id_microregiao", "nome_microregiao", "ano_mes_referencia", "valor_pago", "total_beneficiarios"]

    # Verifica se o diretório existe; se não, cria o diretório
    if not os.path.exists(diretorio):
        os.makedirs(diretorio)

    # Inicializa o arquivo CSV
    inicializar_csv(caminho_csv, campos_csv)

    print("Buscando municípios do estado...")
    municipios = obter_municipios(estado)

    if municipios:
        print(f"Foram encontrados {len(municipios)} municípios no estado RS.")
        print("Iniciando coleta de benefícios...\n")

        requisicoes_por_minuto = 170  # Limita as requisições há no máximo de 180 requisições
        intervalo = 60 / requisicoes_por_minuto  # Tempo de pausa entre requisições

        for municipio in municipios:
            print(f"Processando município: {municipio['nome_municipio']} (ID: {municipio['id_municipio']})")
            for ano in range(2019, 2025):
                for mes in range(1, 13):
                    # if ano == 2024 and mes > 2:
                    #     break
                    ano_mes = f"{ano}{mes:02d}"
                    beneficios = obter_beneficios(municipio['id_municipio'], ano_mes)

                    for beneficio in beneficios:  # Iterar sobre os itens da lista retornada
                        dado = {
                            "id_municipio": municipio['id_municipio'],
                            "nome_municipio": municipio['nome_municipio'],
                            "id_microregiao": municipio['id_microrregiao'],
                            "nome_microregiao": municipio.get('nome_microrregiao'),
                            "ano_mes_referencia": beneficio.get('ano_mes_referencia'),
                            "valor_pago": beneficio.get('valor_pago'),
                            "total_beneficiarios": beneficio.get('total_beneficiarios')
                        }
                        salvar_csv_incremental(dado, caminho_csv)
                    time.sleep(intervalo)  # Pausa entre as requisições

        print(f"Processo finalizado. Dados disponíveis em {caminho_csv}")
    else:
        print("Não foi possível obter os municípios.")
