from typing import final
import os

#bot-related

import logging


from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from googleBooks import googleBooks
from messages import messagesToUser

#this token identifies the bot with a unique credential, do not mess up with that since it can expose your bot token and let people use your unique bot without your permit
BOT_TOKEN = os.environ.get("BOT_TOKEN")
#BOT_USERNAME : final = os.environ[BOT_USERNAME]


## MISC COMMANDS

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE ) -> None:
    "Triggers with /start, not when the bot goes online"
    user = update.effective_user
    await update.message.reply_text(f"Olá {user['username']}, eu trabalho com livros clássicos brasileiros atualmente em domínio público, te entregando uma sinópse e o livro em PDF, se requisitado, adquirido de fontes legais. Insira o comando /help para conhecer minhas funções")


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("/start - inicia o bot! \n /ajuda - mostra esse texto \n /sobre - mostra informações relevantes sobre mim mesma \n /creditos - informações sobre meu artesão \n /sinopse - Procura a sinopse de livros a partir da API do google Books \n /livro - faz o Download de um livro a partir da API do Googe Books ")


async def about(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Eu sou um bot produzido artesanalmente por José Lemos, feito para incentivar a leitura de clássicos e servir como projeto simples de webscrapping")


async def aboutDev(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:    
    await update.message.reply_text("José Lemos é Estudante e desenvolvedor Python/Django, confira mais em linkedin.com/in/lemosjose e github.com/lemosjose")

async def responseMisc(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Envie um comando válido! Para checar os comandos válidos, envie o comando /help")


    
    
def main() -> None:
    "truly starts the bot!!!"
    application = Application.builder().token(BOT_TOKEN).build()


    #handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("ajuda", help))
    application.add_handler(CommandHandler("sobre", about))
    application.add_handler(CommandHandler("creditos", aboutDev))
    application.add_handler(CommandHandler("sinopse", messagesToUser.sendSinopse))
    application.add_handler(CommandHandler("gemini", messagesToUser.sendGemini))
    application.add_handler(CommandHandler("livro", messagesToUser.sendDownloadLink))
    


    #reply to non-command messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responseMisc))


    #STOP WITH CTRL-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
    

