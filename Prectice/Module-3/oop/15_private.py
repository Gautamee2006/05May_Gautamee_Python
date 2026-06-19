class studinfo:
    #private
    __id=12
    __name="gautamee"

    def __getdata(self):
        print("id:",self.__id)
        print("name:",self.__name)

    def display(self):
        self.__getdata()

st=studinfo()
st.display()