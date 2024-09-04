# 自动部署腾讯云的免费证书

----

> 证书还没到期,还没测试

## 一.准备工作

1. 域名在腾讯云上
2. 证书也是用的腾讯云的证书

## 二.使用步骤:

### 0.把本仓库fork了

### 1.腾讯云创建一个专门用于管理SSL证书的子账号,并获取secret_id和secret_key

![图片](./images/setp1.png)

> 注意访问方式和访问权限,点击创建用户后即可拿到secret_id和secret_key

### 2.在自己的仓库中添加环境变量

Fork 本仓库后, 在你自己的仓库中, 进入 ```Settings - Secrets and variables - Actions```, 添加环境变量作为 ```Repository secrets```.


| 变量名称               | 值类型    | 示例                 | 说明                 |
|--------------------|--------|--------------------|--------------------|
| DOMAIN             | String | xxx.com            | 要部署的域名             |
| TENCENT_SECRET_ID  | String | xxxxxx             | 第一步申请的secret_id    |
| TENCENT_SECRET_KEY | String | xxxxxx             | 第一步申请的secret_key   |
| UPLOAD_PATH_PREFIX | String | /docker/Nginx/ssl/ | 证书文件存放路径的前缀,结尾腰带斜杠 |
| SERVICE_HOSTNAME   | String | 1.1.1.1            | 服务器地址              |
| SERVICE_PORT       | int    | 22                 | 服务器端口              |
| SERVICE_USERNAME   | String | root               | 服务器登录用户名           |
| SERVICE_PASSWORD   | String | root               | 服务器登录密码            |

### 3.每天定时执行检查

修改下.github/workflows/python-script.yml文件中的内容

把文件中on的这一部分修改为每天午夜12点执行一次

也可以修改cron表达式符合你需要的更新频率

```yaml
on:
  schedule:
    - cron: '0 0 * * *'
```
