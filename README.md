
# EbSite Vercel
本项目采用 Python Flask + Vercel 部署。
 

# 通过python在本地调试
将项目clone到本地后，安装所有依赖库
运行 website/index.py

# 通过vercel在本地运行

```bash
npm i -g vercel
vercel dev
```

Your Flask application is now available at `http://localhost:3000`.


# 部署新项目到vercel

点击以下按钮即可免费创建一个项目

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fyibo7%2Febsite-for-vercel.git&env=SITE_KEY,MONGODB_SERV,REDIS_SERV&envDescription=SITE_KEY%E6%98%AF%E7%BD%91%E7%AB%99%E5%AF%86%E9%92%A5%2CMONGODB_SERV%E6%98%AFMongoDb%E6%95%B0%E6%8D%AE%E5%BA%93%E8%BF%9E%E6%8E%A5%E5%9C%B0%E5%9D%80%2CREDIS_SERV%E6%98%AFRedis%E8%BF%9E%E6%8E%A5%E5%9C%B0%E5%9D%80&project-name=ebsite-for-vercel&repository-name=ebsite-for-vercel)

- 1、选择你的github账号，并创建项目
- 2、填写环境变量，MONGODB_SERV（数据库连接串），REDIS_SERV（Redis连接串），MONGODB_NAME（数据库名称）
- 

# 更新项目
提交项目后会自动更新

注：
>如果修改了requirements.txt，提交后也一样会自动更新，不需要重新部署。

# 安装
可以点击Deploy一键安装，填写新的数据库后，会打开后台登录页面进行数据初始化：
/login_ad
后台登录的账号与密码是：
user: admin
pass: 111111
 

