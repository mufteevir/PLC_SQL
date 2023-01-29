def mysqlquery(data0, data1, data2,
                data3, data4):

    import pypyodbc
    conn = pypyodbc.connect('Driver={SQL Server};'
                              'Server=localhost;'
                             'Database=weld_data_control;'
                             'uid=press_spvz; '
                             'pwd=admin100;')

    cursor = conn.cursor()



    SQLquery = (""" 
                    INSERT INTO presentations(jigName,partName,event_id,
                    line_id,master_id) 
                    VALUES (?,?,?,?,?)      
                """)
    values = (data0, data1, data2, data3,
             data4)

    cursor.execute(SQLquery, values)
     # results = cursor.fetchall()

     # print(results)
    conn.commit()
    conn.close()