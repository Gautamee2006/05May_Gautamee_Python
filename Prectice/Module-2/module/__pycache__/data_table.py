import pandas as p
import requests as r

url="https://fakestoreapi.com/products"
x={}
req=r.get(url)
data=req.json()
print(data)


dic=list(data)
#print(dic)
df=p.DataFrame(data)
print(df[['id','title','price','rating']])