"""
Event logging system for press shop
Reading data from PLC S7-300 and write it to SQL DB if data was changed
Logging information - DieName, ValueId, ValueOldId, EventId, LineId, MasterId
"""
from time import sleep

import snap7  # for connecting PLC Siemens

from SQLConnect import mysqlquery

send_ReqVariable1 = list(range(0, 200))
send_ReqVariable2 = list(range(0, 200))
k = 0
DB_Number = 11000  # PLC DB number
START_ADDRESS = 0
SIZE = 774  # size of DB
SpisokIP = ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
SpisokIP[0] = '10.18.20.138'  # AIDA1600
SpisokIP[1] = '10.18.20.133'  # AIDA1000
SpisokIP[2] = '10.18.22.3'  # 400TProgressive
SpisokIP[3] = '192.168.3.101'  # 600Blanking
SpisokIP[4] = '10.18.22.66'  # Servo
SpisokIP[5] = '192.168.99.55'  # Progressive
SpisokIP[6] = '192.168.98.10'  # MTD4
SpisokIP[7] = '192.168.97.10'  # MTD3
SpisokIP[8] = '192.168.96.10'  # MTD2
SpisokIP[9] = '192.168.95.11'  # MTD L1 P1
SpisokIP[10] = '192.168.95.21'  # MTD L1 P2
SpisokIP[11] = '192.168.95.31'  # MTD L1 P3
SpisokIP[12] = '192.168.95.41'  # MTD L1 P4
SpisokIP[13] = '192.168.95.51'  # MTD L1 P5
SpisokIP[14] = '192.168.95.61'  # MTD L1 P6
RACK = 0  # PLC Rack
SLOT = 2  # PLC Slot

while 1:
    for IP in SpisokIP:
        try:
            plc = snap7.client.Client()
            plc.connect(IP, RACK, SLOT)
        except:
            sleep(1)
            pass
        if plc.get_connected() == False:
            try:
                plc = snap7.client.Client()
                plc.connect(IP, RACK, SLOT)
                print('not connected')
                sleep(1)
            except:
                sleep(1)
                pass
        else:
            try:
                db = plc.db_read(DB_Number, START_ADDRESS, SIZE)

                LineId = int.from_bytes(db[0:1], byteorder='big')

                EventId = int.from_bytes(db[1:2], byteorder='big')

                ValueId = db[4:258].decode('UTF-8').strip('\x00')

                MasterId = int.from_bytes(db[258:262], byteorder='big')

                DieName = db[264:518].decode('UTF-8').strip('\x00')

                ValueOldId = db[520:774].decode('UTF-8').strip('\x00')

            except:
                sleep(1)
                pass

            if (send_ReqVariable2[LineId] != ValueId) and MasterId != 0 and ValueId != '0' and ValueId != ValueOldId:
                try:
                    mysqlquery(DieName, ValueId, ValueOldId, EventId, LineId, MasterId)
                    send_ReqVariable1[LineId] = EventId
                    send_ReqVariable2[LineId] = ValueId
                except:
                    pass

        sleep(0.5)
