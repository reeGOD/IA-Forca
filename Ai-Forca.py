from unidecode import unidecode# Biblioteca usada para desconsiderar os acentos das palavras
from random import choice
import os

def Organizar_Base(caminho_da_base):#Retorna o tamanho da maior palavra encontrada
    #Escreve um novo arquivo com as palavras da base organizadas alfabéticamente e em letras maiúsculas e sem repetições
    leitura = open(caminho_da_base, "r", encoding="utf-8")
    maior_len = 0
    palavras_lidas = (leitura.read()).split()
    palavras_lidas = sorted(set(palavras_lidas))

    for i in range(len(palavras_lidas)):#Deixar todas as palavras em MAIÚSCULO
        palavras_lidas[i]= unidecode(palavras_lidas[i].upper())
        if(maior_len < len(palavras_lidas[i])): maior_len = len(palavras_lidas[i])

    palavras_lidas = sorted(palavras_lidas)#Deixar todas as palavras em ordem alfabética

    leitura.close()
    escrita = open(caminho_da_base, "w", encoding="utf-8")

    #A inserção é feita de forma a não inserir uma linha em branco ao final da base
    for i in range(len(palavras_lidas)-1): escrita.write("{}\n".format(palavras_lidas[i]))
    escrita.write(palavras_lidas[-1])

    escrita.close()
    return maior_len

def Letra(tentativa):
    try:
        while(True):

            if(tentativa.isalpha()):
                if(len(tentativa)>1): print("Digite apenas 1 letra.\nExemplo:\n Letra: a")
                else: break

            else: print("Entrada inválida! Digite 1 letra!!")

    except:
        print("Caractere inválido! Tente novamente")

    tentativa = tentativa.upper()
    if(tentativa == 'Ç'): tentativa = 'C'

    return unidecode(tentativa)

def Palavra(palavra_sorteada, historico_de_letras):
    #Desconsiderando acentos
    for j in range(len(historico_de_letras)):
        historico_de_letras[j] = unidecode(historico_de_letras[j])

    final = ""
    acertou = False

    for i in range(len(palavra_sorteada)):
        if unidecode(palavra_sorteada[i]) in historico_de_letras:
            final += palavra_sorteada[i] + " "


        else: final += "_ "
    print(final)

    if(unidecode(historico_de_letras[-1]) in unidecode(palavra_sorteada)): acertou = True

    return [final, acertou]

def Listar(lista_das_palavras, tamanho_da_maior):
    lista_len = [0] * (tamanho_da_maior + 1)
    for i in range(len(lista_len)):
        lista_len[i] = []

    for j in range(len(lista_das_palavras)):
        lista_len[len(lista_das_palavras[j])].append(lista_das_palavras[j])

    return lista_len

def Filtro_palavras(quant_letras, letras_corretas, Posic_corretas, letras_erradas, Palavras_e_numeros):
    Palavras_possiveis = []

    for i in range(len(Palavras_e_numeros[quant_letras])):
        cond = True
        for j in range(len(letras_corretas)):
            if unidecode(Palavras_e_numeros[quant_letras][i][Posic_corretas[j]]) != unidecode(letras_corretas[j]):
                cond = False
        if cond == True:
            Palavras_possiveis.append(Palavras_e_numeros[quant_letras][i])

    deletar = []
    for palavra in range(len(Palavras_possiveis)):

        for letra in range(len(Palavras_possiveis[palavra])):
            if(Palavras_possiveis[palavra][letra] in letras_erradas):
                deletar.append(palavra)
                break

    for i in range(len(deletar)):
        del Palavras_possiveis[deletar[i]]
        for j in range(len(deletar)):
            deletar[j] = deletar[j]-1

    return Palavras_possiveis

def Determinar_chute(letras_erradas,letras, quant_letras, Palavras_e_numeros, Palavras_possiveis):
    vogais = ["A", "E", "I", "O", "U"]
    quant_vogais = [0] * 5
    if len(letras) == 0 and len(letras_erradas) == 0:
        for j in range(len(Palavras_e_numeros[quant_letras])):
            for z in range(len(Palavras_e_numeros[quant_letras][j])):
                if (Palavras_e_numeros[quant_letras][j][z] not in letras) and (Palavras_e_numeros[quant_letras][j][z] not in letras_erradas):
                    if unidecode(Palavras_e_numeros[quant_letras][j][z]) in vogais:
                        quant_vogais[vogais.index(unidecode(Palavras_e_numeros[quant_letras][j][z]))] += 1
        maior = 0
        for k in range(len(vogais)):
            if quant_vogais[k] > maior:
                maior = quant_vogais[k]
                posic_maior = k
        vogal_popular = vogais[posic_maior]
        chute = vogal_popular

    else:
        maior = 0
        letrores = []
        quant_letrores = []
        for j in range(len(Palavras_possiveis)):
            for z in range(len(Palavras_possiveis[j])):
                if (Palavras_possiveis[j][z] not in letras) and (Palavras_possiveis[j][z] not in letras_erradas):
                    if (Palavras_possiveis[j][z] not in letrores):
                        letrores.append(Palavras_possiveis[j][z])
                        quant_letrores.append(0)
                    quant_letrores[letrores.index(Palavras_possiveis[j][z])] += 1
        for i in range(len(quant_letrores)):
            if quant_letrores[i] > maior:
                maior = quant_letrores[i]
                posic_maior = i
        letrores_popular = letrores[posic_maior]
        chute = letrores_popular

        if len(Palavras_possiveis) == 1:
            for i in range(len(Palavras_possiveis)):
                if unidecode(Palavras_possiveis[0][i]) not in letras:
                    chute = Palavras_possiveis[0][i]

    return chute

caminho_base = "Base_de_Palavras.txt"

maior = Organizar_Base(caminho_base)

dados = open(caminho_base, "r", encoding="utf-8")
base = (dados.read()).split()

palavra = (choice(base)).upper()
print(palavra)

letrinhas = []#Histórico de chutes
erradas = []
corretas = []
pos_corretas = []
T = 6

#print(Listar(base, Organizar_Base(caminho_base)))

#CÓDIGO
for letra in palavra:# Printa '_' para cada letra da palavra
    print("_", end=" ")
print()

while(True):
    #os.system('cls')

    lista_filtrada = Filtro_palavras(len(palavra), corretas, pos_corretas, erradas, Listar(base, maior))
    print(lista_filtrada)

    print("\nTentativas restantes: {}".format(T))

    tentativa = Letra(Determinar_chute(erradas, corretas, len(palavra), Listar(base, maior),lista_filtrada))

    print("Tentativa: {}".format(tentativa))
    
    letrinhas.append(unidecode(tentativa))
    a = Palavra(palavra, letrinhas)
    if(a[1]==False):
        T-=1
        erradas.append(unidecode(letrinhas[-1]))
        erradas = set(erradas)
        erradas = sorted(erradas)# Organizar em ordem alfabética
    else:
        for l in range(len(palavra)):
            if(palavra[l]==letrinhas[-1]):
                pos_corretas.append(l)
                corretas.append(unidecode(letrinhas[-1]))

    a = a[0]
    c = a.replace(" ","")
    if(len(erradas)>0): print("Não tem: ",end="")

    for i in erradas:
        print(i, end=", ")
    print("")

    print(corretas)

    print(pos_corretas)

    if(c == palavra):
        print("\nParabéns! Você acertou!!")
        break
    if(T==0):
        print("\nGAME OVER")
        break

    print("-#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#- \n")

dados.close()
input("Fim do código.Digite qualquer coisa para finalizar.")