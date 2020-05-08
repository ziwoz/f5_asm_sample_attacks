#### base64 encoding #### (a-z, A-z, 0-9, +, /)
# https://www.base64encoder.io/python/
# https://stackabuse.com/encoding-and-decoding-base64-strings-in-python/

import base64

data = "https://www.iwoz.com/iwoz.html"

# Standard Base64 Encoding
encodedBytes = base64.b64encode(data.encode("utf-8"))
encodedStr = str(encodedBytes, "utf-8")

print(encodedStr)

# aHR0cHM6Ly93d3cuaXdvei5jb20vaXdvei5odG1s

##### Decoding a base64 ######


import base64

base64_message = 'aHR0cHM6Ly93d3cuaXdvei5jb20vaXdvei5odG1s'
base64_bytes = base64_message.encode('utf-8')
message_bytes = base64.b64decode(base64_bytes)
message = message_bytes.decode('utf-8')

print(message)



