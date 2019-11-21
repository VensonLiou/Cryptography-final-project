import numpy as np
import key
import image

def inverseScramble(blocks, key: key.scramblingKey):
    result = np.zeros(blocks.shape)
    for ind, k in enumerate(key.key):
        result[k] = blocks[ind]
    return result

def inverseRotateAndInverse(blocks, key: key.rotateInverseKey):
    result = np.zeros(blocks.shape)
    for ind, k in enumerate(key.key):
        if k == 0:
            result[ind] = blocks[ind]
        elif k == 1:
            result[ind] = blocks[ind][:, :: -1]
        elif k == 2:
            result[ind] = blocks[ind][:: -1, :]
        elif k == 3:
            result[ind] = blocks[ind][:: -1, :: -1]
        elif k == 4:
            result[ind] = np.rot90(np.rot90(np.rot90(blocks[ind])))
        elif k == 5:
            result[ind] = np.rot90(np.rot90(np.rot90(blocks[ind][:, :: -1])))
        elif k == 6:
            result[ind] = np.rot90(np.rot90(np.rot90(blocks[ind][:: -1, :])))
        elif k == 7:
            result[ind] = np.rot90(np.rot90(np.rot90(blocks[ind][:: -1, :: -1])))
    return result

def inverseNPtrans(blocks, key: key.NPTransKey):
    for ind, k in enumerate(key.key):
        if k == 1:
            blocks[ind] = 255 - blocks[ind]

def decrypt(img, key1: key.scramblingKey, key2: key.rotateInverseKey, key3: key.NPTransKey):
    img = inverseNPtrans(img, key3)
    img = inverseRotateAndInverse(img, key2)
    img = inverseScramble(img, key1)
    img = image.postProcessing(img)
    return img