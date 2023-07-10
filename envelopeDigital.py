#Funções: criar um envelope e abir um envelope digital

#Criar um envelope
"""
Entrada
1- Criar arquivo em claro 
2- Criar arquivo da chave Rsa pública do destinatário
3- Criar algum algoritmo assimetrico DES/AES
Processamento
1-Gerar chave temporaria/aletória 
2-Cifrar o arquivo em claro com a chave gerada 
3-Cifrar a chave temporaria com a chave do destinatário
Saída
Dois arquivos um com a chave assinada e outro do arquivo criptografado
"""
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, DES, ARC4

from Crypto.Random import get_random_bytes
import os

def criar_envelope(arquivo_claro, arquivo_chave_publica, algoritmo_simetrico):
    # Carregar a chave pública do destinatário
    chave_publica = RSA.import_key(open(arquivo_chave_publica).read())

    # Gerar uma chave simétrica temporária/aleatória
    chave_simetrica = get_random_bytes(16)  # 16 bytes para chave AES

    # Cifrar o arquivo em claro com a chave simétrica
    cifra_simetrica = None
    if algoritmo_simetrico == "AES":
        cifra_simetrica = AES.new(chave_simetrica, AES.MODE_ECB)
        
    elif algoritmo_simetrico == "DES":
        chave_simetrica = get_random_bytes(8)  # 8 bytes para chave DES

        cifra_simetrica = DES.new(chave_simetrica, DES.MODE_ECB)
    else:
        cifra_simetrica = ARC4.new(chave_simetrica)
   

    # Cria um objeto cifra RSA com o modo PKCS1_OAEP
    rsa = PKCS1_OAEP.new(chave_publica)

    # Descriptografa a chave simétrica com a chave privada do destinatário
    chave_simetrica_cifrada=rsa.encrypt(chave_simetrica)#Criptografando a chave simetrica com a chave pública

    # Criando o arquivo com a chave assinada
    file_chave_assinada=open("chave_assinada.pem","wb")
    file_chave_assinada=file_chave_assinada.write(chave_simetrica_cifrada)
   
    # Criando o arquivo criptografado
    file_claro= open(arquivo_claro, "rb")
    texto_claro = file_claro.read()
    pad = 16 - len(texto_claro) % 16 #Garantir que a mensagem tenha tamanho multiplo de 16 
    texto_claro += bytes([pad] * pad)#Preenche

    texto_cifrado = cifra_simetrica.encrypt(texto_claro)

    file_criptografado= open("arquivo_criptografado", "wb")
    file_criptografado=file_criptografado.write(texto_cifrado)

    print("Envelope criado")

def abrir_envelope(arquivo_criptografado, arquivo_chave_cifrada, arquivo_chave_privada, algoritmo_simetrico):
    # Carregar a chave privada do destinatário
    chave_privada = RSA.import_key(open(arquivo_chave_privada).read())
    #Abrindo o arquivo da chave simetrica criptografada
    file_chave_cifrada = open(arquivo_chave_cifrada, "rb")
    chave_simetrica_cifrada = file_chave_cifrada.read()

    # Decifrar a chave simétrica com a chave privada do destinatário

    # Cria um objeto cifra RSA com o modo PKCS1_OAEP
    rsa = PKCS1_OAEP.new(chave_privada)

    # Descriptografa a chave simétrica com a chave privada do destinatário
    chave_simetrica = rsa.decrypt(chave_simetrica_cifrada)

    # Decifrar o arquivo criptografado com a chave simétrica
    if algoritmo_simetrico == "AES":
        cifra_simetrica = AES.new(chave_simetrica, AES.MODE_ECB)
    elif algoritmo_simetrico == "DES":
        cifra_simetrica = DES.new(chave_simetrica, DES.MODE_ECB)
    else :
        cifra_simetrica = ARC4.new(chave_simetrica)
    

    # Abrindo o arquivo criptografado
    file_criptografado=open(arquivo_criptografado, "rb")
    texto_cifrado = file_criptografado.read()
    texto_decifrado = cifra_simetrica.decrypt(texto_cifrado)
    
    arquivo_decifrado = input("Digite o caminho e o nome do arquivo que possuira a mensagem descriptografada:")
    # Criando o arquivo decifrado
    file_decifrado= open(arquivo_decifrado, "wb")#"arquivo_decifrado"
    file_decifrado.write(texto_decifrado)

    print("Envelope aberto.")


textoEmClaro = input("Digite o caminho e o nome do arquivo do texto em claro:")


#Criar arquivo em claro
file_out = open(textoEmClaro, 'wb')#'textoClaro.txt'
message=input("Digite a mensagem desejada?")
message = bytes(message, 'utf-8')# transforma a mensagem(string utf-8 para bytes)

file_out .write(message)

#Gerar uma chave rsa
key = RSA.generate(2048)
chavePrivada = key.export_key()
#Criar arquivo com a chave privada do destinatario 
file_out = open('private.pem', 'wb')
file_out .write(chavePrivada)
file_out.close()

chavePublica = key.publickey().export_key()
#Criar arquivo com a chave pública do destinatario 
file_out=open('public.pem', 'wb')
file_out.write(chavePublica)
file_out.close()

arquivo_claro =textoEmClaro #"textoClaro.txt"
arquivo_chave_publica = "public.pem"
#algoritmo_simetrico = "AES"
arquivo_criptografado = "arquivo_criptografado"
arquivo_chave_cifrada = "chave_assinada.pem"
arquivo_chave_privada = "private.pem"



print("Escolha o algoritmo simetrico que será utilizado")
print("1-AES")
print("2-DES")
print("3-RC4")

x = input("Digite o valor:")
if x=='1':
    algoritmo_simetrico="AES"
    
    criar_envelope(arquivo_claro, arquivo_chave_publica, algoritmo_simetrico)

    abrir_envelope(arquivo_criptografado, arquivo_chave_cifrada, arquivo_chave_privada, algoritmo_simetrico)
if x=='2':
    algoritmo_simetrico="DES"
    
    criar_envelope(arquivo_claro, arquivo_chave_publica, algoritmo_simetrico)

    abrir_envelope(arquivo_criptografado, arquivo_chave_cifrada, arquivo_chave_privada, algoritmo_simetrico)

if x=='3':
    algoritmo_simetrico="RC4"

    criar_envelope(arquivo_claro, arquivo_chave_publica, algoritmo_simetrico)


    abrir_envelope(arquivo_criptografado, arquivo_chave_cifrada, arquivo_chave_privada, algoritmo_simetrico)
