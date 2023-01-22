def mysqlquery(data0, data1, data2,
                data3, data4, data5):

    import pypyodbc
    conn = pypyodbc.connect('Driver={SQL Server};'
                              'Server=localhost;'
                             'Database=press_data_control;'
                             'uid=press_spvz; '
                             'pwd=admin100;')

    cursor = conn.cursor()



    SQLquery = (""" 
                    INSERT INTO presentations(dieName,eventVal0,eventVal1,event_id,
                    line_id,master_id) 
                    VALUES (?,?,?,?,?,?)      
                """)
    values = (data0, data1, data2, data3,
             data4, data5)

    cursor.execute(SQLquery, values)
     # results = cursor.fetchall()

     # print(results)
    conn.commit()
    conn.close()
