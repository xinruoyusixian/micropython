import socket 


# 捕获异常，如果在"try" 代码块中意外中断，则停止关闭套接字
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)               # 创建UDP的套接字
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)              # 设置套接字属性
    ip=network.WLAN(network.STA_IF).ifconfig()[0]                      # 获取本机ip地址
    s.bind((ip,5353))                                                  # 绑定ip和端口号
    print('waiting...')
    while True:
        data,addr=s.recvfrom(1024)                           # 接收对方发送过来的数据,读取字节设为1024字节,返回(data,addr)二元组
        print('received:',data,'from',addr)                  # 打印接收到数据                                     
        

# 当捕获异常,关闭套接字、网络
except:
  pass
