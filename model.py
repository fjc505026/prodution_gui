

class Model:

    def __init__(self,eui) -> None:
        self.board_info={}
        self.test_detail={}
        self.aws_info={}
        self.test_result=''
        self.test_debug=''
        self.provsion_result=''


    def get_board_info(self,key=''):
        if key=='':
            return self.board_info
        return self.board_info[key]
        
    def get_test_detail(self,key=''):
        if key=='':
            return self.test_detail
        return self.test_detail[key] 

    def get_aws_info(self,key):
        if key=='':
            return self.aws_info
        return self.aws_info[key] 

    def get_test_result(self):
        return self.test_result

    def get_test_debug(self):
        return self.test_debug 

    def get_provsion_result(self):
        return self.provsion_result   
    
    def set_board_info(self,info,key=''):
        if key=='':
            self.board_info=info
        else:    
            self.board_info[key]={key:info}
        
    def set_test_detail(self,info,key=''):
        if key=='':
            self.test_detail=info
        else:    
            self.test_detail[key]={key:info}
                  
    def set_aws_info(self,info,key=''):
        if key=='':
            self.aws_info=info
        else:    
            self.aws_info[key]={key:info} 

    def set_test_result(self,test_result):
        self.test_result=test_result

    def set__test_debug(self,test_debug):
        self.test_debug=test_debug        

    def get_provsion_result(self,provsion_result):
        self.provsion_result=provsion_result  


