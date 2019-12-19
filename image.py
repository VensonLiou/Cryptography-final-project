import matplotlib.image as mpimg
import numpy as np
import cv2

def cuttingPreprocessing(img, Bx = 8, By = 8):
    # cutting scheme
    h_cut = img.shape[1] % Bx
    v_cut = img.shape[0] % By

    if h_cut != 0:
        img = img[:, h_cut // 2 : -(h_cut - h_cut // 2), :]

    if v_cut != 0:
        img = img[v_cut // 2 : -(v_cut - v_cut // 2), :, :]


    return img

def paddingPreprocessing(img, Bx = 8, By = 8):
    # padding scheme
    h_pad = Bx - img.shape[1] % Bx
    v_pad = By - img.shape[0] % By

    if h_pad != 0:
        pad = np.random.randint(256, size = (img.shape[0], h_pad, 3))
        img = np.hstack((pad[:, 0 : h_pad // 2, :], img, pad[:, h_pad // 2 :, :]))

    if v_pad != 0:
        pad = np.random.randint(256, size = (v_pad, img.shape[1], 3))
        img = np.vstack((pad[0 : v_pad // 2, :, :], img, pad[v_pad // 2 :, :, :]))


    return img

def postProcessing(YCbCr):
    imgWidth = int(YCbCr.shape[1] / 3)
    img = np.zeros((YCbCr.shape[0], imgWidth, 3), dtype = int)


    Y = YCbCr[:, : imgWidth]
    Cb = YCbCr[:, imgWidth : 2 * imgWidth]
    Cr = YCbCr[:, 2 * imgWidth :]

    r = (298.082 / 256) * Y + (408.583 / 256) * Cr - 222.921
    g = (298.082 / 256) * Y - (100.291 / 256) * Cb - (208.120 / 256) * Cr + 135.576
    b = (298.082 / 256) * Y + (516.412 / 256) * Cb - 276.836

    img[:, :, 0] = r
    img[:, :, 1] = g
    img[:, :, 2] = b

    img = np.clip(img, 0, 255)

    return img

def YCbCrToBlocks(YCbCr, Bx = 8, By = 8):
    blocks = []
    for i in range(0, YCbCr.shape[0], By):
        for j in range(0, YCbCr.shape[1], Bx):
            blocks.append(YCbCr[i : i + 8, j : j + 8])

    return np.array(blocks)

def blocksToYCbCr(blocks, shape):
    Bx, By = blocks.shape[2], blocks.shape[1]
    numXaxis = int(shape[1] / Bx)
    numYaxis = int(shape[0] / By)
    rows = []
    for i in range(numYaxis):
        rows.append(np.concatenate([blocks[i * numXaxis + j] for j in range(numXaxis)] , axis = 1))

    YCbCr = np.concatenate([rows[i] for i in range(numYaxis)], axis = 0)

    return YCbCr

def readUnencryptedImage(filename, Bx = 8, By = 8):
    img = cv2.imread(filename)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cuttingPreprocessing(img, Bx, By)

    r = img[:, :, 0]
    g = img[:, :, 1]
    b = img[:, :, 2]

    y = 0.299 * r + 0.587 * g + 0.114 * b
    cb = -0.1687 * r - 0.3313 * g + 0.5 * b + 128
    cr = 0.5 * r - 0.4187 * g - 0.0813 * b + 128

    YCbCr = np.hstack((y, cb, cr))

    numBlock = int(YCbCr.size / (Bx * By))

    return img, YCbCr, numBlock

def readencryptedImage(filename, Bx = 8, By = 8):
    YCbCr = mpimg.imread(filename)

    numBlock = int(YCbCr.size / (Bx * By))

    return YCbCr, numBlock

def saveImage(filename, img):
    # RGB
    if img.ndim == 3:
        saveImg = np.zeros(img.shape)
        saveImg[:, :, 0] = img[:, :, 2]
        saveImg[:, :, 1] = img[:, :, 1]
        saveImg[:, :, 2] = img[:, :, 0]
        cv2.imwrite(filename, saveImg)
        return

    # grayscale image
    cv2.imwrite(filename, img)