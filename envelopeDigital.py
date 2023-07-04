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
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Cipher import AES
from Crypto.Cipher import DES
from Crypto.Cipher import ARC4
from Crypto.PublicKey import RSA #Geração do par de chaves
import rsa


def envelopeDigital (arquivoEmClaro,arquivoChavePublica,algoritmoSimetrico):
    #Abrindo o arquivo com o texto em claro
    file=open(arquivoEmClaro,"rb")
    message=file.read()
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
    chave_simetrica_cifrada=rsa.encrypt(key,KeyPubDestinatario)#Criptografando a chave simetrica com a chave pública


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
        

#1 Abir o arquivo com a chave do destinatário 
#2 Abrir o arquivo com a chave simétrica criptografada
#3 Utilizar essa chave para decifrar a chave simétrica
#4 Decifrar o arquivo criptografado com a chave descriptografada

    iv = random.getrandbits(56) # gera um IV de 56 bits
    iv = iv.to_bytes(8, 'big') # converte o IV em 

    #Abrindo os arquivos
    filemessage= open(filemessage.name,"rb")
    message= filemessage.read()#messagem criptografada
    filemessage.close()
    print(message)

    filekeyCrypto= open(fileKeycrypto.name,"rb")
    keyCrypto =filekeyCrypto.read()#Chave simetrica criptografada
    #filekeyPrivate = (arquivoChavePrivada,"rb")
    #keyPrivate=filekeyPrivate.read()
    keyPrivateDestinatario = RSA.import_key (open (arquivoChavePrivada).read ())#Chave privada do destinatario


    # Cria um objeto cifra RSA com o modo PKCS1_OAEP
    rsa = PKCS1_OAEP.new(keyPrivateDestinatario)

    # Descriptografa a chave simétrica com a chave privada do destinatário
    chaveSimetrica = rsa.decrypt(keyCrypto)

    if algoritmoSimetrico =="AES":
        decipher = AES.new(chaveSimetrica, AES.MODE_CBC, iv)
        plaintext = decipher.decrypt(message)



    
    elif algoritmoSimetrico =="DES":
        pass
    
    else :
        decipher = ARC4.new(chaveSimetrica)
        plaintext = decipher.decrypt(message)
             



    return 0


#Gerar uma chave rsa
chavePrivada,chavePublica=rsa.newkeys(2048)#Chaves do destinatario


#Criar arquivo com a chave pública do destinatario 
with open('chavePublicaDest.pem', 'wb') as chave_assinada_arquivo:
        chave_assinada_arquivo.write(chavePublica.save_pkcs1())
#Criar arquivo com a chave privada do destinatario 
with open('chavePrivadaDest.pem', 'wb') as chavePri_assinada_arquivo:
        chavePri_assinada_arquivo.write(chavePrivada.save_pkcs1())





#Arquivos 
file= "textoClaro.txt"
chave_assinada_arquivo='chavePublicaDest.pem'
chavePri_assinada_arquivo="chavePrivadaDest.pem"

#Escolher o algoritmo simétrico
while 1==1:
    print("Escolha o algoritmo simetrico que será utilizado")
    print("1-AES")
    print("2-DES")
    print("3-RC4")
    
    x = input("Digite o valor: ")

    if x == '1':
        algoritmoSimetrico = "AES"
        chave_assinada_arquivo,arquivo_criptografado = envelopeDigital(file, chave_assinada_arquivo, algoritmoSimetrico)
        print (arquivo_criptografado)


        abrirEnvelope(arquivo_criptografado,chave_assinada_arquivo,chavePri_assinada_arquivo,algoritmoSimetrico)
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
    
