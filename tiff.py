import sys
import tags
from shutil import copyfile


class Tiff:
    def __init__(self, file_name):

        self.hexList = self.returnHexList(file_name)
        self.endian = self.defEndian()
        self.isTiff = self.isTiff()
        self.offset = self.connectByte(self.hexList[4: 8])
        self.anonimize(file_name)


    @staticmethod
    def returnHexList(file_name):
        hexList = []
        file = open(file_name, "rb")
        data = file.read()
        file.close()
        hex = data.hex()

        for i in range(len(hex)):
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
        elif self.endian == "little":
            if len(tab) == 2:
                connectedByte = tab[1] + tab[0]
            if len(tab) == 4:
                connectedByte = tab[3] + tab[2] + tab[1] + tab[0]
        return int(connectedByte, 16)

    def returnDE(self, start):
        tag = self.connectByte(self.hexList[start: start + 2])
        type = self.connectByte(self.hexList[start + 2: start + 4])
        size = self.connectByte(self.hexList[start + 4: start + 8])
        data = self.connectByte(self.hexList[start + 8: start + 12])

        print("tag: ", end='')
        for i in tags.requiredTagsStrips:
            if tags.requiredTagsStrips[i] == tag:
                print(str(i), end='')
        print(" (" + str(tag) + ")")

        for i in tags.dataTypes:
            if tags.dataTypes[i] == type:
                print("type: " + str(i))

        print("size: " + str(size))

        print("data: " + str(data))

        print("--------------")

    def returnIFD(self, start):
        amountOfDE = self.connectByte(self.hexList[start: start + 2])
        print("Amount of TAGS:" + str(amountOfDE))
        for i in range(0, amountOfDE):
            self.returnDE(start + 2 + i * 12)
        sizeOfIFD = start + 2 + amountOfDE * 12
        offsetNextIFD = self.connectByte(self.hexList[sizeOfIFD:  sizeOfIFD + 4])
        print("offset of next IFD: " + str(offsetNextIFD))
        if offsetNextIFD == 0:
            print("End of file")

        else:
            print("Go to next IFD")
            self.returnIFD(sizeOfIFD + 4)

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
        copyfile(file_name, 'test.tif')
        anonimizedHexList = self.returnHexList('test.tif')
        position = self.offset + 2
        positionAnonimized = self.offset
        amountOfDE = self.connectByte(self.hexList[self.offset: self.offset + 2])

        if self.isTailed(self.offset) == False:
            anonimizedHexList[positionAnonimized] = 0
            anonimizedHexList[positionAnonimized + 1] = hex(12)
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
                anonimizedHexList[positionAnonimized + x] = '0'
        else:
            anonimizedHexList[positionAnonimized] = 0
            anonimizedHexList[positionAnonimized + 1] = hex(13)
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
                anonimizedHexList[positionAnonimized + x] = '0'

        ###################################
        #wyswitlanie czy git
        start = self.offset
        amountOfDE = 12

        for i in range(0, amountOfDE):
            a= start + 2 + i * 12
            tag = self.connectByte(self.hexList[a: a + 2])
            type = self.connectByte(self.hexList[a + 2: a + 4])
            size = self.connectByte(self.hexList[a + 4: a + 8])
            data = self.connectByte(self.hexList[a + 8: a + 12])

            print("tag: ", end='')
            for i in tags.requiredTagsStrips:
                if tags.requiredTagsStrips[i] == tag:
                    print(str(i), end='')
            print(" (" + str(tag) + ")")

            for i in tags.dataTypes:
                if tags.dataTypes[i] == type:
                    print("type: " + str(i))

            print("size: " + str(size))

            print("data: " + str(data))

            print("--------------")

        sizeOfIFD = start + 2 + amountOfDE * 12
        offsetNextIFD = self.connectByte(anonimizedHexList[sizeOfIFD:  sizeOfIFD + 4])

        if offsetNextIFD != 0:

            print("Go to next IFD")
            self.returnIFD(sizeOfIFD + 4)


