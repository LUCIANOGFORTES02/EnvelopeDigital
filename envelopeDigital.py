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
    elif algoritmo_simetrico == "RC4":
        cifra_simetrica = ARC4.new(chave_simetrica)
    else:
        print("Algoritmo simétrico inválido.")
        return


    # Cria um objeto cifra RSA com o modo PKCS1_OAEP
    rsa = PKCS1_OAEP.new(chave_publica)

    # Descriptografa a chave simétrica com a chave privada do destinatário
    chave_simetrica_cifrada=rsa.encrypt(chave_simetrica)#Criptografando a chave simetrica com a chave pública

    # Criar o arquivo com a chave assinada
    #with open("chave_assinada.pem", "wb") as file_chave_assinada:
    #    file_chave_assinada.write(chave_simetrica_cifrada)
    file_chave_assinada=open("chave_assinada.pem","wb")
    file_chave_assinada=file_chave_assinada.write(chave_simetrica_cifrada)


   
    # Criar o arquivo criptografado
    with open(arquivo_claro, "rb") as file_claro:
        texto_claro = file_claro.read()
        pad = 16 - len(texto_claro) % 16 #Garantir que a mensagem tenha tamanho multiplo de 16 
        texto_claro += bytes([pad] * pad)#Preenche
        #ciphertext = cipher.encrypt(message)
        texto_cifrado = cifra_simetrica.encrypt(texto_claro)

        with open("arquivo_criptografado", "wb") as file_criptografado:
            file_criptografado.write(texto_cifrado)

    print("Envelope criado com sucesso.")

def abrir_envelope(arquivo_criptografado, arquivo_chave_cifrada, arquivo_chave_privada, algoritmo_simetrico):
    # Carregar a chave privada do destinatário
    chave_privada = RSA.import_key(open(arquivo_chave_privada).read())

    # Decifrar a chave simétrica com a chave privada do destinatário
    with open(arquivo_chave_cifrada, "rb") as file_chave_cifrada:
        chave_simetrica_cifrada = file_chave_cifrada.read()


         # Cria um objeto cifra RSA com o modo PKCS1_OAEP
        rsa = PKCS1_OAEP.new(chave_privada)

        # Descriptografa a chave simétrica com a chave privada do destinatário
        chave_simetrica = rsa.decrypt(chave_simetrica_cifrada)

    # Decifrar o arquivo criptografado com a chave simétrica
    cifra_simetrica = None
    if algoritmo_simetrico == "AES":
        cifra_simetrica = AES.new(chave_simetrica, AES.MODE_ECB)
    elif algoritmo_simetrico == "DES":
        cifra_simetrica = DES.new(chave_simetrica, DES.MODE_ECB)
    elif algoritmo_simetrico == "RC4":
        cifra_simetrica = ARC4.new(chave_simetrica)
    else:
        print("Algoritmo simétrico inválido.")
        return

    # Abrir o arquivo criptografado
    with open(arquivo_criptografado, "rb") as file_criptografado:
        texto_cifrado = file_criptografado.read()
        texto_decifrado = cifra_simetrica.decrypt(texto_cifrado)

    # Criar o arquivo decifrado
    with open("arquivo_decifrado", "wb") as file_decifrado:
        file_decifrado.write(texto_decifrado)

    print("Envelope aberto com sucesso.")


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

# Exemplo de uso
arquivo_claro = "textoClaro.txt"
arquivo_chave_publica = "public.pem"
algoritmo_simetrico = "AES"

print("Escolha o algoritmo simetrico que será utilizado")
print("1-AES")
print("2-DES")
print("3-RC4")

x = input("Digite o valor:")
if x=='1':
    algoritmo_simetrico="AES"
    # Criar envelope
    criar_envelope(arquivo_claro, arquivo_chave_publica, algoritmo_simetrico)

    # Abrir envelope
    arquivo_criptografado = "arquivo_criptografado"
    arquivo_chave_cifrada = "chave_assinada.pem"
    arquivo_chave_privada = "private.pem"

    abrir_envelope(arquivo_criptografado, arquivo_chave_cifrada, arquivo_chave_privada, algoritmo_simetrico)
if x=='2':
    algoritmo_simetrico="DES"
    # Criar envelope
    criar_envelope(arquivo_claro, arquivo_chave_publica, algoritmo_simetrico)

    # Abrir envelope
    arquivo_criptografado = "arquivo_criptografado"
    arquivo_chave_cifrada = "chave_assinada.pem"
    arquivo_chave_privada = "private.pem"

    abrir_envelope(arquivo_criptografado, arquivo_chave_cifrada, arquivo_chave_privada, algoritmo_simetrico)

if x=='3':
    algoritmo_simetrico="RC4"
    # Criar envelope
    criar_envelope(arquivo_claro, arquivo_chave_publica, algoritmo_simetrico)

    # Abrir envelope
    arquivo_criptografado = "arquivo_criptografado"
    arquivo_chave_cifrada = "chave_assinada.pem"
    arquivo_chave_privada = "private.pem"

    abrir_envelope(arquivo_criptografado, arquivo_chave_cifrada, arquivo_chave_privada, algoritmo_simetrico)