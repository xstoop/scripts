#!/usr/bin/env python
# coding: utf-8
# author: xstoop@163.com
# see: http://fabric-chs.readthedocs.io/zh_CN/chs/index.html

from fabric.api import *
from fabric.contrib.files import exists
import os

if len(env.hosts)==0 and os.path.exists('host.py'):
    import host
    env=host.env

env.eagerly_disconnect = True #在每个独立任务完成后关闭连接
env.skip_bad_hosts = True #跳过SSH连接失败的主机而不是exit

#拉取镜像并运行容器
@parallel(pool_size=5)
def deploy():
    start_docker()
    #with hide('running', 'stdout', 'stderr'):
    #pull镜像
    print('%(host)s pull mirror' % env)
    run('docker login --username=username  --password=password --email=email your-registry-hub.com')
    #with show('running', 'stdout', 'stderr'):
    run('docker pull your-registry-hub.com/project:latest')
    print('%(host)s pull mirror over' % env)

    #停掉并删除旧容器
    print('%(host)s stop and remove old project container' % env)
    with settings(warn_only=True):
        stop = run('docker stop project')
    if stop.failed == 0:
        run('docker rm project')
    print('%(host)s stop and remove old project container over' % env)

    #启动新容器
    print('%(host)s create new project container' % env)
    run('docker run --name project -it -d -p 8003:80 --restart=always your-registry-hub.com/project:latest')
    print('%(host)s create new project container over' % env)

#查看project status状态
def project_status():
    if docker_pid_exist() == True:
        run('docker ps -a | grep project')

#停止project容器
def stop_project():
    if docker_pid_exist() == True:
        run('docker stop project')

#启动project容器
def start_project():
    if docker_pid_exist() == True:
        run('docker start project')

#重新启动project项目
def restart_project():
    stop_project()
    start_project()

#启动docker
def start_docker():
    if docker_pid_exist() == False:
        run('service docker start',pty=False)
    else:
        print('%(host)s docker is already start' % env)

#停止docker
def stop_docker():
    if docker_pid_exist() == False:
        print('%(host)s docker is already stop' % env)
    else:
        run('service docker stop',pty=False)

#查看docker运行状态
def docker_status():
    with settings(warn_only=True):
        run('service docker status',pty=False)

#检查docker是否在运行
def docker_pid_exist():
    return exists('/var/run/docker.pid')

#安装docker：该方法只适用centos6.9安装docker1.7版本
def install_docker():
    if test_docker() == False:
        print('%(host)s now begin install...' % env)
        with settings(warn_only=True):
            with hide('stdout'):
                # 升级device-mapper
                run('yum -y upgrade device-mapper-libs')

                docker_rpm = run('rpm -qa | grep epel-release-6-8.noarch')
                if docker_rpm != 'epel-release-6-8.noarch':
                    # 添加docker rpm
                    run('rpm -iUvh http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm > /dev/null 2>&1')

                # 安装docker
                install = run('yum -y install docker-io')
                if install.failed == 0:
                    # 上传docker启动文件,增加了启动前创建自定义的docker网桥
                    put('./init.d-docker','/etc/init.d/docker')
                    run('chmod +x /etc/init.d/docker')
                    # 上传docker配置文件，自定义加速器与网桥
                    put('./cfg-docker','/etc/sysconfig/docker')
                    run('service docker start',pty=False)

#卸载docker
def uninstall_docker():
    stop_docker()
    with settings(warn_only=True):
        run('ifconfig zdocker0 down')
        run('brctl delbr zdocker0')
        run('yum -y remove docker-io')

#检查docker运行状态
def test_docker():
    if exists('/usr/bin/docker') == False:
        print('%(host)s docker is not install' % env)
        return False
    else:
        if docker_pid_exist() == False:
            print('%(host)s docker is already install but not running' % env)
        else:
            print('%(host)s docker is already install and is running' % env)
        return True

#检测SSH主机连接情况
def test_host_cont():
    with settings(warn_only=True):
        with hide('running', 'stdout'):
            run_result=run('pwd')
            if run_result.failed == 0:
                print('%(host)s connection success' % env)
            else:
                print('%(host)s connection failed' % env)
