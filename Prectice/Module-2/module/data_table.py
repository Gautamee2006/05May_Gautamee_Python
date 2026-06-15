import pandas 
import requests as r

url="https://fakestoreapi.com/products"
x={}
req=r.get(url)
data=req.json()


l=list(data)
df=pandas.DataFrame(data)
print(df[['id','title','price','rating']])