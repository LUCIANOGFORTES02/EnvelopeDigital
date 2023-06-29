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


def envelopeDigital ():
    
    
    return 0





#Gerando chave aleatória
key =Fernet.generate_key()
f = Fernet(key)

#Lendo o arquivo em claro
file = open("textoClaro.txt","rb")
data = file.read()

#Criptografando o arquivo
encrypted = f.encrypt(data)
print (encrypted)
