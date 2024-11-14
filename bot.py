import telebot
import modules as md 
import json

with open('keys.json', 'r') as file:
    keys = json.load(file)
TELEGRAM_TOKEN = keys['TELEGRAM_TOKEN']
GOOGLE_API_KEY = keys['GOOGLE_API_KEY']
bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Olá! Envie um termo de busca e eu vou retornar imagens sobre ele!")

@bot.message_handler(func=lambda message: True)
def send_image(message):
    query = message.text
    chat_id = message.chat.id
    bot.reply_to(message, 'Buscando imagens...')
    images = []
    images_google = md.search_images_google(query)
    images_bing = md.search_images_bing(query)
    images.extend(images_google)
    images.extend(images_bing)
    if images:
        for image_path in images:
            with open(image_path, 'rb') as image_file:
                print(image_path)
                bot.send_photo(chat_id, image_file)
        bot.reply_to(message, f'Todas as imagens encontradas com o termo "{query}" foram enviadas!')
        print('Imagens enviadas!')
        md.erase_folder()
    else:
        bot.reply_to(message, "Desculpe, não consegui encontrar uma imagem para esse termo.")

if __name__ == '__main__':
    print("Bot iniciado!")
    bot.polling()