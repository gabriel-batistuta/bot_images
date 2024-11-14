# bot_images

Um bot que te envia imagens pelo seu termo de busca

![cute cat](assets/example.jpg)

```bash
touch keys.json
echo '{
    "TELEGRAM_TOKEN":"..",
    "BING_API_KEY":"...",
    "BING_ENDPOINT":"https://api.bing.microsoft.com/v7.0/images/search",
    "GOOGLE_API_KEY":"...",
    "GOOGLE_CUSTOM_SEARCH_CX":"..."
}' > keys.json
```

Bibliotecas usadas:
- [requests](https://github.com/psf/requests)
- [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)
- [Google-Images-Search](https://github.com/arrrlo/Google-Images-Search)

Ferramentas usadas:
- [Google Custom Image Search API](https://developers.google.com/custom-search/v1/overview?hl=pt-br)
- [Bing Image Search API](https://www.microsoft.com/en-us/bing/apis/bing-image-search-api)
- [Telegram API](https://core.telegram.org/api)