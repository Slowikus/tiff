import sys
import tags

class Tiff:
    def __init__(self, file_name):

        self.hexList = self.returnHexList(file_name)
        self.endian = self.defEndian()
        self.isTiff = self.isTiff()
        self.offset = self.connectByte(self.hexList[4: 8])
        print("offset: " + str(self.offset))
        self.returnIFD(self.offset)


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

        for i in tags.basicTags:
            if tags.basicTags[i] == tag:
                print("tag name: " + str(i))

        print("tag: " + str(tag))
        print("type: " + str(type))
        print("size: " + str(size))
        print("data: " + str(data))

        print("----------")

    def returnIFD(self, start):
        amountOfDE = self.connectByte(self.hexList[start: start + 2])
        print("Amount of TAGS:" + str(amountOfDE))
        for i in range(0, amountOfDE):
            self.returnDE(start + 2 + i*12)
        sizeOfIFD = start + 2 + amountOfDE * 12
        offsetNextIFD = self.connectByte(self.hexList[sizeOfIFD:  sizeOfIFD + 4])
        print("offset of next IFD: " + str(offsetNextIFD))
        if offsetNextIFD == 0:
            print("End of file")
            sys.exit()
        else:
            print("Go to next IFD")
            self.returnIFD(sizeOfIFD+4)
