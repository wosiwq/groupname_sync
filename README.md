# 目录

- [开始](#开始)
  - [下载](#下载)
  - [安装](#安装)
  - [使用](#使用)
- [注意](#注意)
- [TODO](#TODO)

# 开始

## 下载

直接下载或clone本项目

## 安装

1. 将``groupname_sync``文件夹放入``hoshino``的``modules``文件夹
2. 复制``groupname_sync.example``到``config``文件夹，重命名为``groupname_sync.py``，打开后按照注释进行配置
3. 修改``_bot_.py``，在``MODULES_ON``中添加``clanbattlereport``
4. 重启HoshinoBot


## 使用

本项目目前还非常粗糙~~（因为我摸鱼）~~，所以有且仅有两条命令

1. 初始化群名
2. 修改群名 ***

在**启用**了 `群昵称同步` 服务后，使用 **初始化群名** 命令，将原来的群名录入内存，即可开始自动同步yobot中的进度，效果大致如下

> K.A.会战群
> K.A.会战群28-4

在使用 **修改群名** 命令后会自动停止同步。

# 注意

因为未实现本地储存，所有数据均存于内存内，重启BOT就会失效，另，此服务开启与关闭的权限设置为仅SUPERUSER可更改，且默认不启用，若想修改，请删除或更改 `groupname_sync.py` 第八行的 `manage_priv` 与 `enable_on_default` 。

# TODO

- [ ] json存储群名等信息