"""
connection and read data from beckhoff PC using ADS protocol, writing data to SQL
"""
import os

os.add_dll_directory(r'C:\TwinCAT\AdsApi\TcAdsDll\x64')
import pyads
from SQLConnect import mysqlquery
from time import sleep

SpisokADS = ['', '', '', '', '', '']
SpisokADS[0] = '172.16.17.25.1.1'  # 800TDM
SpisokADS[1] = '192.168.82.20.1.1'  # 1000TDM
SpisokADS[2] = '5.6.30.148.1.1'  # 250TDM
SpisokPRS = [1, 2, 3, 4]
send_ReqVariable1 = [0, 0, 0, 0, 0]
send_ReqVariable2 = [0, 0, 0, 0, 0]

while 1:
    # for ADS in SpisokADS:
    for N in SpisokPRS:
        try:
            # connect to plc and open connection
            plc = pyads.Connection('172.16.17.25.1.1', 801)
            plc.open()
            # read state ADS [0] and Device [1]
            state = plc.read_state()
            if state[0] != 0:  # 0 - invalided state
                # read int value by name
                LineId = plc.read_by_name(".P" + str(N) + "_RFID_DATA.LineID", pyads.PLCTYPE_UINT)
                EventId = plc.read_by_name(".P" + str(N) + "_RFID_DATA.EventID", pyads.PLCTYPE_UINT)
                ValueId = plc.read_by_name(".P" + str(N) + "_RFID_DATA.ValueID", pyads.PLCTYPE_STRING)
                MasterId = plc.read_by_name(".P" + str(N) + "_RFID_DATA.MasterID", pyads.PLCTYPE_DINT)
                DieName = plc.read_by_name(".P" + str(N) + "_RFID_DATA.DieName", pyads.PLCTYPE_STRING)
                ValueOld = plc.read_by_name(".P" + str(N) + "_RFID_DATA.ValueOld", pyads.PLCTYPE_STRING)

                # close connection
                plc.close()
                sleep(0.5)

            else:
                print("ADS invalid")
                sleep(1)

        except:
            print("not connected")
            sleep(1)
            pass

        if send_ReqVariable2[N] != ValueId and MasterId != 0 and ValueId != '0' and ValueId != ValueOld:
            # noinspection PyBroadException
            try:
                mysqlquery(DieName, ValueId, ValueOld, EventId, LineId, MasterId)
                send_ReqVariable1[N] = EventId
                send_ReqVariable2[N] = ValueId
                print('sql')
            except:
                print('something wrong, check buffer')
                pass
