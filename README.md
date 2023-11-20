
# EbSite CMS Vercel

这是一个轻量级CMS系统，可一键部署在Vercel上，轻松实现个人或简单的企业网，
借自Vercel的免费服务及相关数据库的免费服务，你可以实现真正免费独立网站。


官方演示站点:https://ebsite-for-vercel.vercel.app/

### 主要功能项：
- 前后台用户及权限管理
- 分类、内容与专题管理
- 可扩展CMS内容模型
- 可扩展数据调用部件
- 自定义表单
- 可定制主题皮肤
- 可监听触发器

请点赞与关注，我将有动力在后续会更新更多的功能项。

# 运行依赖
- 运行环境本项目采用 Python Flask + Vercel 部署。
- 数据库: MongoDb
    - 免费申请512MB: https://cloud.mongodb.com
- 缓存: Redis
    - 免费申请30M: https://app.redislabs.com


# 通过python在本地调试
将项目clone到本地后，安装所有依赖库后运行 website/index.py

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
- 2、填写环境变量
  - MONGODB_SERV（数据库连接串）
  - REDIS_SERV（Redis连接串）
  - MONGODB_NAME（数据库名称）
- 3、初始化默认数据及演示数据
    
    打开后台登录页面:https://你的域名/login_ad
    这里会自动完成数据的初始化，然后你可以使用以下账号密码登录后台:
    - user: admin
    - pass: 111111
   

# 更新项目
如果你在上面安装的页面上选择了：Create private Git Repository
，提交后会复制一份EbSite CMS Vercel源码在你的github下。
你可以在这个基础上随意修改你的项目，
如果你将修改的代码提交到github,系统会自动更新到vercel上，所以在提交代码前，要确认你的代码是否正确无误，
否则会影响你正在运行中的网站。
### 注意
- 如果你修改了requirements.txt，提交后代码后，vercel会自动安装新的python库，并重新部署，无需手动处理。
- 如果你在vercel上修改了环境变量，则需要你重新部署(也可通过随意改动源代码提交让后其自动重新部署)。
 
# 支持
本项目为免费项目，你可以自动修改，但请保留代码官方出处声明。
### 加微信进群:
![img.png](img.png)

### 捐赠开发者:
![img_1.png](img_1.png)