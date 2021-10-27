import tkinter as tk
from tkinter import  Text, Tk, ttk
from tkinter.messagebox import showerror, showwarning, showinfo
from tkinter.constants import BOTTOM, CENTER, LEFT, RIGHT, TOP, TRUE
from scanner.ecia import Scanner


class View(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.is_auto_scan = tk.BooleanVar()
        self.scanner=''

        self.info_frame_vars=[]
        self.detail_frame_vars=[]
        self.aws_frame_vars=[]

        main_frame = tk.Frame(parent)
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

        btn_test = tk.Button(frame_2_col1, text="Start Test", fg="blue",font=10, command=self.btn_start_handler)
        btn_test.grid(row=0, column=0, columnspan=2, sticky="nsew", ipadx=20, ipady=20)

        radio_scan=tk.Radiobutton(frame_2_col1, text="scan", variable=self.is_auto_scan, value=True,
                        command=self.sel)
        radio_scan.grid(row=1, column=0,  sticky="w", padx=5, pady=5)
        radio_mannul=tk.Radiobutton(frame_2_col1, text="manual", variable=self.is_auto_scan, value=False,
                        command=self.sel)
        radio_mannul.grid(row=1, column=1,  sticky="w", padx=5, pady=5)

        eui_label = ttk.Label(frame_2_col1, text="board eui:")
        eui_label.grid(row=2, column=0,  sticky="w", padx=5, pady=5)
        self.eui_entry = ttk.Entry(frame_2_col1)
        self.eui_entry.grid(row=2, column=1,  sticky="w", padx=5, pady=5)

        ##frame_2_col2   board_info
        key_list=[]
        value_list=[]  #not used
        self.board_info={'board eui':'','board type':'DT1119','board Rev':'A','project':'Viotel','batch':'256'}
        for key,value in self.board_info.items():
            key_list.append(key)
            value_list.append(value)
        
        self.generate_labels_with_lableframe(frame_2_col2,"INFO.", key_list, self.info_frame_vars)

        ##frame_2_col3   test detail
        ele_list=['modem test','gps test','flash test','battery test','solar test']
        self.generate_labels_with_lableframe(frame_2_col3,"DETAIL",ele_list,self.detail_frame_vars)

        ##frame_2_col4   test result
        labelframe = tk.LabelFrame(frame_2_col4, text="RESULT")
        labelframe.pack(fill="both", expand="yes",ipadx=20,ipady=20)
        self.test_result_label = tk.Label(labelframe, relief="ridge",font=('bold', 20), anchor=CENTER)
        self.test_result_label.pack(ipadx=40,ipady=40)

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

        btn_provision = tk.Button(frame_2_col1, text="Provision",fg="blue",font=10, command=self.btn_provision_handler)
        btn_provision.pack(ipadx=20, ipady=20)

        ele_list=['thing name','node type']
        self.generate_labels_with_lableframe(frame_2_col2,"AWS Info",ele_list,self.aws_frame_vars)

        labelframe = tk.LabelFrame(frame_2_col3, text="RESULT")
        labelframe.pack(fill="both", expand="yes",ipadx=20,ipady=20)
        self.provision_result_label = tk.Label(labelframe,relief="ridge",font=('bold', 20),anchor=CENTER)
        self.provision_result_label.pack(ipadx=40,ipady=40)

    def set_controller(self, controller):
        self.controller = controller

    def btn_start_handler(self):
        if not self.is_auto_scan.get():
            if not self.eui_entry.get().startswith("98") or len(self.eui_entry.get())!=16:
                msg="please type valid eui, 16 digitals"
                #print("msg")
                showwarning(title='Warning',message=msg)
            else:
                self.controller.model.set_board_info(self.eui_entry.get(), 'eui')
                print(self.controller.model.get_board_info('eui'))
                key_list=[]
                value_list=[]
                tmp={'board eui':self.controller.model.get_board_info('eui'),'board type':'DT1118','board Rev':'B','project':'Viotel','batch':'256'}
                for key,value in tmp.items():
                    key_list.append(key)
                    value_list.append(value)

                self.update_labels_in_lableframe(self.info_frame_vars,value_list)
                self.update_test_result_label("PASS")
        
        else:
            if not self.scanner:
                try:
                    self.scanner = Scanner()
                except: #Exception Scanner use exit(0)
                    msg="Can't find Scanner, please have a check and another try"
                    #print("msg")
                    showwarning(title='Warning',message=msg)
                    return

            self.scanner.drain()
            print("Please scan device barcode(plug in battery and switch on the board)")
            bc = self.scanner.scan()
            if "S" not in bc:
                msg="Could not decode barcode"
                #print(msg)
                showwarning(title='Warning',message=msg)
            self.controller.model.set_board_info(bc["S"],"eui")    

    def btn_provision_handler(self):
        pass
        #... self.update_labels_in_lableframe(self.aws_frame_vars,value_list)

    def sel(self):
        if self.is_auto_scan.get():
            print("Scanner Mode") 
        else:    
            print("Mannual Mode") 
    
    def generate_labels_with_lableframe(self,master_frame,framename, key_list, vars_list):
        row_index=list(range(0,len(key_list)))
        labelframe = tk.LabelFrame(master_frame, text=framename)
        labelframe.pack(fill="both", expand="yes")
        labelframe.rowconfigure(row_index, minsize=10, weight=1)
        labelframe.columnconfigure([0,1], minsize=100, weight=1)
        
        for idx in row_index:
            board_eui_label = tk.Label(labelframe, text=key_list[idx]+':')
            board_eui_label.grid(row=idx, column=0,  sticky="w", padx=5, pady=5)
            vars_list.append(tk.StringVar())
            board_eui_data = tk.Label(labelframe, textvariable=vars_list[idx])
            board_eui_data.grid(row=idx, column=1,  sticky="w", padx=5, pady=5)
           
    def update_labels_in_lableframe(self,var_list,val_list):
        row_index=list(range(0,len(var_list)))
        for idx in row_index:
            var_list[idx].set(val_list[idx])


    def update_test_result_label(self, result):
        if result == 'PASS':
            self.test_result_label.config(text="PASS",fg="green")
        else:
            self.test_result_label.config(text="FAIL",fg="red") 


    def update_provision_result_label(self,result):
        if result == 'PASS':
            self.provision_result_label.config(text="PASS",fg="green")
        else:
            self.provision_result_label.config(text="FAIL",fg="red")       

    

