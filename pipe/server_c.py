# named pipe Server
# encoding: utf-8

import os, time
import setting
import hashlib

# certify username and passwd by file
cert = ''

# read auth_name and auth_passwd from file`
contains = ''

read_path = "/tmp/server_in.pipe"
write_path = "/tmp/server_out.pipe"

try:
    # 创建命名管道
    os.mkfifo( write_path )
    os.mkfifo( read_path )
except OSError as e:
    # 如果命名管道已经创建过了，那么无所谓
    print("mkfifo error:", e)

# 验证
with open("%s"%user_path "r") as f:  
    cert = f.read().split("\n")
    
with open('%s'%auth_path, 'r') as f:
    contains = f.read().split(' ')

while True:
    # 写入和读取的文件，正好和Client相反
    rf = os.open(read_path, os.O_RDONLY )
    f = os.open(write_path, os.O_SYNC | os.O_CREAT | os.O_RDWR )

    # 接收请求

    res = os.read(rf,50)
    res = str(res, encoding='utf-8')

    if len(res) == 0:
        # 没有收到字符，一般是唯一的发送方被关闭了。
        continue
    
    if 'my' in res:
        # print(res)
    
        # 验证用户和密码
        flag = False
        parts = res.split(' ')

        # print(parts)

        username = parts[1]
        passwd = parts[2]
           
        m = hashlib.md5()
        m.update(passwd.encode('utf-8'))
        passwd_cert = str(m.digest())
        
        for i in cert:
            if username == i.split("###")[0] and passwd_cert == i.split("###")[1]:
                username_auth = username
                flag = True

        if flag == True:

            auth_name = contains[0]
            auth_passwd = contains[1].replace('\n','')

            req = auth_name + ' ' +  auth_passwd 
            req = 'yes###' + req
            req = bytes(req, encoding='utf-8')

            # print(req)
            
            # 发送消息给客户端 
            os.write(f, req)

        else:
            os.write(f, b"please relogin")

    else:
        os.write(f, b'error')
    
    os.close(f)
    os.close(rf)
