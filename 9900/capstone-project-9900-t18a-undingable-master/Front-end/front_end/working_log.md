#  Front-end working log:
## 此日志为所有编辑者编辑内容的信息更新：

***额外注意：新更新的放在最前面***

### 更新如下：

***
##### 编辑时间 悉尼时间10.20 4:16pm
##### 编辑者：Julia
###### 编辑内容：
* antd配置更新，可能需要的命令如下：
  * antd高级配置： yarn add @craco/craco
  * antd主题颜色更改： yarn add craco-less

参考文档：https://ant.design/docs/react/use-with-create-react-app-cn
直接看高级配置那一节

* 如果样式无法显示，把App.less里的第一句import改为下面这个：
  * @import 'antd/dist/antd.css' 
***
##### 编辑时间：北京时间10.10 2:32pm
##### 编辑者：Julia
###### 编辑内容：
* 上传User page
***
 
##### 编辑时间：北京时间10.9 6:14pm
##### 编辑者：Sean
###### 编辑内容：
* 脚手架引入antd
* 增加前端work log文档
* ***git ignore文件已经忽视node_modules,此部分需要自己下载，放进运行文件夹***
***

#####
package.json
 "start": "HOST=0.0.0.0 craco start",
can't work, then change into:
"start": "./node_modules/.bin/react-scripts start",
