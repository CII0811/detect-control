import serial
from tkinter import *
from time import sleep
import sys

ser = serial.Serial('COM5', 9600, timeout=1)
max_temperature = 28

def update_values():
    while ser.in_waiting:
        data_raw = ser.readline()
        data = data_raw.decode()
        print(data)

        if len(data) >= 36:
            Temperature = data[31:36]
            Humidity = data[10:15]
            Temperature2=data[71:76]
            Humidity2=data[50:55]

            try:
                temperature_float = float(Temperature)
                humidity_float = float(Humidity)
                temperature_float2 = float(Temperature2)
                humidity_float2 = float(Humidity2)

                
                if temperature_float >= max_temperature :
                    result_label.config(text='溫度過高')                       
                    print('溫度過高')
                elif temperature_float < max_temperature:
                    result_label.config(text='溫度正常')
                    print('溫度正常')
                if temperature_float2 >= max_temperature:
                    result_label2.config(text='溫度過高') 
                    print('溫度2過高')
                elif temperature_float2 < max_temperature:
                    result_label2.config(text='溫度正常')
                    print('溫度2正常')
                if temperature_float >= max_temperature or temperature_float2 >= max_temperature:
                    motor_status_label.config(text='開啟')
                    ser.write(b'Servo_ON\n')
                    sleep(0.5)
                elif temperature_float < max_temperature or temperature_float2 < max_temperature:
                    motor_status_label.config(text='關閉')
                    ser.write(b'Servo_OFF\n')
                    sleep(0.5)

            except ValueError as e:
                print(f"Error converting to float: {e}")

        temperature_label.config(text=f' {Temperature} °C')
        humidity_label.config(text=f'{Humidity}%')
        temperature_label2.config(text=f' {Temperature2} °C')
        humidity_label2.config(text=f'{Humidity2}%')

    # 使用 after 方法，每隔一段时间自动调用 update_values 函数
    root.after(1000, update_values)

def update_max_temperature():
    global max_temperature
    try:
        max_temperature = float(max_temp_entry.get())
    
    except ValueError:
        print("請輸入有效的數字")
        
try:
    root = Tk()
    root.title("小型環控箱監測")
    root.geometry("400x250")
    
    controlT=Label(root, text="最高溫度 : ", width=10)
    T1 = Label(root, text="溫度1", bg="lightyellow", width=10)
    T2 = Label(root, text="溫度2", bg="lightyellow", width=10)
    M1 = Label(root, text="濕度1", bg="lightblue", width=10)
    M2 = Label(root, text="濕度2", bg="lightblue", width=10)
    F1 = Label(root, text="風扇", bg="lightgreen", width=10)

    btn1 = Button(root, text="Exit", width=15, command=root.destroy)
    btn1.grid(row=6, column=1)
    btn1 = Button(root, text="確認", width=10, command=update_max_temperature)
    btn1.grid(row=0, column=2)
    
    # Entry元件用於輸入最高溫度
    max_temp_entry = Entry(root, width=10)
    max_temp_entry.insert(0, str(max_temperature))
    max_temp_entry.grid(row=0, column=1)

    controlT.grid(row=0, column=0)
    T1.grid(row=1, column=0)
    T2.grid(row=3, column=0)
    M1.grid(row=2, column=0)
    M2.grid(row=4, column=0)
    F1.grid(row=5, column=0)
    
    
    result_label = Label(root, text="偵測狀態")
    result_label.grid(row=1, column=2)
    temperature_label = Label(root, text="偵測中...")
    temperature_label.grid(row=1, column=1)
    humidity_label = Label(root,text="偵測中...")
    humidity_label.grid(row=2, column=1)

    result_label2 = Label(root, text="偵測狀態")
    result_label2.grid(row=3, column=2)
    temperature_label2 = Label(root, text="偵測中...")
    temperature_label2.grid(row=3, column=1)
    humidity_label2 = Label(root,text="偵測中...")
    humidity_label2.grid(row=4, column=1)
    
    motor_status_label = Label(root, text="關閉")
    motor_status_label.grid(row=5, column=1)
    # 第一次启动更新
    update_values()

    root.mainloop()

except KeyboardInterrupt:
    ser.close()
    print('再見！')
