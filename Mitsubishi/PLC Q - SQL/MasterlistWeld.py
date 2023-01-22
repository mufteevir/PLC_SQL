"""
reading list of production masters with card number and access level
and writing this information to PLC Q Series
"""
import pymcprotocol  # mc protocol for connecting to PLC Q
import pypyodbc  # for connecting with SQL

pymc3e = pymcprotocol.Type3E()
IP = "192.168.60.100"
from time import sleep

# pymc3e.connect("192.168.60.100", 4133)
while 1:
    try:
        conn = pypyodbc.connect('Driver={SQL Server};'
                                'Server=localhost;'
                                'Database=weld_data_control;'
                                'uid=press_spvz; '
                                'pwd=admin100;')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM dbo.masters")
        result = cursor.fetchall()
        D_Reg_List = []
        cardNumber = []
        accessLevel = []
        i = 0
        D_Reg_List_start = 4700
        for row in result:
            cardNumber.append(row[1])
            accessLevel.append(row[2])
            D_Reg_List_calc = D_Reg_List_start + i
            D_Reg_List_string = 'D' + str(D_Reg_List_calc)
            D_Reg_List.append(D_Reg_List_string)
            i += 2
        # print(cardNumber)
        # print(accessLevel)
        # print(D_Reg_List)
        pymc3e.connect(IP, 4133)
        pymc3e.randomwrite(word_devices=[], word_values=[], dword_devices=D_Reg_List, dword_values=cardNumber)
        pymc3e.batchwrite_wordunits(headdevice="D4900", values=accessLevel)
        pymc3e.close()
    except:
        pass
    sleep(60)
