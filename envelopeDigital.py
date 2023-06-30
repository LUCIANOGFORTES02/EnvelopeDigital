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
import random
from Crypto.Cipher import AES
from Crypto.Cipher import DES
from Crypto.Cipher import ARC4
from Crypto.PublicKey import RSA #Geração do par de chaves
import rsa


def envelopeDigital (arquivoEmClaro,arquivoChavePublica,algoritmoSimetrico):
    file=open(arquivoEmClaro,"rb")
    message=file.read()#Texto em claro
    file.close()
    
#Gerar chave simetrica com o algoritmo passado 
    if algoritmoSimetrico =="AES":

        key = random.getrandbits(128) # gera uma chave de 128 bits

        key = key.to_bytes(16, 'big') # converte a chave em bytes

        iv = random.getrandbits(128) # gera um IV de 128 bits

        iv = iv.to_bytes(16, 'big') # converte o IV em bytes

        cipher = AES.new(key, AES.MODE_CBC, iv)#Modo de operação CBC (Chiper Block Chaning)
        pad = 16 - len(message) % 16 #Garantir que a mensagem tenha tamanho multiplo de 16 
        message += bytes([pad] * pad)#Preenche
        ciphertext = cipher.encrypt(message)#Criptografando a mensagem

        fileKeyPub=open(arquivoChavePublica,"r")
        KeyPubDestinatario= RSA.import_key(fileKeyPub.read())
        #KeyPubDestinatario= fileKeyPub.read()
        chave_simetrica_cifrada=rsa.encrypt(key,KeyPubDestinatario)#Criptografaando a chave simetrica com a chave pública


         # Escrever o envelope criptográfico nos arquivos de saída
        chave_assinada_arquivo = open('chave_assinada.pem', 'wb')
        chave_assinada_arquivo.write(chave_simetrica_cifrada)
        chave_assinada_arquivo.close()
        
        arquivo_criptografado= open('arquivo_criptografado', 'wb')
        arquivo_criptografado.write(ciphertext)
        arquivo_criptografado.close()

    elif algoritmoSimetrico =="DES":
         pass
    else :
         pass
    
    
    return chave_assinada_arquivo,arquivo_criptografado




#Gerar uma chave rsa
chavePrivada,chavePublica=rsa.newkeys(2048)#Chaves do destinatario


#Criar aqruivo com a chave pública do destinatario
with open('chavePublicaDest.pem', 'wb') as chave_assinada_arquivo:
        chave_assinada_arquivo.write(chavePrivada.save_pkcs1())



#Lendo o arquivo em claro
file= "textoClaro.txt"
chave_assinada_arquivo='chavePublicaDest.pem'
algoritmoSimetrico = "AES"
envelopeDigital(file, chave_assinada_arquivo, algoritmoSimetrico)

"""
while False:
    print("Escolha o algoritmo simetrico")
    print("1-AES")
    print("2-DES")
    print("3-RC4")
    
    x = input("Digite o valor: ")

    if x == '1':
        algoritmoSimetrico = "AES"
        envelopeDigital(file, chave_assinada_arquivo, algoritmoSimetrico)

    elif x == '2':
        algoritmoSimetrico = "DES"
        envelopeDigital(file, chave_assinada_arquivo, algoritmoSimetrico)

    elif x == '3':
        algoritmoSimetrico = "RC4"
        envelopeDigital(file, chave_assinada_arquivo, algoritmoSimetrico)

    else:
        print("Opcao invalida")1
"""    
