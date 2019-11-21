import matplotlib.image as mpimg
import numpy as np

Bx = 8
By = 8

def cuttingPreprocessing(img, Bx, By):
    # cutting scheme
    h_cut = img.shape[1] % Bx
    v_cut = img.shape[0] % By

    if h_cut != 0:
        img = img[:, h_cut // 2 : -(h_cut - h_cut // 2), :]

    if v_cut != 0:
        img = img[v_cut // 2 : -(v_cut - v_cut // 2), :, :]


    return img

def paddingPreprocessing(img, Bx, By):
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

def imread(filename, Bx = 8, By = 8):
    img = mpimg.imread(filename)
    img = cuttingPreprocessing(img, Bx, By)

    r = img[:, :, 0]
    g = img[:, :, 1]
    b = img[:, :, 2]

    y = 0.299 * r + 0.587 * g + 0.114 * b
    cb = -0.1687 * r - 0.3313 * g + 0.5 * b + 128
    cr = 0.5 * r - 0.4187 * g - 0.0813 * b + 128

    YCbCr = np.hstack((y, cb, cr))

    numBlock = YCbCr.size / (Bx * By)

    return YCbCr, numBlock