import qrcode

data = "+919601933815"

img = qrcode.make(data)

img.save("qrcode1.png")
