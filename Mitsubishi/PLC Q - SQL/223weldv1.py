"""
Event logging system for robotic welding cell
Reading data from PLC Q Series and write it to SQL DB if data was changed
Logging information - jig-id, part_id, event_id, line_id, master_id
settings for Q PLC is provided in pdf file
"""
from time import sleep

import pymcprotocol  # connecting by mc protocol

from SQLConnect import mysqlquery

IP = "192.168.60.100"
i = 0
while 1:
    try:
        pymc3e = pymcprotocol.Type3E()
        pymc3e.connect(IP, 4133)  # 4133 - dec, 1025 - hex
        line_values = pymc3e.batchread_wordunits(headdevice="D5000", readsize=1)
        # print(line_id[0])
        line_id = line_values[0]
        event_values = pymc3e.batchread_wordunits(headdevice="D5001", readsize=1)
        # print(event_id[0])
        event_id = event_values[0]
        master_values = pymc3e.batchread_wordunits(headdevice="D5003", readsize=1)
        # print(master_id[0])
        master_id = master_values[0]
        jig_values = pymc3e.batchread_wordunits(headdevice="D5010", readsize=4)
        a1 = jig_values[0] & 0xff
        a2 = (jig_values[0] >> 8) & 0xff
        a3 = jig_values[1] & 0xff
        a4 = (jig_values[1] >> 8) & 0xff
        a5 = jig_values[2] & 0xff
        a6 = (jig_values[2] >> 8) & 0xff
        jig_data = bytes([a1, a2, a3, a4, a5, a6])  # ASCII values for D
        jig_text = jig_data.decode('utf-8')
        # print(jig_text)
        part_values = pymc3e.batchread_wordunits(headdevice="D5020", readsize=4)
        a1 = part_values[0] & 0xff
        a2 = (part_values[0] >> 8) & 0xff
        a3 = part_values[1] & 0xff
        a4 = (part_values[1] >> 8) & 0xff
        a5 = part_values[2] & 0xff
        a6 = (part_values[2] >> 8) & 0xff
        part_data = bytes([a1, a2, a3, a4, a5, a6])  # ASCII values for D
        part_text = part_data.decode('utf-8')
        # print(part_text)
        if master_id == 0 and i == 1:
            i = 0
        pymc3e.close()
    except:
        sleep(1)
        pymc3e.close()
        pass
    if master_id != 0 and event_id != 0 and line_id != 0 and i == 0:
        try:
            mysqlquery(jig_text, part_text, event_id, line_id, master_id)
            i = 1
        except:
            pass
    sleep(5)
