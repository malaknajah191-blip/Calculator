import tkinter as tk
import math

button_values=[
    ["AC","+/-","%","÷"],
    ["7","8","9","x"],
    ["4","5","6","-"],
    ["1","2","3","+"],
    ["0",".","√","="],
]

right_symbols=["÷","+","x","-","="] 
top_symbols=["AC","+/-","%"]
row_count=len(button_values)
column_count=len(button_values[0])

light_gray="#D4D4D2"
black="#1C1C1C"
orange="#FF9500"
white="white"
dark_gray="#505050"

#Window
window=tk.Tk()
window.title("Calculator")
window.resizable(False,False)
frame=tk.Frame(window)
label=tk.Label(frame,text="0",font=('Arial',45),background=black,
               foreground=white,anchor="e",width=column_count)

label.grid(row=0,column=0,columnspan=column_count,sticky="we")
for row in range (row_count):
    for column in range (column_count):
        value=button_values[row][column]
        button=tk.Button(frame,text=value,font=('Arial',30),
                         width=column_count-1,height=1,
                         command=lambda value=value: button_clicked(value))
        if value in top_symbols:
            button.config(foreground=black,background=light_gray)
        elif value in right_symbols:
            button.config(foreground=white,background=orange)
        else:
            button.config(foreground=white,background=dark_gray)

        button.grid(row=row+1,column=column)


frame.pack()
A="0"
operator=None
B=None

def clear_all():
    global A,B,operator
    A="0"
    operator=None
    B=None
def remove_zero_decimal(num,precision=3):
    if num%1==0:
        num=int(num)
        return str(num)
    else:
        return str(round(num,precision))
def button_clicked(value):
    global right_symbols,top_symbols,A,B,operator 
    if value in right_symbols:
        if value=="=":
            if A is not None and operator is not None:
                B=label["text"]
                numA=float(A)
                numB=float(B)
                if operator=="+":
                    label["text"]=remove_zero_decimal(numA+numB)
                elif operator=="-":
                    label["text"]=remove_zero_decimal(numA-numB)
                elif operator =="x":
                    label["text"]=remove_zero_decimal(numA*numB)
                elif operator=="÷":
                    label["text"]=remove_zero_decimal(numA/numB)
               
                clear_all()
                
        elif value in "+-x÷√":
            if operator is None :
                A=label["text"]
                label["text"]="0"
                B="0"
            operator=value
    elif value in top_symbols:
        if value=='AC':
            clear_all()
            label["text"]="0"
        elif value=="+/-":
            result=float(label["text"]) *-1
            label["text"]=remove_zero_decimal(result)
        elif value=="%":
            result=float(label["text"]) /100
            label["text"]=remove_zero_decimal(result)
    

    else :
        if value ==".":
            if value not in label['text']:
                if label["text"]=="0":
                    label["text"]="0."
                else:
                    label["text"]+="."
            
        elif value in "0123456789":
            if label["text"]=="0":
               label['text']=value
            else:
                label["text"]+=value
                
        else : 
            try:
                if value== "√" :
                    number=float(label["text"])
                    if number>=0:
                       result=number**0.5
                       label["text"]=remove_zero_decimal(result)
                    else:
                       label["text"]="Error"
            except Exception:
                label['text']='Error'

            

#center window 
window.update() #update window with the new sizes
window_width=window.winfo_width()
window_height=window.winfo_height()
screen_width=window.winfo_screenwidth()
screen_height=window.winfo_screenheight()
window_x=int((screen_width/2)-(window_width/2))
window_y=int((screen_height/2)-(window_height/2))
window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

window.mainloop()





