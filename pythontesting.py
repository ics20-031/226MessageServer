#!/usr/bin/python3
import re

data = "PUT 12341 234Hi"
data = data[3:] # Remove PUT from the string
print(data)
data = data.replace(" ", "")
print(data)
# print("key is: " + key)
# print("values is: " + value)

# if (value == ""):
#     print("no value")
# if not (re.match('^[a-zA-Z0-9]{8}$', key)):
#     print("wrong key")

