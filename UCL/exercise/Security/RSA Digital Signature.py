import rsa
def generateKeys():
    (publicKey, privateKey) = rsa.newkeys(1024)
    with open('./publicKey.pem', 'wb') as p:
        p.write(publicKey.save_pkcs1('PEM'))
    with open('./privateKey.pem', 'wb') as p:
        p.write(privateKey.save_pkcs1('PEM'))

def loadKeys():
    with open('./publicKey.pem', 'rb') as p:
        publicKey = rsa.PublicKey.load_pkcs1(p.read())
    with open('./privateKey.pem', 'rb') as p:
        privateKey = rsa.PrivateKey.load_pkcs1(p.read())
    return privateKey, publicKey

def encrypt(message, key):
    return rsa.encrypt(message.encode('ascii'), key)

def decrypt(ciphertext, key):
    try:
        return rsa.decrypt(ciphertext, key).decode('ascii')
    except:
        return False
    
def sign(message, key):
    return rsa.sign(message.encode('ascii'), key, 'SHA-256')

def verify(message, signature, key):
    try:
        return rsa.verify(message.encode('ascii'), signature, key,) == 'SHA-256'
    except:
        return False
    
generateKeys()
publicKey, privateKey = loadKeys()
message = input('Hi Bob! this message is very secret.')
ciphertext = encrypt(message, publicKey)
print(ciphertext)
signature = sign(message, privateKey)
text = decrypt(ciphertext, privateKey)
if verify(text, signature, publicKey):
    print("Successfully verified")
else:
    print("Unsuccessful")