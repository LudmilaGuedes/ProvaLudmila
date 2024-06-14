import pandas as pd
import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()
from meuPacote.atletas import getAge
from meuPacote.atletas import getCountry
from meuPacote.atletas import getMedal
from meuPacote.email import enviar_email

BASE_DIR = str(Path(os.path.dirname(__file__)).parent)

def main():
    file = BASE_DIR + '/data/nomesAtletas.xlsx'
    df_excel = pd.read_excel(file)
    
    nomes = df_excel['nome'].tolist()

    colunas = ['nome', 'idade', 'pais', 'medalha']
    df = pd.DataFrame(columns=colunas)

    idades=[]
    paises=[]
    medalhas=[]

    for i in nomes:
        idade = getAge(i)
        idades += [idade]
    for i in nomes:
        pais = getCountry(i)
        paises+= [pais]
    for i in nomes:
        medalha = getMedal(i)
        medalhas += [medalha]
    
    df["nome"] = nomes
    df["idade"] = idades
    df["pais"] = paises
    df["medalha"] = medalhas
    print(df)

    df.to_excel(BASE_DIR + '/data/listaFinal.xlsx')

    #atletas acima de 30 anos que consquistaram medalhas de ouro 
    acima30 = df.query("medalha == 'Gold' and idade > 30.0")
    acima30 = acima30['nome'].tolist()
    print(acima30)

    #atletas dos estados unidos
    americanos = df.query("pais == 'United States' ")
    quantAmericanos = len(americanos)
    print(quantAmericanos)

    #mais velho 
    maisVelho = df['idade'].max()
    print(maisVelho)
    nomeMaisVelho = df.query("idade == 69")
    nomeMaisVelho = nomeMaisVelho['nome'].tolist()
    print(nomeMaisVelho)
    

    #paises que partiparam
    paisesParticipantes = list(set(df['pais']))
    paisesParticipantes = len(paisesParticipantes)

    usuario = os.environ.get("YAHOO_USER") 
    senha = os.environ.get("YAHOO_PASSWORD") 
    destinatario = 'guedesdf.lud@gmail.com'
    assunto = 'Prova AP2'
    mensagem = f"Os atletas com mais de 30 anos que conquistaram a medalha de ouro foram: {acima30}.\nOs USA ganharam {quantAmericanos} medalhas.\nO atleta mais velho que ganhou medalha foi {nomeMaisVelho} de {maisVelho} anos.\nNessa amostra contem {paisesParticipantes} pais que ganharam medalhas"
    
    print(mensagem)
    enviar_email(usuario, senha, destinatario, assunto, mensagem)
