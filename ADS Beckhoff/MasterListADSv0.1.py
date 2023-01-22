"""
reading master list from MS SQL and writing to Beckhoff PC through ADS protocol
"""
import os

os.add_dll_directory(r'C:\TwinCAT\AdsApi\TcAdsDll\x64')
import pypyodbc
import pyads
from time import sleep
from collections import OrderedDict

RubricList = [1, 2, 3, 4,
              5]  # 1 - blanking, 2 - transfer, 3 - minitandem, 5 - big tandem, 6 - MTN, 7 - BigTool, 8 - MiniTool, 9 - Common Tool
SpisokADS = ['', '']
SpisokADS[0] = '172.16.17.25.1.1'  # 800TDM
SpisokADS[1] = '5.6.30.148.1.1'  # 250TDM
# SpisokADS[2] = '192.168.82.20.1.1' #1000TDM


conn = pypyodbc.connect('Driver={SQL Server};'
                        'Server=localhost;'
                        'Database=press_data_control;'
                        'uid=press_spvz; '
                        'pwd=admin100;')

while 1:
    for IP in SpisokADS:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM dbo.bboard_masters")
        result = cursor.fetchall()
        cardholderName = []
        cardNumber = []
        accessLevel = []
        i = 0
        if IP == ('172.16.17.25.1.1'):
            banda = [5, 6, 7, 9, 10, 12]
        elif IP == ('5.6.30.148.1.1'):
            banda = [3, 6, 8, 9, 10, 11]
        else:
            banda = []
        for row in result:
            if row[4] in banda:
                cardholderName.append(row[0])
                cardNumber.append(row[1])
                accessLevel.append(row[2])

                print(cardholderName[i], cardNumber[i], accessLevel[i])
                print(IP, i)
                try:
                    plc = pyads.Connection(IP, 801)
                    plc.open()
                    # read state ADS [0] and Device [1]
                    state = plc.read_state()
                    print(state)
                    stMasterData = (('ID', pyads.PLCTYPE_DINT, 1), ('nameCardHolder', pyads.PLCTYPE_STRING, 1),
                                    ('member', pyads.PLCTYPE_BYTE, 1))

                    vars_to_write = OrderedDict([('ID', cardNumber[i]), ('nameCardHolder', cardholderName[i]),
                                                 ('member', accessLevel[i])])
                    source = '.MasterList[' + str(i) + ']'
                    plc.write_structure_by_name(source, vars_to_write, stMasterData)

                    print('write')
                    i = i + 1
                    # close connection
                    plc.close()
                except Exception as e:
                    print("not connected")
                    sleep(1)
                    pass
    sleep(300)
