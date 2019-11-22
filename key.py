import numpy as np

class key:

    def __init__(self, numBlock = None, keyStr = None, fromFile = None):
        if keyStr:
            self.check_validity(keyStr, numBlock)
            self.key = self.keyStrToKey(keyStr)
            self.keyStr = keyStr
        elif fromFile:
            self.key = self.keyStrToKey(fromFile)
            self.keyStr = fromFile
        else:
            self.newKey(numBlock)

    def __str__(self):
        return self.keyStr

class scramblingKey(key):

    def newKey(self, numBlock):
        self.key = np.arange(numBlock, dtype=int)
        np.random.shuffle(self.key)
        self.keyStr = self.keyToKeyStr()

    def keyStrToKey(self, keyStr):
        key = [int(i) for i in keyStr.split('.')]
        return np.array(key)

    def keyToKeyStr(self):
        keyStr = ''
        for i in self.key:
            keyStr += str(i)
            keyStr += '.'
        return keyStr[: -1]

    def check_validity(self, keyStr, numBlock):
        key = self.keyStrToKey(keyStr)
        key = np.sort(key)
        if len(key) != numBlock:
            raise Exception('Key length is incorrect')
        for i in range(numBlock):
            if i != key[i]:
                raise Exception('Key format is incorrect')

class rotateInverseKey(key):

    def newKey(self, numBlock):
        self.key = np.random.randint(8, size = numBlock)
        self.keyStr = self.keyToKeyStr()

    def keyStrToKey(self, keyStr):
        key = [int(i) for i in keyStr]
        return np.array(key)

    def keyToKeyStr(self):
        keyStr = ''
        for i in self.key:
            keyStr += str(i)
        return keyStr

    def check_validity(self, keyStr, numBlock):
        if len(keyStr) != numBlock:
            raise Exception('Key length must be equal to n')
        counter = 0
        for i in range(8):
            counter += keyStr.count(str(i))
        if counter != numBlock:
            raise Exception("Key can only composed by '0', '1', '2',..., '7'")

class NPTransKey(key):
    
    def newKey(self, numBlock):
        self.key = np.random.randint(2, size=numBlock)
        self.keyStr = self.keyToKeyStr()

    def keyStrToKey(self, keyStr):
        key = [int(i) for i in keyStr]
        return np.array(key)

    def keyToKeyStr(self):
        keyStr = ''
        for i in self.key:
            keyStr += str(i)
        return keyStr

    def check_validity(self, keyStr, numBlock):
        if len(keyStr) != numBlock:
            raise Exception('Key length must be equal to n')
        if keyStr.count('0') + keyStr.count('1') != numBlock:
            raise Exception("Key can only composed by '0' and '1'")

def save(key1: scramblingKey, key2: rotateInverseKey, key3: NPTransKey, keyFile = 'key.store'):
    with open(keyFile, mode = 'w') as f:
        f.write(key1.keyStr + '\n' + key2.keyStr + '\n' + key3.keyStr)

def load(keyFile = 'key.store'):
    with open(keyFile, mode = 'r') as f:
        key1 = scramblingKey(fromFile = f.readline()[:-1])
        key2 = rotateInverseKey(fromFile = f.readline()[:-1])
        key3 = NPTransKey(fromFile = f.readline())
    return key1, key2, key3