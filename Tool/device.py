from secure_tool import Secure
from unsecure_tool import Unsecure

mode = input("Enter mode : ")

if(mode == "secure"):
    secure = Secure()
    secure.start()
else:
    unsecure = Unsecure()
    unsecure.start()