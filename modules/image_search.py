from google_images_search import GoogleImagesSearch
import os
import json
import requests
from PIL import Image
from io import BytesIO

with open('keys.json', 'r') as file:
    keys = json.load(file)
gis = GoogleImagesSearch(keys['GOOGLE_API_KEY'], keys['GOOGLE_CUSTOM_SEARCH_CX'])

# subscription_key = os.environ['BING_SEARCH_V7_SUBSCRIPTION_KEY']
# endpoint = os.environ['BING_SEARCH_V7_ENDPOINT'] + "/bing/v7.0/search"

BING_API_KEY=keys['BING_API_KEY']
BING_ENDPOINT=keys['BING_ENDPOINT']


def get_image_format_from_url(image_url):
    try:
        # Faz o download da imagem usando requests
        response = requests.get(image_url)
        if response.status_code != 200:
            return None
        response.raise_for_status()  # Levanta um erro se a requisição falhar
        
        # Abre a imagem diretamente da resposta em bytes usando Pillow
        image = Image.open(BytesIO(response.content))
        
        # Retorna o formato da imagem
        return image.format.lower()  # O formato será algo como 'jpeg', 'png', 'gif', etc.
    
    except requests.exceptions.RequestException as e:
        raise e
    except Exception as e:
        raise e

def search_images_bing(query):
    headers = {
        'Ocp-Apim-Subscription-Key': BING_API_KEY
    }
    params = {
        'q': query,
        'count': 5,  # Número de imagens a buscar
        'safeSearch': 'Off',  # Opções: Off, Moderate, Strict
        # 'imageType': 'AnimatedGif', # Opções: AnimatedGif, Clipart, Line, Photo, Transparent
        'color':'ColorOnly', # Opções: ColorOnly, Monochrome, Color
        'size':'Large', # Opções: small, Medium, Large, Wallpaper
        'license': 'Any', # Opções: Any, Public, Share, ShareCommercially, Modify, ModifyCommercially
        # 'freshness': 'Week' # Opções: Day, Week, Month
    }
    response = requests.get(BING_ENDPOINT, headers=headers, params=params)
    response.raise_for_status()  # Levanta uma exceção para códigos de status de erro
    search_results = response.json()
    images = []
    save_dir = 'images'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    # Baixa e salva cada imagem
    for i, result in enumerate(search_results['value']):
        image_url = result['contentUrl']
        file_extension = get_image_format_from_url(image_url)
        if file_extension is None:
            continue
        # file_extension = result['encodingFormat']
        file_name = f"{query}_{i}.{file_extension}"
        file_path = os.path.join(save_dir, file_name)
        
        # Verifica e adiciona sufixo para evitar sobrescrita
        counter = 1
        while os.path.exists(file_path):
            file_name = f"{query}_{i}_{counter}.{file_extension}"
            file_path = os.path.join(save_dir, file_name)
            counter += 1
        
        # Baixa e salva a imagem
        try:
            image_data = requests.get(image_url).content
            with open(file_path, 'wb') as img_file:
                img_file.write(image_data)
            images.append(file_path)
        except Exception as e:
            print(f"Erro ao baixar a imagem: {e}")
    
    return images

_search_params = {
    'q': '...',
    'num': 10,
    'fileType': 'jpg|gif|png|jpeg',
    'rights': 'cc_publicdomain|cc_attribute|cc_sharealike|cc_noncommercial|cc_nonderived',
    'safe': 'off', ##
    # 'imgType': 'clipart|face|lineart|stock|photo|animated', ##
    # 'imgSize': 'huge|icon|large|medium|small|xlarge|xxlarge|imgSizeUndefined', ##
    # 'imgDominantColor': 'black|blue|brown|gray|green|orange|pink|purple|red|teal|white|yellow|imgDominantColorUndefined', ##
    # 'imgColorType': 'color|gray|mono|trans|imgColorTypeUndefined' ##
}

def search_images_google(query):
    # Lista para armazenar os caminhos das imagens salvas
    images = []
    save_dir = 'images'  # Diretório onde as imagens serão salvas

    _search_params['q'] = query

    # Cria o diretório de imagens se ele não existir
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    gis.search(search_params=_search_params, path_to_dir=save_dir, custom_image_name=query)

    for file in os.listdir(save_dir):
        if file.startswith(query):  # Verifica se o arquivo começa com o nome da consulta
            base_name, ext = os.path.splitext(file)
            new_name = base_name
            counter = 1
            
            # Adiciona um contador se já houver uma imagem com o mesmo nome
            while os.path.exists(os.path.join(save_dir, f"{new_name}{ext}")):
                new_name = f"{base_name}{counter}"
                counter += 1
            
            # Renomeia o arquivo, se necessário, e adiciona o caminho à lista
            final_path = os.path.join(save_dir, f"{new_name}{ext}")
            os.rename(os.path.join(save_dir, file), final_path)
            images.append(final_path)

    return images