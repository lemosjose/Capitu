from telegram import Update
from typing import final
import requests
import json
import os 
import google.generativeai as ai

#configurações gerais de permissão e API_KEY, verifique sempre seu .env local.
API_KEY = os.environ.get('API_KEY_BOOKS')

ai.configure(api_key=os.environ.get('GEMINI_KEY'))

model = ai.GenerativeModel("gemini-1.5-flash")

class googleBooks:


    def forceGemini(book, author) -> str:
        sinopse = model.generate_content(f"Gere uma sinópse sucinta para o livro {book}")
        
        if not sinopse.text:
            return f"Não foi possível gerar uma sinopse para o livro {book} com o google gemini"

        return sinopse.text
        
    
    def getSinopse(book, author) -> str:
        #aceita texto capitalizado e/ou mais bagunçado que o normal
        try:
            if not author:
                fetch = requests.get(f"https://www.googleapis.com/books/v1/volumes?q={book}&key={API_KEY}")
            else:
                 fetch = requests.get(f"https://www.googleapis.com/books/v1/volumes?q={book}+inauthor:{author}&key={API_KEY}")
            fetch.raise_for_status()

            jsonTarget = json.loads(fetch.text) 
            
        except requests.exceptions.ConnectionError:
                return f"Não consegui procurar a sinopse para o livro {book}"

        #deixa o gemini cuidar dos trolls
        if "items" not in jsonTarget:
            return (model.generate_content(f"Gere uma sinópse para o livro {book}, se não conseguir achar um livro minimamente conhecido com esse nome, diga que não encontrou nada e o título sequer tem resultado na api do google books.")).text+"\n Você provavelmente está me tentando me trollar, né?"
            
        for i in jsonTarget["items"]:
            try:
                sinopse = i["volumeInfo"]["description"]
                break
            except (KeyError, IndexError):
                continue 

        #obtém via gemini se não for possível obter diretamente via google books
        
        if not sinopse:
            sinopse = (model.generate_content(f"Gere uma sinopse para o livro {book}")).text+"\n gerado via google Gemini"
             
        return sinopse
        
    
    #infelizmente existe uma autenticação (e as vezes um captcha) ao realizar o download, então vamos nos conter com apenas o link de Download 
    def getDownloadLink(book, author) -> str:
        try:
            fetch = requests.get(f"https://www.googleapis.com/books/v1/volumes?q={book}&key={API_KEY}", stream=True)
            fetch.raise_for_status()

            jsonTarget = json.loads(fetch.text)
        except requests.exceptions.ConnectionError:
            return(f"Não foi possível realizar o download do livro {book}")


       #EPUB é o formato "definitivo" para ebooks, o código vai parar se um link para o epub for encontrado
        for i in jsonTarget["items"]:
            try:
                downloadLink =  i["accessInfo"]["epub"]["downloadLink"]
                return downloadLink
            except(KeyError, IndexError):
                continue

        for j in jsonTarget["items"]:
            try:
                downloadLink = i["accessInfo"]["pdf"]["downloadLink"]
                return downloadLink
            except(KeyError, IndexError):
                continue

        return f"Link de download não encontrado para o livro {book}"






    
    
