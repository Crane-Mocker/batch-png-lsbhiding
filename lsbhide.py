#c0conut 2020.12.20
#Using stegano to implement batch png lsbhiding
#hide_msg can't be long

import os
from stegano import lsb
import random
import string
import math

target_dir = os.walk("test")
index = 1

for path, dir_list, file_list in target_dir:
    for file_name in file_list:
       cur_target = os.path.join(path, file_name)
       hide_len = random.randint(10, 20)
       hide_msg = ''.join(random.sample(string.ascii_letters + string.digits, hide_len))
      #hide_msg = random.random()*math.pow(2, )
      #get a random n-bit binary hide_msg, n cannot be large
       print(hide_msg)
       secret = lsb.hide(cur_target, hide_msg)
       secret.save("./res/"+str(index)+"_lsb_1.png")
       index += 1
