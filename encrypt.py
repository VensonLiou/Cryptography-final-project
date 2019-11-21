import numpy as np
import key
import image

def scramble(blocks, key: key.scramblingKey):
    result = np.zeros(blocks.shape)
    for ind, k in enumerate(key.key):
        result[ind] = blocks[k]
    return result

def rotateAndInverse(blocks, key: key.rotateInverseKey):
    result = np.zeros(blocks.shape)
    for ind, k in enumerate(key.key):
        if k == 0:
            result[ind] = blocks[ind]
        elif k == 1:
            result[ind] = blocks[ind][:, : : -1]
        elif k == 2:
            result[ind] = blocks[ind][: : -1, :]
        elif k == 3:
            result[ind] = blocks[ind][: : -1, : : -1]
        elif k == 4:
            result[ind] = np.rot90(blocks[ind])
        elif k == 5:
            result[ind] = np.rot90(blocks[ind])[:, : : -1]
        elif k == 6:
            result[ind] = np.rot90(blocks[ind])[: : -1, :]
        elif k == 7:
            result[ind] = np.rot90(blocks[ind])[: : -1, : : -1]
    return result

def NPtrans(blocks, key: key.NPTransKey):
    for ind, k in enumerate(key.key):
        if k == 1:
            blocks[ind] = 255 - blocks[ind]
    return blocks

def encrypt(YCbCr, key1: key.scramblingKey, key2: key.rotateInverseKey, key3: key.NPTransKey):
    blocks = image.YCbCrToBlocks(YCbCr)
    blocks = scramble(blocks, key1)
    blocks = rotateAndInverse(blocks, key2)
    blocks = NPtrans(blocks, key3)
    return image.blocksToYCbCr(blocks, YCbCr.shape)