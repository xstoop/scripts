[fabric](http://fabric-chs.readthedocs.io/zh_CN/chs/index.html)脚本，该脚本可以做如下事情：

* 在多台远程服务器上自动发布与管理docker容器服务
* 在多台远程服务器上自动安装docker
* 可根据需求自定义其他方法

使用该脚本前，需要先安装fabric：

```
yum -y install fabric
```

要在多台远程服务器上运行时，需要创建host.py脚本，并在host.py中添加所有服务器的SSH登录信息，配置信息见host.py.example文件。

执行docker服务的发布运行如下命令：

```
fab deploy
```

执行docker安装运行如下命令：
```
fab install_docker
```

在指定单独一台服务器上运行命令时，可以不将服务器信息添加进行host.py，通过运行命令时直接指定参数：
```
fab -H username@ip:port -p password install_docker
```

查看可用的任务命令

```
fab -l

    deploy              发布与启动icproxy容器服务
    docker_pid_exist    判断docker pid是否启动
    docker_status       查看docker的启动状态
    icproxy_status      查看icproxy容器的状态
    ifconfig            查看网络接口信息
    install_docker      安装docker        
    restart_icproxy     重启icproxy容器
    start_docker        启动docker
    start_icproxy       启动icproxy容器
    stop_docker         停止docker
    stop_icproxy        停止icproxy容器
    test_docker         检查docker的安装情况
    test_host_cont      测试主机连接
    uninstall_docker    卸载docker
```
