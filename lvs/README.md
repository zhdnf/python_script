# LVS环境搭建

## 实现目标
- 将10.13.68.79的请求负载到10.13.68.78
- 方式：wlc + nat
- 服务：syslog(udp:514),grpc(tcp:50051)
- 兼容: centos6.5  centos7

## 实现工具
- keepalived
- ipvsadm

## 实现过程
1. 下载keepalived, ipvsadm
2. 根据负载需要改写配置文件，keepalived.conf
3. 打开ip转发功能
4. 重启keepalived服务

