import tags
import binascii


class Tiff:
    def __init__(self, file_name):

        self.hexList = self.returnHexList(file_name)
        self.endian = self.defEndian()
        self.isTiff = self.isTiff()
        self.offset = self.connectByte(self.hexList[4: 8])
        self.returnIFD(self.offset, self.hexList)
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
        #print("Amount of TAGS:" + str(amountOfDE))
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
        print("////////////////// Tagi zanonimizowanego pliku //////////////////" )
        self.returnIFD(self.offset, anonimizedHexList)

        #zapisywanie do pliku
        newFile = open("anonim.tif","wb")
        for x in range(len(anonimizedHexList)):
            binaryList = binascii.unhexlify(anonimizedHexList[x])
            newFileByteArray = bytearray(binaryList)
            newFile.write(newFileByteArray)

