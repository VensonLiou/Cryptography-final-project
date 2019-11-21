import matplotlib.pyplot as plt
import image
import key
import encrypt
import decrypt

# read image
ori, YCbCr, n = image.readUnencryptedImage('doggy.jpg')

plt.imshow(ori)
plt.title('Original')
plt.show()

# generate random key
k1 = key.scramblingKey(n)
k2 = key.rotateInverseKey(n)
k3 = key.NPTransKey(n)

# print key
# key.__str__()
print('k1 =', k1)
print('k2 =', k2)
print('k3 =', k3)

# encrypt
encryptedImg = encrypt.encrypt(YCbCr, k1, k2, k3)

# result after encryption
plt.imshow(encryptedImg, cmap = 'gray')
plt.title('Encrypted')
plt.show()

image.saveImage('encryptedImg.jpg', encryptedImg)

# read image to decrypt
encryptedImg, n = image.readencryptedImage('encryptedImg.jpg')

# specify keys
k1 = key.scramblingKey(n, k1.keyStr)
k2 = key.rotateInverseKey(n, k2.keyStr)
k3 = key.NPTransKey(n, k3.keyStr)

# decrypt
decryptedImg = decrypt.decrypt(encryptedImg, k1, k2, k3)

# result after decryption
plt.imshow(decryptedImg)
plt.title('Decrypted')
plt.show()

image.saveImage("decryptedImg.jpg", decryptedImg)