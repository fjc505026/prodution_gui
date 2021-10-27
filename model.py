

from tkinter.constants import NONE


class Model:

    def __init__(self,eui) -> None:
        self.board_info={}
        self.test_detail={}
        self.aws_info={}
        self.test_result=''
        self.test_debug=''
        self.provsion_result=''

    #view call this to update view
    def get_board_info(self, key=NONE):
        if key==NONE:
            return self.board_info
        return self.board_info[key]
        
    def get_test_detail(self,key=NONE):
        if key==NONE:
            return self.test_detail
        return self.test_detail[key] 

    def get_aws_info(self,key):
        if key==NONE:
            return self.aws_info
        return self.aws_info[key] 

    def get_test_result(self):
        return self.test_result

    def get_test_debug(self):
        return self.test_debug 

    def get_provsion_result(self):
        return self.provsion_result   
    
    #connect db, update this
    def set_board_info(self,info,key=NONE):
        if key==NONE:
            self.board_info=info
        else:    
            self.board_info[key]=info
        
    def set_test_detail(self,info,key=NONE):
        if key==NONE:
            self.test_detail=info
        else:    
            self.test_detail[key]=info
                  
    def set_aws_info(self,info,key=NONE):
        if key==NONE:
            self.aws_info=info
        else:    
            self.aws_info[key]=info 

    def set_test_result(self,test_result):
        self.test_result=test_result

    def set__test_debug(self,test_debug):
        self.test_debug=test_debug        

    def get_provsion_result(self,provsion_result):
        self.provsion_result=provsion_result  


