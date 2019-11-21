import matplotlib.pyplot as plt
import image
import key
import encrypt
import decrypt

# read image
ori, YCbCr, n = image.imread('doggy.jpg')

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
encryImg = encrypt.encrypt(YCbCr, k1, k2, k3)

# result after encryption
plt.imshow(encryImg, cmap = 'gray')
plt.title('Encrypted')
plt.show()

# decrypt
decryImg = decrypt.decrypt(encryImg, k1, k2, k3)

# result after encryption
plt.imshow(decryImg)
plt.title('Decrypted')
plt.show()