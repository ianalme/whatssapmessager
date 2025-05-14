import requests
from datetime import datetime
import time
import os

def messagesprivate(number,message,image):
    url = 'http://localhost:6508/enviarindividual'
    payload = {
        'numero': number,
        'mensagem': message,
        'imagem':image
    }

    r = requests.post(url, json=payload)
    if r.ok:
        print('✅ Mensagem enviada com sucesso pelo Node.js!')
    else:
        print('❌ Falha ao enviar.')
    pass


# Grupos de whatssap----------------------------------------
def mandarfuncao(grupo, mensagem,imagem = False):
    url = 'http://localhost:6508/enviar'
    payload = {
        'grupo': grupo,
        'mensagem': mensagem,
        'imagem':imagem
    }

    r = requests.post(url, json=payload)
    if r.ok:
        print('✅ Mensagem enviada com sucesso pelo Node.js!')
    else:
        print('❌ Falha ao enviar.')
        


def verificamomento(line:str):
    check = False

    hora = str(datetime.now().hour).strip()
    data_hoje = datetime.today().strftime('%d/%m/%Y').strip()
    linha = str(line).split('&')
    data = linha[2].strip()
    horaprevista = linha[3].strip()

    #print(data,data_hoje,hora,horaprevista)
    
    if data_hoje == data:
        #print('é hoje')
        if hora == horaprevista:
            #print('é agora')
            check = True
    
    return check,linha

def marcar_linha(comparar_linha, caminho_arquivo = 'aniversario/programado.txt'):
    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        linhas = f.readlines()

    linhas_modificadas = []
    for linha in linhas:
        linha_sem_quebra = linha.rstrip('\n')
        if linha_sem_quebra in comparar_linha:
            linha_sem_quebra += ' #'
        linhas_modificadas.append(linha_sem_quebra + '\n')

    with open(caminho_arquivo, 'w', encoding='utf-8') as f:
        f.writelines(linhas_modificadas)

def lerprogramacao(type = 'grupo', programado = 'aniversario/programado.txt', mensagens = "aniversario/mensagens/", imagens = "aniversario/images/"):
    with open(programado, "r", encoding="utf-8") as arquivo:
        linhas = arquivo.readlines()
    for linha in linhas:
        #print(linha.strip())  # strip() tira o \n do final
        if '#' in linha:
            continue
        else:
            check,lista = verificamomento(linha.strip()) #check é se é a data atual, e lista é uma lista com os componentes
            
            if os.path.isfile(f"{mensagens}{lista[0]}") and os.path.isfile(f"{imagens}{lista[1]}"):
                print('Diretório correto de', lista[0].replace('.txt',''))
            else:
                print('erro com', lista[0].replace('.txt',''))
                
            if check == True:
                print(lista)
                with open(f'{mensagens}{lista[0]}', 'r', encoding='utf-8') as f:
                    conteudo = f.read()
                imagem = f'{imagens}{lista[1]}'
                #mandarfuncao('',conteudo)
                print(conteudo)
                
                
                if type == 'grupo':
                    mandarfuncao('DIAS & LIMA ⚜',conteudo,imagem=imagem)
                    #mandarfuncao('POSTS DE ANIVERSÁRIO DIAS E LIMA 🎂🎈',conteudo,imagem=imagem)
                    marcar_linha(linha)
                else:
                    messagesprivate(lista[4],conteudo,imagem)
                    marcar_linha(linha,caminho_arquivo=programado)
                
# Exemplo:
#mandarfuncao('POSTS DE ANIVERSÁRIO DIAS E LIMA 🎂🎈', 'Mensagem enviada do Python! 🚀','img/raquete.jpg')
#messagesprivate('556391164693','teste teste teste','img/raquete.jpg')

while True:
    lerprogramacao()
    lerprogramacao(type = 'privado',programado = 'privado/programado.txt', mensagens = "privado/mensagens/", imagens = 'privado/images/')
    print("Aguardando 1 minutos...")
    time.sleep(1 * 60)  # 30 minutos em segundos

#DIAS & LIMA ⚜