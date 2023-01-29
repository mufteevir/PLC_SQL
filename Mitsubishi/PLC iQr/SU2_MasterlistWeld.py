import pymcprotocol
import pypyodbc
pymc3e=pymcprotocol.Type3E()
IP = "10.128.127.207"
from time import sleep
#pymc3e.connect("192.168.60.100", 4133)
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
        D_Reg_List_start = 10000  #4700
        for row in result:
            cardNumber.append(row[1])
            accessLevel.append(row[2])
            D_Reg_List_calc = D_Reg_List_start + i
            D_Reg_List_string = 'D' + str(D_Reg_List_calc)
            D_Reg_List.append(D_Reg_List_string)
            i += 2
        #print(cardNumber)
        #print(accessLevel)
        #print(D_Reg_List)
        pymc3e.connect(IP, 5555)
        pymc3e.randomwrite(word_devices=[], word_values=[], dword_devices=D_Reg_List, dword_values=cardNumber)
        pymc3e.batchwrite_wordunits(headdevice="D10200", values=accessLevel)  #D4900
        pymc3e.close()
    except:
        pass
    sleep(60)