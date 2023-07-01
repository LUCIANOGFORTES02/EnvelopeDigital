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

      

    elif algoritmoSimetrico =="DES":
        #FALTA GERAR O ALGORITMO SIMETRICO DES
        
        key = random.getrandbits(56) # gera uma chave de 56 bits

        key = key.to_bytes(8, 'big') # converte a chave em bytes

        iv = random.getrandbits(56) # gera um IV de 56 bits

        iv = iv.to_bytes(8, 'big') # converte o IV em bytes

        cipher = DES.new(key, DES.MODE_ECB)
        pad = 8 - len(message) % 8
        message += bytes([pad] * pad)
        
        ciphertext = cipher.encrypt(message)


        
         

    else :

        key = random.getrandbits(128) # gera uma chave de 128 bits
        key = key.to_bytes(16, 'big') # converte a chave em bytes
        
        cipher = ARC4.new(key)
        ciphertext = cipher.encrypt(message)


    #Chave Pública do destinatário
    fileKeyPub=open(arquivoChavePublica,"r")
    KeyPubDestinatario= RSA.import_key(fileKeyPub.read())#importando a chave pública
    chave_simetrica_cifrada=rsa.encrypt(key,KeyPubDestinatario)#Criptografaando a chave simetrica com a chave pública


    # Escrever o envelope criptográfico nos arquivos de saída
    chave_assinada_arquivo = open('chave_assinada.pem', 'wb')
    chave_assinada_arquivo.write(chave_simetrica_cifrada)
    chave_assinada_arquivo.close()
    
    arquivo_criptografado= open('arquivo_criptografado', 'wb')
    arquivo_criptografado.write(ciphertext)
    arquivo_criptografado.close()
         
    
    
    return chave_assinada_arquivo,arquivo_criptografado


#Entrada com arquivo da mensagem e a chave criptografada + arquivo da chave rsa do destinatario + Algoritmo simetrico 
def abrirEnvelope(filemessage,fileKeycrypto,arquivoChavePrivada,algoritmoSimetrico):
        
    if algoritmoSimetrico =="AES":
            pass
    
    elif algoritmoSimetrico =="DES":
        pass
    
    else :
        pass
             



    return 0


#Gerar uma chave rsa
chavePrivada,chavePublica=rsa.newkeys(2048)#Chaves do destinatario


#Criar aqruivo com a chave pública do destinatario
with open('chavePublicaDest.pem', 'wb') as chave_assinada_arquivo:
        chave_assinada_arquivo.write(chavePrivada.save_pkcs1())



#Arquivos 
file= "textoClaro.txt"
chave_assinada_arquivo='chavePublicaDest.pem'


#Escolher o algoritmo simétrico
while 1==1:
    print("Escolha o algoritmo simetrico que será utilizado")
    print("1-AES")
    print("2-DES")
    print("3-RC4")
    
    x = input("Digite o valor: ")

    if x == '1':
        algoritmoSimetrico = "AES"
        envelopeDigital(file, chave_assinada_arquivo, algoritmoSimetrico)
        abrirEnvelope()
        print("Deu certo")

    elif x == '2':
        algoritmoSimetrico = "DES"
        envelopeDigital(file, chave_assinada_arquivo, algoritmoSimetrico)
        abrirEnvelope()


    elif x == '3':
        algoritmoSimetrico = "RC4"
        envelopeDigital(file, chave_assinada_arquivo, algoritmoSimetrico)
        abrirEnvelope()


    else:
        print("Opcao invalida")
    
