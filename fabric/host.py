#!/usr/bin/env python
# coding: utf-8

from fabric.api import env

#ssh默认登录用户
env.user = 'root'   

#ssh主机列表
env.hosts = [
                'root@ip1:port', #服务器1
                'root@ip2:port', #服务器2
            ]
            
#ssh默认登录密码
env.password = 'password'  

#ssh指定主机的登录密码
env.passwords = {
                    'root@ip1:port' : 'password',
		                'root@ip2:port' : 'password',
		            }
