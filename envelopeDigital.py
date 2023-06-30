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
from cryptography.fernet import Fernet
import rsa


def envelopeDigital (arquivoEmClaro,arquivoChavePublica,algoritmoSimetrico):

#Gerar chave simetrica com o algoritmo passado 

#Cifrar o arquivo em claro com a chave simetrica
    
#Cifrar a chave simetrica com a chave publica do destinatário
    
    return 0




#Gerar uma chave rsa
chavePrivada,chavePublica=rsa.newkeys(2048)#Chaves do destinatario


#Criar aqruivo com a chave pública do destinatario
with open('chavePublicaDest.txt', 'wb') as chave_assinada_arquivo:
        chave_assinada_arquivo.write(chavePrivada.save_pkcs1())



#Lendo o arquivo em claro
with open ("textoClaro.txt","r") as file:
     data= file.read()
print (data)
