# encoding=utf-8

import os
import sys
import re
import socket
import time
import paramiko
from paramiko.py3compat import u

import setting
from utils import logconf

re = re.compile("\r")

try:
    import termios
    import tty

    has_termios = True
except ImportError:

    has_termios = False


def posix_shell(chan, log_opt):
    import select
    
    # 当前输入流str, 判断是否输入回车
    curStr=''
    # 输入回车，输入的所有str即命令
    full_cmd=''
    
    oldtty = termios.tcgetattr(sys.stdin)
    
    try:
        tty.setraw(sys.stdin.fileno())
        
        # tty配置
        # newtty = termios.tcgetattr(sys.stdin.fileno())
        # newtty[6][termios.VINTR] = 0
        # newtty[6][termios.VQUIT] = 0
        # newtty[6][termios.VSUSP] = 0
        # termios.tcsetattr(sys.stdin, termios.TCSAFLUSH, newtty)

        tty.setcbreak(sys.stdin.fileno())
        

        chan.settimeout(0.0)
        
        while True:
            r, w, e = select.select([chan, sys.stdin], [], [])

            if chan in r:
                try:
                    x = u(chan.recv(1024))
                    if len(x) == 0:
                        sys.stdout.write("-"*40+"\r\n")
                        break
                    if curStr != '\r':
                        cmdArray = x.split('\n')
                        cmd = cmdArray[0]
                        cmdArray = cmd.split(' ')
                        new_cmd = cmdArray[len(cmdArray)-1]
                        if ''!= new_cmd:
                            cmd = new_cmd
                        full_cmd = full_cmd + cmd
                    elif ''!=full_cmd:
                        # 写入日志
                        log_opt.logger_opt().info(full_cmd)
                        full_cmd = ''
                    
                    sys.stdout.write(x)
                    sys.stdout.flush()

                except socket.timeout:
                    pass

            if sys.stdin in r:
                x = sys.stdin.read(1)
                curStr = x
                if x == '':
                    full_cmd = full_cmd + ''
                if len(x) == 0:
                    break

                chan.send(x)
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oldtty)


def audit(ip, username, auth_name, auth_passwd):
    # 创建会话并认证
    tran = paramiko.Transport((ip, 22, ))
    tran.start_client()
    tran.auth_password(auth_name, auth_passwd)
    chan = tran.open_session()

    # 日志初始化
    local_time = time.localtime()
    time_str1 = time.strftime("%Y-%m-%d", local_time)

    # time_str2 = time.strftime("%H:%M:%S")
    log_opt_path = setting.AUDIT_PATH + '/opt/' + username
    log_login_out_path = setting.AUDIT_PATH + '/login_out/' + username

    if os.path.lexists(log_opt_path) == True:
        pass
    else:
        os.system('mkdir -p %s'%log_opt_path)
    
    if os.path.lexists(log_login_out_path) == True:
        pass
    else:
        os.system('mkdir -p %s'%log_login_out_path)
    
    log_opt_file = time_str1 + '_opt.log'
    log_login_out_file = time_str1 + '_login_out.log'

    log_opt_path = log_opt_path + "/" + log_opt_file
    log_login_out_path = log_login_out_path + "/" + log_login_out_file

    log_opt = logconf.LogConf(log_opt_path)
    log_login_out = logconf.LogConf(log_login_out_path)
   
    # login日志
    log_login_str = username + ' - ' + ip + ' - login'
    log_login_out.logger_opt().info(log_login_str)

    #打开虚拟终端
    chan.get_pty()
    chan.invoke_shell()
    posix_shell(chan, log_opt)
    
    # logout日志
    log_logout_str = username + '-' + ip + ' - logout'
    log_login_out.logger_opt().info(log_logout_str)


if __name__=='__main__':
    ip = '192.168.203.198'
    audit(ip, "user1", "root", '123456')
