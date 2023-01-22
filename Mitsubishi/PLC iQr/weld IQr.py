"""
successful test connecting to iQR PLC CPU and read data
settings for iQR PLC is provided in pdf file
"""
import pymcprotocol
from time import sleep
pymc3e = pymcprotocol.Type3E(plctype="iQ-R") #plctype="iQ-R"
pymc3e.connect("10.128.127.207", 5555)
sleep(1)

line_values = pymc3e.batchread_wordunits(headdevice="D2066",readsize=1)
print(line_values)

pymc3e.close()
