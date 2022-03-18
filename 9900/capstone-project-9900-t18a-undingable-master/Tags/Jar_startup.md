# Jar包启动步骤
后端同学：
1. 在 IDEA 的右侧 Maven clean -> install
2. 观察 target 目录是否已经产生了 jar 包

前端同学：
1. 如未安装 Java， 前往 (https://www.java.com/zh-CN/) -> 免费 Java 安装
2. 如果 Mac， 在设置的最下面安装完后会出现 Java， 点开可进行 Java相关设置
3. 安装 Java 后， 找到项目目录下的 (Tags/Back-end-1.0-SNAPSHOT.jar)
4. 有能力同学可以 cd 到该目录直接运行，也可以复制这个 Jar 包到任意位置
5. 最后一步， 在 Jar 包的目录下运行该命令：
``` shell
Java -jar Back-end-1.0-SNAPSHOT.jar
```
如果观察到 Java 启动 tomcat 8080 端口即为启动成功

# 端口
- 登录端口(POST)
```shell
    localhost:8080/user/login
```

需要参数： name, password

- 注册端口(POST)
```shell
    localhost:8080/user/register
```
需要参数：name, password, role, email

Swagger访问地址http://localhost:8080/swagger-ui.html
