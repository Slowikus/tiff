class TiffManipulations:
    def __init__(self, file_name):
        self.hexCode = {'width': 0x0100, 'length': 0x0101, 'bits_per_sample': 0x102, 'compression': 0x0103,
                        'photometric_interpretation': 0x0106, 'strip_offsets': 0x111, 'rows_per_strip': 0x0116,
                        'strip_byte_counts': 0x117, 'x_resolution': 0x011A, 'y_resolution': 0x11B,
                        'resolution_unit': 0x0128}

        self.hexValue = {'width': 0, 'length': 0, 'bits_per_sample': 0, 'compression': 0,
                         'photometric_interpretation': 0, 'strip_offsets': 0, 'rows_per_strip': 0,
                         'strip_byte_counts': 0, 'x_resolution': 0, 'y_resolution': 0,
                         'resolution_unit': 0}

        self.data_hex_list = self.returnHexList(file_name)
        self.endian = self.defEndian()
        self.isTiff = self.isTiff()
        self.offset = self.connectByte(self.data_hex_list[4: 8])
        self.returnDE(self.offset+14)
        self.returnIFD(self.offset)


    @staticmethod
    def returnHexList(file_name):
        file = open(file_name, "rb")
        data = file.read()
        file.close()
        data_hex = data.hex()
        data_hex_list = []
        for i in range(len(data_hex)):
            if i % 2 == 0 and i != 0:
                data_hex_list.append(data_hex[i - 2:i])
        print("data_hex_list:" + str(data_hex_list))
        return data_hex_list

    def defEndian(self):
        if int(self.data_hex_list[0] + self.data_hex_list[1], 16) == 0x4949:
            return "little"
        elif int(self.data_hex_list[0] + self.data_hex_list[1]) == 0x4d4d:
            return "big"
        else:
            raise NameError("This file is not Tiff")

    def isTiff(self):
        if self.connectByte(self.data_hex_list[2: 4]) == 0x002A:
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


    def returnIFD(self, start):
        DE = self.connectByte(self.data_hex_list[start: start + 2])
        for i in range(0, DE):
            returnDE()

    def returnDE(self, start):
        tag = self.connectByte(self.data_hex_list[start: start+2])
        type = self.connectByte(self.data_hex_list[start+2: start+4])
        size = self.connectByte(self.data_hex_list[start+4: start+8])
        date = self.connectByte(self.data_hex_list[start+8: start+12])
        print("tag: " + str(tag))
        print("type: " + str(type))
        print("size: " + str(tag))
        print("date: " + str(date))
