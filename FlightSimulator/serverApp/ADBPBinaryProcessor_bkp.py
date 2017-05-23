#!/usr/bin/python
import struct

class PARAMS:
    FrameCounter = 100
    TIME = 101
    ACFTREG = 102
    FLTNUM = 103
    ORIGIN = 104
    DESTINATION = 105
    FLTPHASE = 106
    LATITUDE = 107
    LONGITUDE = 108
    ALTITUDE = 109
    CAS = 110
    GNDSPEED = 111
    MACH = 112
    HDG = 113
    HDGSEL = 114
    VERTSPEED = 115
    WINDSPEED = 116
    WINDDIRT = 117
    TOTFUEL = 118
    N11 = 119
    N12 = 120
    N21 = 121
    N22 = 122
    MWCPFWC1 = 123
    MWFOFWC1 = 124
    MCCPFWC1 = 125
    MCFOFWC1 = 126
    MWCPFWC2 = 127
    MWFOFWC2 = 128
    MCCPFWC2 = 129
    MCFOFWC2 = 130
    ENG1LOP = 131
    ENG2LOP = 132


PARAM_NAMES = {
    PARAMS.FrameCounter: "FrameCounter",
    PARAMS.TIME: "TIME",
    PARAMS.ACFTREG: "ACFTREG",
    PARAMS.FLTNUM: "FLTNUM",
    PARAMS.ORIGIN: "ORIGIN",
    PARAMS.DESTINATION: "DESTINATION",
    PARAMS.FLTPHASE: "FLTPHASE",
    PARAMS.LATITUDE: "LATITUDE",
    PARAMS.LONGITUDE: "LONGITUDE",
    PARAMS.ALTITUDE: "ALTITUDE",
    PARAMS.CAS: "CAS",
    PARAMS.GNDSPEED: "GNDSPEED",
    PARAMS.MACH: "MACH",
    PARAMS.HDG: "HDG",
    PARAMS.HDGSEL: "HDGSEL",
    PARAMS.VERTSPEED: "VERTSPEED",
    PARAMS.WINDSPEED: "WINDSPEED",
    PARAMS.WINDDIRT: "WINDDIRT",
    PARAMS.TOTFUEL: "TOTFUEL",
    PARAMS.N11: "N11",
    PARAMS.N12: "N12",
    PARAMS.N21: "N21",
    PARAMS.N22: "N22",
    PARAMS.MWCPFWC1: "MWCPFWC1",
    PARAMS.MWFOFWC1: "MWFOFWC1",
    PARAMS.MCCPFWC1: "MCCPFWC1",
    PARAMS.MCFOFWC1: "MCFOFWC1",
    PARAMS.MWCPFWC2: "MWCPFWC2",
    PARAMS.MWFOFWC2: "MWFOFWC2",
    PARAMS.MCCPFWC2: "MCCPFWC2",
    PARAMS.MCFOFWC2: "MCFOFWC2",
    PARAMS.ENG1LOP: "ENG1LOP",
    PARAMS.ENG2LOP: "ENG2LOP"
}


class Types:
    uint_type = 112  # 0x70
    int_type = 113  # 0x71
    double_type = 130  # 0x82
    string_type = 161  # 0xa1

class ADBPPacketProcessor:
    unpack_uchar = struct.Struct('B')
    unpack_int = struct.Struct('i')
    unpack_uint = struct.Struct('I')
    unpack_double = struct.Struct('d')

    def Process(self, in_data):

        t_rtnvalue = {}
        #print in_data.encode('hex')

        t_firstChar = in_data[0]
        in_data = in_data[1:]
        t_byte = None
        t_newItem = True
        t_keyValue = None

        while True:

            #print t_firstChar.encode('hex'),
            t_byte = self.unpack_uchar.unpack(t_firstChar)[0]

            if t_byte == 0:
                None

            elif t_newItem:
                t_keyValue = PARAM_NAMES[t_byte]
                t_newItem = False

            elif t_byte == Types.uint_type:
                byte = in_data[0:4]
                unpacked_data = self.unpack_uint.unpack(byte)[0]

                t_rtnvalue[t_keyValue] = unpacked_data
                #tmp = UintItem(t_keyValue, unpacked_data)
                #tmp.Print()

                in_data = in_data[4:]
                t_newItem = True

            elif t_byte == Types.int_type:
                unpacked_data = self.unpack_int.unpack(in_data[0:4])[0]

                t_rtnvalue[t_keyValue] = unpacked_data
                #tmp = IntItem(t_keyValue, unpacked_data)
                #tmp.Print()

                in_data = in_data[4:]
                t_newItem = True

            elif t_byte == Types.double_type:
                unpacked_data = self.unpack_double.unpack(in_data[0:8])[0]
                t_rtnvalue[t_keyValue] = unpacked_data
                #tmp = DoubleItem(t_keyValue, unpacked_data)
                #tmp.Print()

                in_data = in_data[8:]
                t_newItem = True

            elif t_byte == Types.string_type:
                t_length = self.unpack_uchar.unpack(in_data[0])[0]
                t_string = in_data[1:t_length + 1]
                t_rtnvalue[t_keyValue] = t_string

                #tmp = StringItem(t_keyValue, t_length + 1, t_string)
                #tmp.Print()

                in_data = in_data[t_length + 1:]
                t_newItem = True


            # if we reached end of data
            if not in_data:
                break

            t_firstChar = in_data[0]
            in_data = in_data[1:]

        return t_rtnvalue