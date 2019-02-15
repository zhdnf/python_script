import os
import logconf
import pexpect
from apscheduler.schedulers.blocking import BlockingScheduler

# rsync 被同步的源文件
src_path = '192.168.203.155:/root/rsync'

# rsync 同步后的目标目录
dst_path = '/root/rsync'

# ssh私钥
# ssh_path = '/root/.ssh/rsync'

# 服务日志目录
log_path = '/export/rsync'

# 远程ssh密码
passwd = ''

def job_run():
    global update
    global error

    try:    
        # 自动化交互
        child = pexpect.spawn("rsync -adt %s %s"%(src_path, dst_path))
        child.expect("root@192.168.203.155's password:")
        child.sendline(passwd)
        child.read()

        # ssh免密
        # os.system("rsync -adt -e 'ssh -i %s ' %s %s %s"%(ssh_path, src_path, dst_path))

        update_str = "sync successful"
        update.logger_update().info(update_str)

    except Exception as e:
        error_str = "sync error: %s:%s"%(type(e),e)
        error.logger_error().error(error_str)

if __name__ == "__main__":

    if os.path.lexists(dst_path) == False:
        os.system('mkdir -p %s'%dst_path)

    if os.path.lexists(log_path) == False:
        os.system('mkdir -p %s'%log_path)

    update_file=log_path+'/update.log'
    error_file=log_path+'/error.log'

    # 日志初始化
    update=logconf.LogConf(update_file)
    error=logconf.LogConf(error_file)

    # 定时任务初始化
    scheduler=BlockingScheduler()

    scheduler.add_job(func=job_run,trigger='interval',seconds=5)
    scheduler.start()

