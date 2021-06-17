import secrets
import random
import sympy
import tags
import binascii
import math
import pprint
import sys

class Tiff:
    def __init__(self, file_name, anonimize):

        self.xor = 12344
        self.dividedImageDataDecimal = []
        self.dividedEncryptedImageData = []
        self.encryptedImageData = []
        self.imageDataFile = []
        self.decryptedImageData = []
        self.decryptedHex = []
        self.dataL = 180
        self.hexList = self.returnHexList(file_name)
        self.endian = self.defEndian()
        self.isTiff = self.isTiff()
        self.offset = self.connectByte(self.hexList[4: 8])
        if anonimize == 'ecb':
            self.ECB()
        if anonimize == 'cbc':
            self.CBC()
        if anonimize == 'ctr':
            self.CTR()

        # self.returnIFD(self.offset, self.hexList)



    def ECB(self):
        self.readRequiredTags()
        self.keys()
        self.toChunks(self.imageData, 127)
        self.encrypt()
        self.toHex()
        self.savefile(self.encryptedImageData, 'zakodowanyECB.tif')
        self.readEncrypted('zakodowanyECB.tif')
        self.decrypt()
        self.savefile(self.decryptedHex, 'odkodowanyECB.tif')

    def CBC(self):
        self.readRequiredTags()
        self.keys()
        self.toChunks(self.imageData, 127)
        self.encryptCBC()
        self.toHex()
        self.savefile(self.encryptedImageData, 'zakodowanyCBC.tif')
        self.readEncrypted('zakodowanyCBC.tif')
        self.decryptCBC()
        self.savefile(self.decryptedHex, 'odkodowanyCBC.tif')

    def CTR(self):
        self.readRequiredTags()
        self.keys()
        self.toChunks(self.imageData, 127)
        self.encryptCTR()
        self.toHex()
        self.savefile(self.encryptedImageData, 'zakodowanyCTR.tif')
        self.readEncrypted('zakodowanyCTR.tif')
        self.decryptCTR()
        self.savefile(self.decryptedHex, 'odkodowanyCTR.tif')

    @staticmethod
    def returnHexList(file_name):
        hexList = []
        file = open(file_name, "rb")
        data = file.read()
        file.close()
        hex = data.hex()

        for i in range(len(hex)+1):
            if i % 2 == 0 and i != 0:
                hexList.append(hex[i - 2:i])
        return hexList

    def defEndian(self):
        if int(self.hexList[0] + self.hexList[1], 16) == 0x4949:
            return "little"
        elif int(self.hexList[0] + self.hexList[1], 16) == 0x4d4d:
            return "big"
        else:
            raise NameError("This file is not Tiff")

    def isTiff(self):
        if self.connectByte(self.hexList[2: 4]) == 0x002A:
            return True
        raise NameError("This file is not Tiff")

    def connectByte(self, tab):
        connectedByte = ''
        if self.endian == "big":
            if len(tab) == 2:
                connectedByte = tab[0] + tab[1]
            if len(tab) == 4:
                connectedByte = tab[0] + tab[1] + tab[2] + tab[3]
            if len(tab) == 8:
                connectedByte = tab[0] + tab[1] + tab[2] + tab[3] +tab[4] + tab[5] + tab[6] + tab[7]
        elif self.endian == "little":
            if len(tab) == 2:
                connectedByte = tab[1] + tab[0]
            if len(tab) == 4:
                connectedByte = tab[3] + tab[2] + tab[1] + tab[0]
            if len(tab) == 8:
                connectedByte = tab[7] + tab[6] + tab[5] + tab[4]+tab[3] + tab[2] + tab[1] + tab[0]
        return int(connectedByte, 16)

    def returnDE(self, start, hexList):
        tag = self.connectByte(hexList[start: start + 2])
        type = self.connectByte(hexList[start + 2: start + 4])
        size = self.connectByte(hexList[start + 4: start + 8])
        data = self.connectByte(hexList[start + 8: start + 12])

        print("tag: ", end='')
        for i in tags.tags:
            if tags.tags[i] == tag:
                print(str(i), end='')
        print(" (" + str(tag) + ")")

        for i in tags.dataTypes:
            if tags.dataTypes[i] == type:
                print("type: " + str(i))

        print("size: " + str(size))

        print("data:", end='')
        for i, j in tags.data.items():
            if tag == i:
                for key in j:
                    if key == data:
                        print(" " + str(tags.data[tag][key]) + " ", end='')
        print("(" + str(data) + ")")

        print("\n--------------")

        for i in tags.exifTags:
            if tags.exifTags[i] == tag:
                print("--Znaleziono nowy IFD: " + str(i) + " --")
                self.returnIFD(data, self.hexList)

    def returnIFD(self, start, hexList):
        amountOfDE = self.connectByte(hexList[start: start + 2])
        # print("Amount of TAGS:" + str(amountOfDE))
        for i in range(0, amountOfDE):
            self.returnDE(start + 2 + i * 12, hexList)
        sizeOfIFD = start + 2 + amountOfDE * 12
        offsetNextIFD = self.connectByte(hexList[sizeOfIFD:  sizeOfIFD + 4])
        print("offset of next IFD: " + str(offsetNextIFD))
        if offsetNextIFD == 0:
            print("End of IFD")
        else:
            print("Go to next IFD")
            self.returnIFD(sizeOfIFD + 4, hexList)

    # Funkcja zwracająca true jeżeli znajdzie wskazany tag oraz false jezeli nie. nie poztrebne XD
    def findTag(self, start, tag):
        amountOfDE = self.connectByte(self.hexList[start: start + 2])
        for i in range(0, amountOfDE):
            if tag == self.connectByte(self.hexList[start + 2 + i * 12: start + 2 + i * 12 + 2]):
                return True

        sizeOfIFD = start + 2 + amountOfDE * 12
        offsetNextIFD = self.connectByte(self.hexList[sizeOfIFD:  sizeOfIFD + 4])
        if offsetNextIFD != 0:
            self.returnIFD(sizeOfIFD + 4)

        return False

    # Funkcja sprawdzająca czy obraz jest "tailowany"
    def isTailed(self, start):
        if self.findTag(start, 273) == True:
            return False
        else:
            return True

    # Funkcja tworząca zanonimizowana kopię obrazu
    def anonimize(self, file_name):
        anonimizedHexList = self.returnHexList(file_name)
        position = self.offset + 2
        positionAnonimized = self.offset
        amountOfDE = self.connectByte(self.hexList[self.offset: self.offset + 2])

        if self.isTailed(self.offset) == False:

            if self.endian == "big":
                anonimizedHexList[positionAnonimized] = '00'
                anonimizedHexList[positionAnonimized + 1] = '0c'
            elif self.endian == "little":
                anonimizedHexList[positionAnonimized] = '0c'
                anonimizedHexList[positionAnonimized + 1] = '00'

            print(self.connectByte(anonimizedHexList[positionAnonimized: positionAnonimized + 2]))
            positionAnonimized += 2
            for i in range(0, amountOfDE):
                tag = self.connectByte(self.hexList[position: position + 2])
                for i in tags.requiredTagsStrips:
                    if tags.requiredTagsStrips[i] == tag:
                        for x in range(12):
                            anonimizedHexList[positionAnonimized + x] = self.hexList[position + x]
                        positionAnonimized += 12
                position += 12

            for x in range(4):
                anonimizedHexList[positionAnonimized + x] = '00'
        else:
            if self.endian == "big":
                anonimizedHexList[positionAnonimized] = '00'
                anonimizedHexList[positionAnonimized + 1] = '0d'
            elif self.endian == "little":
                anonimizedHexList[positionAnonimized] = '0d'
                anonimizedHexList[positionAnonimized + 1] = '00'

            positionAnonimized += 2
            for i in range(0, amountOfDE):
                tag = self.connectByte(self.hexList[position: position + 2])
                for i in tags.requiredTagsStrips:
                    if tags.requiredTagsStrips[i] == tag:
                        for x in range(12):
                            anonimizedHexList[positionAnonimized + x] = self.hexList[position + x]
                        positionAnonimized += 12
                position += 12

            for x in range(4):
                anonimizedHexList[positionAnonimized + x] = '00'
        print("////////////////// Tagi zanonimizowanego pliku //////////////////")
        self.returnIFD(self.offset, anonimizedHexList)

        # zapisywanie do pliku
        newFile = open("anonim.tif", "wb")
        for x in range(len(anonimizedHexList)):
            binaryList = binascii.unhexlify(anonimizedHexList[x])
            newFileByteArray = bytearray(binaryList)
            newFile.write(newFileByteArray)

    def readRequiredTags(self):

        amountOfDE = self.connectByte(self.hexList[self.offset: self.offset+2])
        for i in range(0, amountOfDE):
            start = self.offset + 2 + i * 12
            tag = self.connectByte(self.hexList[start: start + 2])
            type = self.connectByte(self.hexList[start + 2: start + 4])
            data = self.connectByte(self.hexList[start + 8: start + 12])

            for i in tags.tagsSave:
                if tags.tagsSave[i] == tag:
                    tags.tagsValues[i] = data

                    if i == 'x_resolution':
                        x = tags.tagsValues['x_resolution']
                        self.xRes = self.hexList[x : x + 8]
                    if i == 'y_resolution':
                        y = tags.tagsValues['y_resolution']
                        self.yRes = self.hexList[y : y + 8]


        self.stripsInImage = math.floor((tags.tagsValues['length'] * (tags.tagsValues['rows_per_strip'] - 1)) /  tags.tagsValues['rows_per_strip'])
        self.imageData = []
        for i in range(tags.tagsValues['strip_byte_counts']):
            self.imageData.append(self.hexList[tags.tagsValues['strip_offsets']+i])




    def savefile(self, pixels, filename):
        anonimizedHexList = []
        anonimizedHexList.append("49492a00")
        anonimizedHexList.append("080000000c00")

        position = self.offset + 2
        amountOfDE = self.connectByte(self.hexList[self.offset: self.offset + 2])

        for i in range(0, amountOfDE):
            tag = self.connectByte(self.hexList[position: position + 2])
            for i in tags.requiredTagsStrips:
                if tags.requiredTagsStrips[i] == tag:
                    if i == 'bits_per_sample':
                        for x in range(8):
                            anonimizedHexList.append(self.hexList[position + x])
                        anonimizedHexList.append("9e000000")
                    elif i == 'x_resolution':
                        for x in range(8):
                            anonimizedHexList.append(self.hexList[position + x])
                        anonimizedHexList.append("A4000000")
                    elif i == 'y_resolution':
                        for x in range(8):
                            anonimizedHexList.append(self.hexList[position + x])
                        anonimizedHexList.append("AC000000")
                    elif i == 'strip_offsets':
                        for x in range(8):
                            anonimizedHexList.append(self.hexList[position + x])
                        anonimizedHexList.append("B4000000")
                    else:
                        for x in range(12):
                            anonimizedHexList.append(self.hexList[position + x])
            position += 12

        for x in range(4):
            anonimizedHexList.append('00')
        anonimizedHexList.append("080008000800")
        anonimizedHexList = anonimizedHexList + self.xRes
        anonimizedHexList = anonimizedHexList + self.yRes
        anonimizedHexList = anonimizedHexList + pixels

        newFile = open(filename, "wb")
        for x in range(len(anonimizedHexList)):
            binaryList = binascii.unhexlify(anonimizedHexList[x])
            newFileByteArray = bytearray(binaryList)
            newFile.write(newFileByteArray)

    def keys(self):
        # klucz 1024 bitowy
        self.e = 834781
        self.n = 1

        while (self.n.bit_length() < 1024) is True:
            num_of_bits = random.randrange(480, 520)
            p = secrets.randbits(num_of_bits)
            q = secrets.randbits(1024 - num_of_bits)
            while sympy.isprime(p) is False:
                p = secrets.randbits(num_of_bits)
            while sympy.isprime(q) is False:
                q = secrets.randbits(1024 - num_of_bits)
            self.n = p * q

        phi_n = (p - 1) * (q - 1)
        self.d = pow(self.e, -1, phi_n)
        self.p = p
        self.q = q

    def hexListToDecimalNum(self,list):
        num = ''
        for i in range(0, len(list)):
            num = num + list[i]
        return int(num, 16)

    def toChunks(self,my_list , lenght):
        divided = [my_list[i * lenght:(i + 1) * lenght] for i in range((len(my_list) + lenght - 1) // lenght)]

        for value in divided:

            #długość kazdego 127
            self.dividedImageDataDecimal.append(self.hexListToDecimalNum(value))



    def encrypt(self):

        for i in self.dividedImageDataDecimal:
            a = pow(i, self.e, self.n)
            self.dividedEncryptedImageData.append(a)




    def toHex(self):


        for i in range(0,len(self.dividedEncryptedImageData)):
            a = hex(self.dividedEncryptedImageData[i]).replace('0x','')
            if i != len(self.dividedEncryptedImageData):
                if len(a) < 256:
                    zeros = '0' * (256 - len(a))
                    a =zeros + a
            else:
                a = '0' + a

            self.encryptedImageData.append(a)


        self.amountOfChunksToRead = len(self.encryptedImageData)

    def readEncrypted(self,filename):
        hexList = []
        file = open(filename, "rb")
        data = file.read()
        file.close()
        hex = data.hex()

        for i in range(len(hex) + 1):
            if i % 2 == 0 and i != 0:
                hexList.append(hex[i - 2:i])

        data = self.dataL
        for i in range(0,self.amountOfChunksToRead):
            self.imageDataFile.append(hexList[data:data+128])
            data = data+128

    def decrypt(self):

        for i in range(0,len(self.imageDataFile)):

            self.decryptedImageData.append((pow(int((''.join(self.imageDataFile[i])), 16), self.d, self.n)))

        for i in range(0,len(self.decryptedImageData)):
            a = hex(self.decryptedImageData[i]).replace('0x','')
            if i != len(self.decryptedImageData)-1:
                if len(a) < 254:
                    zeros = '0' * (254 - len(a))
                    a =  zeros + a

            self.decryptedHex.append(a)


    ######## CBC #########################################################
    def encryptCBC(self):


        a = self.xor

        for i in self.dividedImageDataDecimal:
            i = i ^ (a >> 1)
            # print(i.bit_length())

            a = pow(i, self.e, self.n)
            # print(a.bit_length())
            self.dividedEncryptedImageData.append(a)


    def decryptCBC(self):

        for i in range(0,len(self.imageDataFile)):
            if i == 0:
                a = self.xor
            else:
                a = int((''.join(self.imageDataFile[i-1])), 16)
                # print('(')
                # print(len(self.imageDataFile[i-1]))
                # print(len(self.imageDataFile[i]))
                # print(')')

            b=pow(int((''.join(self.imageDataFile[i])), 16), self.d, self.n)
            b = b ^ (a >> 1)
            self.decryptedImageData.append(b)




        for i in range(0,len(self.decryptedImageData)):
            a = hex(self.decryptedImageData[i]).replace('0x','')

            if i != len(self.decryptedImageData)-1:
                if len(a) < 254:
                    zeros = '0' * (254 - len(a))
                    a =  zeros + a

            self.decryptedHex.append(a)

############ CTR ##############################################
    def encryptCTR(self):
        self.ctr = secrets.token_hex(50)

        for i in range(0, len(self.dividedImageDataDecimal)):
            nonce = self.ctr
            for lenght in range(0,50-len(str(i+1))):
                nonce = nonce +'00'
            if len(str(i+1)) % 2 == 0:
                nonce = nonce + str(i+1)
            else:
                nonce = nonce + '0' + str(i+1)
            # print(nonce)

            a = pow(int(nonce,16), self.e, self.n)
            a = a ^ self.dividedImageDataDecimal[i]
            self.dividedEncryptedImageData.append(a)

    def decryptCTR(self):
        for i in range(0, len(self.imageDataFile)):
            nonce = self.ctr
            for lenght in range(0, 50 - len(str(i + 1))):
                nonce = nonce + '00'
            if len(str(i + 1)) % 2 == 0:
                nonce = nonce + str(i + 1)
            else:
                nonce = nonce + '0' + str(i + 1)

            a = pow(int(nonce, 16), self.e, self.n)
            # print(self.imageDataFile[i])
            a = a ^ int((''.join(self.imageDataFile[i])), 16)
            self.decryptedImageData.append(a)


        for i in range(0,len(self.decryptedImageData)):
            a = hex(self.decryptedImageData[i]).replace('0x','')
            if i != len(self.decryptedImageData)-1:
                if len(a) < 254:
                    zeros = '0' * (254 - len(a))
                    a =  zeros + a

            self.decryptedHex.append(a)
