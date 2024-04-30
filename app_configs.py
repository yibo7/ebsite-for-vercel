import os

from eb_utils.xs_json import XsJson


cf_path = 'conf/setting.json'
# 检查文件是否存在
if os.path.exists(cf_path):
    CF = XsJson("conf/setting.json")
    CF_APP = CF.load()
else:
    print(f"在vercel上运行忽略setting.json请在环境变量设置配置。")
