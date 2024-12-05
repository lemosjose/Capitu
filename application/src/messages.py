from typing import final
import json
from googleBooks import googleBooks

from telegram import Update
from telegram.ext import ContextTypes

import requests

class messagesToUser:

    async def sendGemini(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        if len(context.args) < 2:
            sinopse = googleBooks.forceGemini(context.args[0], "")
        else:
            sinopse = googleBooks.forceGemini(context.args[0], context.args[1])

        await update.message.reply_text(f"Sinópose para o livro {context.args[0]}: \n {sinopse} \n"+"\n Gerado via google gemini")
    
    async def sendSinopse(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        if len(context.args) < 2:
            sinopse = googleBooks.getSinopse(context.args[0], "")
        else:
            sinopse = googleBooks.getSinopse(context.args[0], context.args[1])

        await update.message.reply_text(f"Sinópose para o livro {context.args[0]}: \n {sinopse} \n")

    async def sendDownloadLink(update: Update, context: ContextTypes.DEFAULT_TYPE):
                
        if len(context.args) == 1:
            downloadLink = googleBooks.getDownloadLink(context.args[0], "")
        else:
            downloadLink = googleBooks.getDownloadLink(context.args[0], context.args[1])

        await update.message.reply_text(f"{downloadLink}")

            
        

        
