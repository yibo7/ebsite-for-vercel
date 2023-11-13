
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

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fyibo7%2Febsite-for-vercel.git&env=SITE_KEY&envDescription=SITE_KEY%E6%98%AF%E7%BD%91%E7%AB%99%E5%AF%86%E9%92%A5%EF%BC%8C%E8%B6%8A%E5%A4%8D%E6%9D%82%E8%B6%8A%E5%AE%89%E5%85%A8&envLink=https%3A%2F%2Fgithub.com%2Fyibo7%2Fxs_proxy_api&project-name=ebsite-for-vercel&repository-name=ebsite-for-vercel)

# 更新项目
提交项目后会自动更新

注：
>如果修改了requirements.txt，提交后也一样会自动更新，不需要重新部署。