# PLC_SQL
Programs for implementation swipe system in production, that includes
connecting different PLCs to Python, reading PLC data and writing to MS SQL for logging,
and reading list of production masters from SQL and writing to PLCs

# Mitsubishi PLC

We had 2 types of controllers - Q series and iQr series. For Q series we were making connection through CPU and Ethernet module QJ71E71

[223weldv1.py](https://github.com/mufteevir/PLC_SQL/blob/master/Mitsubishi/PLC%20Q%20-%20SQL/223weldv1.py) - reading data from PLC Q Series and write it to SQL DB if data was changed

[MasterlistWeld.py](https://github.com/mufteevir/PLC_SQL/blob/master/Mitsubishi/PLC%20Q%20-%20SQL/MasterlistWeld.py) - reading list of production masters with card number and access level
and writing this information to PLC Q Series

I also provide 2 files with connection settings for Mitsubishi Q series

[PLC Q CPU connect settings.pdf](https://github.com/mufteevir/PLC_SQL/blob/master/Mitsubishi/PLC%20Q%20-%20SQL/PLC%20Q%20CPU%20connect%20settings.pdf) - settings for connection through Q CPU Ethernet port

[PLC Q QJ71E71 connect settings.pdf](https://github.com/mufteevir/PLC_SQL/blob/master/Mitsubishi/PLC%20Q%20-%20SQL/PLC%20Q%20QJ71E71%20connect%20settings.pdf) - settings for connection through QJ71E71 Ethernet module

[weld IQr.py](https://github.com/mufteevir/PLC_SQL/blob/master/Mitsubishi/PLC%20iQr/weld%20IQr.py) - successful test connecting to iQR PLC CPU and read data

[PLC IQr CPU connect settings.pdf](https://github.com/mufteevir/PLC_SQL/blob/master/Mitsubishi/PLC%20iQr/PLC%20IQr%20CPU%20connect%20settings.pdf) - settings for connection through iQR CPU Ethernet port