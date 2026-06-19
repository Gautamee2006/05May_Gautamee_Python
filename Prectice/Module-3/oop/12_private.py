class studeinfo:
    #private
    __stid=101
    __stnm="gautamee"

    def __getdata(self):
        print("id:",self.__stid)
        print("name:",self.__stnm)
    
    def display(self):
        self.__getdata()

st=studeinfo()
st.display()