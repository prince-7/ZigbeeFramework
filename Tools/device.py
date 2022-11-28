from secure_tool import Secure
from unsecure_tool import Unsecure

import os

mode = input("Enter mode : ")

if(mode == "secure"):
    secure = Secure()
    secure.start()
else:
    unsecure = Unsecure()
    unsecure.start()