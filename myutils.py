#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ctypes

def Main():
        
    libtest = ctypes.CDLL("./libmyutils.so")

    ### 1. helloworld
    libtest.helloworld.argtypes = None
    libtest.helloworld.restype = ctypes.c_int
    libtest.helloworld()
    print()


    ### 2. pass two values
    libtest.sum.argtypes = [ctypes.c_int, ctypes.c_int]
    libtest.sum.restype = ctypes.c_int
    rc = libtest.sum(123, 321)
    print("rc={}".format(rc))
    print()


    ### 3. pass a pointer value
    libtest.pass_value_by_reference.argtypes = [ctypes.POINTER(ctypes.c_int)]
    libtest.pass_value_by_reference.restype = ctypes.c_int
    myValue = ctypes.c_int(123)
    rc = libtest.pass_value_by_reference(myValue)
    print(myValue.value)
    print("rc={}".format(rc))
    print()


    ### 4. pass a struct by value
    class pass_struct_by_value_t(ctypes.Structure):
        _fields_ = [
            ("value", ctypes.c_int),
            ("str", ctypes.c_char*100)
        ]
    libtest.pass_struct_by_value.argtypes = [pass_struct_by_value_t]
    libtest.pass_struct_by_value.restype = ctypes.c_int
    myStruct = pass_struct_by_value_t(123, b"Hello World !")
    rc = libtest.pass_struct_by_value(myStruct)
    print("rc={}".format(rc))
    print()


    ### 5. pass a pointer struct
    class pass_struct_by_reference_t(ctypes.Structure):
        _fields_ = [
            ("value", ctypes.c_int),
            ("str", ctypes.c_char*100),
            ("result", ctypes.c_int)
        ]
    libtest.pass_struct_by_reference.argtypes = [ctypes.POINTER(pass_struct_by_reference_t)]
    libtest.pass_struct_by_reference.restype = ctypes.c_int
    myStruct = pass_struct_by_reference_t(123, b"Hello World !")
    rc = libtest.pass_struct_by_reference(ctypes.byref(myStruct))
    print("result={}".format(myStruct.result))
    print("rc={}".format(rc))
    print()


    ### 6. pass a nested struct
    class ip_t(ctypes.Structure):
        _fields_ = [
            ("ip_address", ctypes.c_char*64)
        ]
    class machine_t(ctypes.Structure):
        _fields_ = [
            ("name", ctypes.c_char*128),
            ("ip_num", ctypes.c_int),
            ("ip", ctypes.POINTER(ip_t))
        ]
    class servers_t(ctypes.Structure):
        _fields_ = [
            ("machine_num", ctypes.c_int),
            ("machine", ctypes.POINTER(machine_t))
        ]
    libtest.show_servers.argtypes = [ctypes.POINTER(servers_t)]
    libtest.show_servers.restype = ctypes.c_int

    machine_list = []

    ip_list = []
    ip_list.append(ip_t(b"192.168.0.1"))
    ip_num = len(ip_list)
    ips = (ip_t*ip_num)(*ip_list)
    machine_list.append(machine_t(b"machineA", ip_num, ips))

    ip_list.clear()
    ip_list.append(ip_t(b"192.168.1.1"))
    ip_list.append(ip_t(b"192.168.2.2"))
    ip_list.append(ip_t(b"192.168.2.3"))
    ip_num = len(ip_list)
    ips = (ip_t*ip_num)(*ip_list)
    machine_list.append(machine_t(b"machineB", ip_num, ips))

    machine_num = len(machine_list)
    machines = (machine_t*machine_num)(*machine_list)
    servers = servers_t(machine_num, machines)
    rc = libtest.show_servers(ctypes.byref(servers))
    print("rc={}".format(rc))
    print()


    ### 7. pass a function pointer
    def callbackFunc(msg):
        print("Hey, {}".format(msg.decode('utf-8')))
    myCallback = ctypes.CFUNCTYPE(None, ctypes.c_char_p)
    libtest.callback_sample.argtypes = [myCallback]
    libtest.callback_sample.restype = None
    libtest.callback_sample(myCallback(callbackFunc))

if __name__ == '__main__':
    Main()