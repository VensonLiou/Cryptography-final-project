import numpy as np

class key:
    def __init__(self, numBlock, keyStr = None):
        if keyStr:
            self.check_validity(keyStr, numBlock)
            self.key = self.keyStrToKey(keyStr)
            self.keyStr = keyStr
        else:
            self.newKey(numBlock)

    def __str__(self):
        return self.keyStr

    def newKey(self, numBlock):
        pass

    def keyStrToKey(self, keyStr):
        pass

    def keyToKeyStr(self):
        pass

    def check_validity(self, keyStr, numBlock):
        pass

class scramblingKey(key):

    def newKey(self, numBlock):
        self.key = np.arange(numBlock, dtype=int)
        np.random.shuffle(self.key)
        self.keyStr = self.keyToKeyStr()

    def keyStrToKey(self, keyStr):
        key = []
        for i in range(0, len(keyStr), 2):
            key.append(int(keyStr[i : i+2]))
        return np.array(key)

    def keyToKeyStr(self):
        keyStr = ''
        for i in self.key:
            if i < 10:
                keyStr += '0'
            keyStr += str(i)
        return keyStr

    def check_validity(self, keyStr, numBlock):
        if len(keyStr) % 2 != 0:
            raise Exception('Key length is incorrect')
        key = self.keyStrToKey(keyStr)
        key = np.sort(key)
        for i in range(numBlock):
            if i != key[i]:
                raise Exception('Key format is incorrect')

class rotateInverseKey:

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
        if keyStr.count('0') + keyStr.count('1') != numBlock:
            raise Exception("Key can only composed by '0', '1', '2',..., '7'")

class NPTransKey:
    def newKey(self, numBlock):
        self.key = np.random.randint(8, size=numBlock)
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