from tkinter import *
from tkinter import ttk
from threading import Thread
import time, datetime
import random
import pytz
import psycopg2
root = Tk()
flag=0
obj1 = datetime.datetime.now()
weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
diasemana = weekdays[obj1.weekday()]
def ProcessPunchDate(flag,diasemana):
    while(True):
        def getPuchDate():
            RandMinutes=random.randrange(0,15)
            RandSeconds=random.randrange(0,59)
            obj = datetime.datetime.now()
            tz = pytz.timezone('America/Bogota')
            col_obj = tz.localize(obj)
            new_tz = pytz.timezone('Asia/Shanghai')
            # Re-defining the timezone https://www.geeksforgeeks.org/working-with-datetime-objects-and-timezones-in-python/
            new_obj = col_obj.astimezone(new_tz)
            #new_obj.minute=new_obj.minute+RandNumber
            time_change = datetime.timedelta(minutes=RandMinutes, seconds=RandSeconds)
            new_time = new_obj + time_change
            print(f'Output from function "getPunchdate" dia de la semana: {diasemana} y datepunch: {new_time.astimezone(new_tz)}')
            return new_time.astimezone(new_tz),diasemana
        def InsertDB(punchDate):
                conn = psycopg2.connect(
                    host="192.168.1.11",
                    database="biotime",
                    user="postgres",
                    password="123456",
                    port="7496")

                cur = conn.cursor()
                tuple_data1 = (
                    '98481683', punchDate, 0, 15, 0, 'CN97212360540', '3D', 'Moteles', None, None, 1, 9,
                    'AAIABAJABAGAAACAAAJA',
                    None, punchDate, 82, 1, 0, 0.0)
                print(tuple_data1[0],'::', tuple_data1[1])
                sql1 = "INSERT INTO public.iclock_transaction(emp_code,punch_time,punch_state,verify_type,work_code,terminal_sn,terminal_alias,area_alias,gps_location,mobile,source,purpose,crc,reserved,upload_time,emp_id, terminal_id,is_mask,temperature) VALUES (%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s)"
                cur.execute(sql1, tuple_data1)

                conn.commit()
                flag=1
                cur.close()
                conn.close()
        if (diasemana!='Friday' and  diasemana!='Sunday'):
            if (((datetime.datetime.now().hour==7 and  datetime.datetime.now().minute>50) or (datetime.datetime.now().hour==8 and  datetime.datetime.now().minute<11))):
                DiaColombia_and_ChinaNow= getPuchDate()
                SelectedDateTime = DiaColombia_and_ChinaNow[0]
                diasemana=DiaColombia_and_ChinaNow[1]
                if flag == 0:
                    PunchInsertada=InsertDB(SelectedDateTime)
                    print(f'Registro insertado en public.iclock_transaction Table, día de la semana: {diasemana}')
                    flag=1
                else:
                    print(f'Ya se hizo una marcación en este rango de horas')
            else:
                print(f'Horario no pertenece al rango de horas correcto {datetime.datetime.now()} que se estableció  flag=0')
                flag=0
        else:
            print('Días no laborables')
        time.sleep(180)

threadGetDate = Thread(target=ProcessPunchDate,args=(flag,diasemana), name='threadPunchRecord')
threadGetDate.daemon=True
threadGetDate.start()

content = ttk.Frame(root)
frame = ttk.Frame(content, borderwidth=10, relief="ridge", width=200, height=100)
namelbl = ttk.Label(content, text="Name")
name = ttk.Entry(content)

onevar = BooleanVar(value=True)
twovar = BooleanVar(value=False)
threevar = BooleanVar(value=True)

one = ttk.Checkbutton(content, text="One", variable=onevar, onvalue=True)
two = ttk.Checkbutton(content, text="Two", variable=twovar, onvalue=True)
three = ttk.Checkbutton(content, text="Three", variable=threevar, onvalue=True)
ok = ttk.Button(content, text="Okay")
cancel = ttk.Button(content, text="Cancel")

content.grid(column=0, row=0)
frame.grid(column=0, row=0, columnspan=3, rowspan=2)
namelbl.grid(column=3, row=0, columnspan=2)
name.grid(column=3, row=1, columnspan=2)
one.grid(column=0, row=3)
two.grid(column=1, row=3)
three.grid(column=2, row=3)
ok.grid(column=3, row=3)
cancel.grid(column=4, row=3)

root.mainloop()