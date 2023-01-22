"""
reading list of production masters with card number and access level
and writing this information to PLC Q Series
"""
import struct
from time import sleep

import pypyodbc
import snap7
from snap7.snap7exceptions import Snap7Exception

# DB settings
DB_Number = 11001
START_ADDRESS = 0
SIZE = 39562
RACK = 0
SLOT = 2
RubricList = [1, 2, 3, 4, 5, 6, 7, 8, 9,
              10]  # 1 - blanking, 2 - transfer, 3 - minitandem, 5 - big tandem, 6 - MTN, 7 - BigTool, 8 - MiniTool, 9 - Common Tool
Spisok = ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
SpisokIP1 = ['', '', '', '']
SpisokIP1[0] = '10.18.22.3'  # 400TProgressive
SpisokIP1[1] = '192.168.3.101'  # 600Blanking
SpisokIP1[2] = '10.18.22.66'  # Servo
SpisokIP1[3] = '192.168.99.55'  # Progressive
SpisokIP2 = ['', '']
SpisokIP2[0] = '10.18.20.138'  # AIDA1600
SpisokIP2[1] = '10.18.20.133'  # AIDA1000
SpisokIP3 = ['', '', '', '', '', '', '', '', '', '']
SpisokIP3[0] = '192.168.98.10'  # MTD L4
SpisokIP3[1] = '192.168.97.10'  # MTD L3
SpisokIP3[2] = '192.168.96.10'  # MTD L2
SpisokIP3[3] = '192.168.95.11'  # MTD L1 P1
SpisokIP3[4] = '192.168.95.21'  # MTD L1 P2
SpisokIP3[5] = '192.168.95.31'  # MTD L1 P3
SpisokIP3[6] = '192.168.95.41'  # MTD L1 P4
SpisokIP3[7] = '192.168.95.51'  # MTD L1 P5
SpisokIP3[8] = '192.168.95.61'  # MTD L1 P6
SpisokIP3[9] = '192.168.95.9'  # MTD L1
Spisok[1] = SpisokIP1
Spisok[2] = SpisokIP2
Spisok[3] = SpisokIP3
# SQL settings
conn = pypyodbc.connect('Driver={SQL Server};'
                        'Server=localhost;'
                        'Database=press_data_control;'
                        'uid=press_spvz; '
                        'pwd=admin100;')
while 1:
    for rubric_id in RubricList:
        for IP in Spisok[rubric_id]:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM dbo.bboard_masters")
            result = cursor.fetchall()
            cardholderName = []
            cardNumber = []
            accessLevel = []
            i = 0
            if rubric_id == 3:
                ToolShop = 8
                ComPressShop = 11
            else:
                ToolShop = 7
                ComPressShop = 12
            for row in result:
                if row[4] == rubric_id or row[4] == 6 or row[4] == ToolShop or row[4] == 9 or row[4] == ComPressShop or \
                        row[4] == 10:
                    cardholderName.append(row[0])
                    # print(cardholderName)
                    cardNumber.append(row[1])
                    # print(cardNumber)
                    accessLevel.append(row[2])
                    # print(accessLevel)
                    i = i + 1
            try:
                plc = snap7.client.Client()
                plc.connect(IP, RACK, SLOT)
            except Snap7Exception as e:
                sleep(1)
                pass
            if plc.get_connected() == False:
                try:
                    plc = snap7.client.Client()
                    plc.connect(IP, RACK, SLOT)
                    print('not connected')
                    sleep(1)
                except Snap7Exception as e:
                    sleep(1)
                    pass
            else:
                z = 0
                k = 0
                while i != 0:
                    a = 0 + k
                    b = 260 + k
                    c = 6 + k
                    if k < 39560:
                        cardNumbertodb = struct.pack('>l', cardNumber[z])
                        plc.db_write(DB_Number, a, cardNumbertodb)
                        accessLeveltodb = struct.pack('<h', accessLevel[z])
                        plc.db_write(DB_Number, b, accessLeveltodb)
                        b = bytes(cardholderName[z], 'utf-8')
                        cardholderNametodb = struct.pack('254s', b)
                        # print(cardholderNametodb)
                        plc.db_write(DB_Number, c, cardholderNametodb)
                        k = k + 262
                        i = i - 1
                        z = z + 1
                    else:
                        break

            sleep(20)
