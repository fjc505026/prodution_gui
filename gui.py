import tkinter as tk
from tkinter import  ttk
from tkinter.messagebox import showerror, showwarning, showinfo
from tkinter.constants import BOTTOM, CENTER, LEFT, RIGHT, TOP, TRUE
# from tkinter.filedialog import askopenfilename, asksaveasfilename
# from typing import Text
from scanner.ecia import Scanner

board_eui={}
gui_scanner={}

def btn_start_handler():
    if not is_auto_scan.get():
        if not eui_entry.get().startswith("98") or len(eui_entry.get())!=16:
            msg="please type valid eui, 16 digitals"
            #print("msg")
            showwarning(title='Warning',message=msg)
        else:
            board_eui=eui_entry.get() 
            #print(board_eui)
    else:
        global gui_scanner
        if not gui_scanner:
            try:
                gui_scanner = Scanner()
            except: #Exception Scanner use exit(0)
                msg="Can't find Scanner, please have a check and another try"
                #print("msg")
                showwarning(title='Warning',message=msg)
                return

        gui_scanner.drain()
        print("Please scan device barcode(plug in battery and switch on the board)")
        bc = gui_scanner.scan()
        if "S" not in bc:
            msg="Could not decode barcode"
            #print(msg)
            showwarning(title='Warning',message=msg)
        board_eui = bc["S"]

def btn_provision_handler():
    pass

def sel():
    if is_auto_scan.get():
        print("Scanner Mode") 
    else:    
        print("Mannual Mode") 
  
def generate_labels_with_lableframe(master_frame,framename, elements_list):
    row_index=list(range(0,len(elements_list)))
    labelframe = tk.LabelFrame(master_frame, text=framename)
    labelframe.pack(fill="both", expand="yes")
    labelframe.rowconfigure(row_index, minsize=10, weight=1)
    labelframe.columnconfigure([0,1], minsize=100, weight=1)
    
    for idx in row_index:
        board_eui_label = tk.Label(labelframe, text=elements_list[idx]+':')
        board_eui_label.grid(row=idx, column=0,  sticky="w", padx=5, pady=5)
        board_eui_data = tk.Label(labelframe, text="placeholder..")
        board_eui_data.grid(row=idx, column=1,  sticky="w", padx=5, pady=5)


main_window = tk.Tk()
is_auto_scan = tk.BooleanVar()
main_window.title("Definium Prodution Test Tool")
main_window.geometry('1200x800+50+50')
main_frame = tk.Frame(main_window)
main_frame.pack()

frame_1_top=tk.LabelFrame(main_frame,text="TEST")
frame_1_top.pack(side=TOP,fill="both", expand="yes")

frame_1_middle=tk.LabelFrame(main_frame,text="DEBUG")
frame_1_middle.pack(fill="both", expand="yes")

frame_1_bottom=tk.LabelFrame(main_frame,text="PROVSION")
frame_1_bottom.pack(side=BOTTOM,fill="both", expand="yes")

#frame_1_top stuff
frame_2_col1=tk.Frame(frame_1_top,padx=10, pady=10)
frame_2_col1.pack(side=LEFT)
frame_2_col2=tk.Frame(frame_1_top,padx=10, pady=10)
frame_2_col2.pack(side=LEFT)
frame_2_col3=tk.Frame(frame_1_top,padx=10, pady=10)
frame_2_col3.pack(side=LEFT)
frame_2_col4=tk.Frame(frame_1_top,padx=10, pady=10)
frame_2_col4.pack(side=LEFT)


##frame_2_col1  test 
frame_2_col1.rowconfigure([0,1,2,3,4], minsize=10, weight=1)
frame_2_col1.columnconfigure(0, minsize=100, weight=1)

btn_test = tk.Button(frame_2_col1, text="Start Test", fg="blue",font=10, command=btn_start_handler)
btn_test.grid(row=0, column=0, columnspan=2, sticky="nsew", ipadx=20, ipady=20)

radio_scan=tk.Radiobutton(frame_2_col1, text="scan", variable=is_auto_scan, value=True,
                command=sel)
radio_scan.grid(row=1, column=0,  sticky="w", padx=5, pady=5)
radio_mannul=tk.Radiobutton(frame_2_col1, text="manual", variable=is_auto_scan, value=False,
                command=sel)
radio_mannul.grid(row=1, column=1,  sticky="w", padx=5, pady=5)

eui_label = ttk.Label(frame_2_col1, text="board eui:")
eui_label.grid(row=2, column=0,  sticky="w", padx=5, pady=5)
eui_entry = ttk.Entry(frame_2_col1)
eui_entry.grid(row=2, column=1,  sticky="w", padx=5, pady=5)

##frame_2_col2   board_info
ele_list=['board eui','board type','board rev','project','batch']
generate_labels_with_lableframe(frame_2_col2,"INFO.",ele_list)

##frame_2_col3   test detail
ele_list=['modem test','gps test','flash test','battery test','solar test']
generate_labels_with_lableframe(frame_2_col3,"DETAIL",ele_list)

##frame_2_col4   test result
labelframe = tk.LabelFrame(frame_2_col4, text="RESULT")
labelframe.pack(fill="both", expand="yes",ipadx=20,ipady=20)
result_label = tk.Label(labelframe, text="PASS",relief="ridge",fg="red",anchor=CENTER)
result_label.pack(ipadx=40,ipady=40)

#frame_1_middle stuff
frame_1_middle.rowconfigure(0, weight=1)
frame_1_middle.columnconfigure(0,weight=1)
debug_text=tk.Text(frame_1_middle)
debug_text.grid(row=0, column=0, sticky='ew')
debug_text.insert('1.0', 'This a text demo\r\n'*1000)
scrollbar = ttk.Scrollbar(frame_1_middle, orient='vertical', command=debug_text.yview)
scrollbar.grid(row=0, column=1, sticky='ns')
debug_text['yscrollcommand'] = scrollbar.set

#frame_1_bottom stuff
frame_2_col1=tk.Frame(frame_1_bottom,padx=10, pady=10)
frame_2_col1.pack(side=LEFT)
frame_2_col2=tk.Frame(frame_1_bottom,padx=50, pady=10)
frame_2_col2.pack(side=LEFT)
frame_2_col3=tk.Frame(frame_1_bottom,padx=10, pady=10)
frame_2_col3.pack(side=RIGHT)

btn_provision = tk.Button(frame_2_col1, text="Provision",fg="blue",font=10, command=btn_provision_handler)
btn_provision.pack(ipadx=20, ipady=20)

ele_list=['thing name','node type']
generate_labels_with_lableframe(frame_2_col2,"AWS Info",ele_list)

labelframe = tk.LabelFrame(frame_2_col3, text="RESULT")
labelframe.pack(fill="both", expand="yes",ipadx=20,ipady=20)
result_label = tk.Label(labelframe, text="PASS",relief="ridge",fg="red",anchor=CENTER)
result_label.pack(ipadx=40,ipady=40)

main_window.mainloop()