# print-bot

### 场景简介

打印机在办公室里面，但是几个小伙伴平常都在实验室做事，2个位置之间没有网络连接，所以没办法通过常规的方式打印文件。以前，我们都是通过微信发送给办公室的同事帮忙打印，但经常麻烦别人总是不太好，所以构建了这个系统。


### 框架结构

其结构如下：

'''
+----------------------+            +-----------+-------------+         +------------+
|                      |            |           |             |         |            |
|                      |            |           |             |         |            |
|    wechat mini APP   +----------->+   NginX   |   Python    |         |   Python   |
|                      |            |           |             |         |            |        +-----------+
|                      |            |     +     |             |         |            |        |           |
+----------------------+            |           |             |         |            |        |           |
                                    |    PHP    | TCP Server  +-------->+ TCP Client +------->+ Printer   |
                                    |           |             |         |            |        |           |
+----------------------+            |           |             |         |            |        |           |
|                      |            |           |             |         |            |        +-----------+
|                      |            |           |             |         |            |
|      PC Tool         +----------->+           |             |         |            |
|                      |            |           |             |         |            |
|                      |            |           |             |         |            |
+----------------------+            +-----------+-------------+         +------------+



        User client                         Server                          Client               Printer
'''

1. User Client端。包括2个部分，其一是微信小程序客户端，可以选择聊天记录中的文件，并发送到打印机；另一个是电脑端使用的工具，实现和小程序一样的功能。

2. Server端。包含了一个Nginx做http和https的代理，然后通过php做简单的处理，存在到固定的打印目录下；另外，TCP Server会监控打印目录，如果有变换，就通知相连的TCP Client来抓取打印文件；

3. Client端。最好的方案当然是利用pi之类的平台，但是我们办公室的打印是联想的，无linux驱动，无力吐槽。所以最后是把Client端放在了小伙伴的OA PC上，反正他也不用。Client端在在获取打印的命令后，会去服务端get文档，然后调用print打印，最后通知Server打印完成；

4. Printer端。打印机，只要在PC上设置好默认的打印机选型即可；

