# named pipe Client
# encoding: utf-8

import os
import time
from setting import NSSH_PATH

write_path = "/tmp/server_in.pipe"
read_path = "/tmp/server_out.pipe"

def client(message):
   if 'my' in message:
        my_client(message)


def my_client(message):
    username = ''
    passwd = ''
    auth_name = ''
    auth_passwd = ''

    parts = message.split(' ')
    
    username = parts[2]
    passwd = parts[3]

    # 写
    f = os.open(write_path, os.O_SYNC | os.O_CREAT | os.O_RDWR )
    
    # 读
    rf = None
    
    # Client发送请求
    req = 'my' + ' ' + username + ' '+ passwd
    req = bytes(req, encoding='utf-8')
    len_send = os.write(f, req)

    try:
        if rf == None:
            # *要点1：在这里第一次打开read_path，实际这里的open是一个阻塞操作
            # 打开的时机很重要。如果在程序刚开始，没发送请求就打开read_path，肯定会阻塞住
            rf = os.open(read_path, os.O_RDONLY)
        
        # 接收Server回应
        s = os.read(rf,50)
    except KeyboardInterrupt:
        print("\n\r")
        exit(0)

    s = str(s, encoding='utf-8')

    parts = s.split("###")
   
    # 验证成功
    if parts[0] == 'yes':
        auth_name = parts[1].split(' ')[0]
        auth_passwd = parts[1].split(' ')[1]

        # if len(s)==0:
        # 一般来说，是管道被意外关闭了，比如Server退出了
            # print("error")

        os.close(f)
        os.close(rf)
        
        # 执行命令
        os.system("python3 %s %s %s %s"%(NSSH_PATH, username, auth_name, auth_passwd))
    else:
        print(s)
        
        os.close(f)
        os.close(rf)


if __name__ == '__main__':
    message = 'haha'
    client(message)

