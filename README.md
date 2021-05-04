渲染完成后自动发送到钉钉机器人进行通知

# 安装
- 请将 Dingding_notification.py 拷贝至达芬奇指定的脚本存放目录下
- macOS: /Users/{你的用户名}/Library/Application Support/Blackmagic Design/DaVinci Resolve/Fusion/Scripts/Deliver
- Windows: C:\Users{你的用户名}\AppData\Roaming\Blackmagic Design\DaVinci Resolve\Support\Fusion\Scripts\Deliver
- 请使用v17及以上版本
- 在渲染设置中即可找到
- 仅支持在达芬奇内使用，不支持在外部运行

# 用法
- 新建渲染任务时，勾选上 Trigger script at 【End】 of render job之后，选择该脚本即可，并会在渲染任务完成后自动执行


# 需要
- Python 3.6 64-bit
- 第三方库：requests
- 其他版本的 Python 达芬奇并不支持
