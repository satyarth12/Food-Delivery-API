import json
import os
import random
import requests
import string
from django.utils.text import slugify
from io import BytesIO


# # function to add to JSON
# def write_json(new_data, user):
#     src = './utils/data/'
#     filename = src+str(user.phone)
#     with open(filename,'r+') as file:
#         # First we load existing data into a dict.
#         file_data = json.load(file)
#         file_data.update(new_data)
#         file.seek(0)
#         json.dump(file_data, file, indent = 4)
#         return file_data




# def write_data(data, user):
#     src='./utils/data/'
#     filename = src+str(user.phone)
#     with open(filename,'w+') as file:
#         json.dump(data, file, indent=4)





def send_otp(phone):
    if phone:
        
        key = random.randint(999, 9999)
        phone = str(phone)
        otp_key = str(key)

        link = f'https://2factor.in/API/R1/?module=TRANS_SMS&apikey=b3628db0-ce73-11eb-8089-0200cd936042&to={phone}&from=HMESHF&templatename=SMSTemp&var1=USER&var2={otp_key}'
        result = requests.get(link, verify=False)

        return otp_key




import uuid
def generate_ref_code():
    code = str(uuid.uuid4()).replace('-','')[:12]
    return code



