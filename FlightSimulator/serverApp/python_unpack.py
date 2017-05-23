#!/usr/bin/python
import struct
import binascii

'''
Reading bytes from a file
using the struct module
'''


class Types:
    uint_type = '70'
    int_type = '71'
    double_type = '72'
    string_type = '73'


class UintItem:
    keyValue = None
    value = None

    def __init__(self, t_k, t_v):
        self.keyValue = t_k
        self.value = t_v

    def Print(self):
        print("keyValue: {0} value: {1}".format(self.keyValue, self.value))


class IntItem:
    keyValue = None
    value = None

    def IntItem(self):
        None


class DoubleItem:
    keyValue = None
    value = None

    def DoubleItem(self):
        None


class StringItem:
    keyValue = None
    length = None
    value = None

    def StringItem(self):
        None


f = open("pack_mips", "rb")
try:
    byte = f.read(1)
    newItem = True

    while byte != "":

        print(byte).encode('hex'),
        # print(byte),

        if (newItem):
            s = struct.Struct('B')
            t_keyValue = s.unpack(byte)
            newItem = False

        if byte.encode('hex') == Types.uint_type:
            byte = f.read(4)
            s = struct.Struct('I')
            unpacked_data = s.unpack(byte)

            tmp = UintItem(t_keyValue, unpacked_data)
            tmp.Print()

        # Do stuff with byte.
        byte = f.read(1)

finally:
    f.close()