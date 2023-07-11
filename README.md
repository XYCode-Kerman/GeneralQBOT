# 通用QQ机器人

On master: ![](https://img.shields.io/codecov/c/gh/XYCode-Kerman/GeneralQBOT?token=8ZA3QCOXRY&style=for-the-badge)  On develop![](https://img.shields.io/codecov/c/gh/XYCode-Kerman/GeneralQBOT/develop?token=8ZA3QCOXRY&style=for-the-badge)

![](https://img.shields.io/github/license/XYCode-Kerman/GeneralQBOT?style=for-the-badge) ![](https://img.shields.io/github/repo-size/XYCode-Kerman/GeneralQBOT?style=for-the-badge) ![](https://img.shields.io/static/v1?label=Python&message=3.8&style=for-the-badge&color=blue)

## 说明

本项目旨在建立一个通用的QQ机器人，方便各群群主对群聊进行管理。

> ⚠警告：**本项目处于不完善状态！由于开发者只有 XYCode-Kerman 一人，而且忙于学业，没有太多的时间用于为本项目找🐛（bug）和增强鲁棒性，请时刻关注其的运行情况并<span style="color: red;">严格按照 Wiki 进行配置！</span>(~~尽管Wiki中的某些内容是过时的，但并无太大区别~~)**。
>
> 当你发现一个Bug时，你应该通过Issue向开发者报告，或者在**config.py**中找到开发者的QQ号进行询问。如果需要自行修复，请参见[For Developers][#for-developers]章节！
>
> requirements.txt和pip是被本项目弃用的包管理器，本项目正在使用**poetry**作为包管理器。

内置多种功能，包括但不限于**游戏**、**自动面试**、**购买邀请码入群**，**积分系统**等。详情请见 [功能](#功能) 章节。

## 架构

![](./docs/架构图.svg)

本项目底层依赖于 **mirai** 和 **mirai-console-loader** 项目，是他们的开发者提供了和QQ交互的接口。在此之上，mirai-api-http 向外暴露了接口，使得 **General QBOT** 可以以其他语言和 **mirai** 进行交互，而不是使用Java。

**Yiri Mirai** 负责和 **mirai-api-http** 进行交互，使得我可以更方便的在 Python 中调用 mirai 的接口。

> 小声哔哔：本人也是 **Yiri Mirai** 的维护者之一

## 功能

### 预计2023年6月前完成


- [x] 文本审查
  - [x] 腾讯云
  - [ ] 阿里云（本人没有阿里云账号）
  - [ ] 本地关键词
  - [ ] 本地AI
- [x] 一言
- [x] 随机图片
- [x] 反刷屏
- [x] 数学计算
- [x] 聊天记录保存
- [ ] 智能热群
- [ ] ~~ChatGPT~~（请使用 **QChatGPT** 项目，该项目与本项目均采用 **Yiri Mirai** 作为框架，维护更方便，并且更加稳定）
- [ ] 画图
  - [ ] Anything（二次元图片专用）
    - [ ] 基于百度 Aistudio 的 API 调用
    - [ ] 本地运行（没钱买显存 > 16g 的显卡，欢迎有能力的开发者参与维护）
  - [ ] ~~DALL E~~ （请使用 **QChatGPT** 项目，该项目与本项目均采用 **Yiri Mirai** 作为框架，维护更方便，并且更加稳定）
- [x] 签到
- [ ] 积分兑换礼品
  - [ ] 调用配置好的 API 发放奖励
  - [ ] 给予群中的某项权限作为奖励
  - [ ] 购买入群邀请码
- [x] 加群自动审批
  - [x] 根据邀请码判断能否入群
  - [ ] 根据邀请人判断能否入群（Yiri Mirai 在 pypi 上的版本暂不支持该功能，请使用 Github 上的 master 分支）
- [x] 基于 ChatGPT 的自动面试（针对需要一定知识的游戏交流群和其他需要面试的场景）
- [x] 虚拟女友/男友

## 使用

## For Users

### 你需要的

1. 一颗聪明的脑袋（~~大头儿子~~）
2. 一种调用OpenAI Api的方式（当你启用GPT相关功能时）（~~现在好像没有彻底不使用OpenAI API的设置欸，建议自己改代码~~）
   1. 官方API服务（也许会拥有更多功能，但是收费）
   2. 自建API服务（功能等同于网页版，但是免费）
      1. [将网页版ChatGPT用作OpenAI Api](https://github.com/acheong08/ChatGPT-to-API)，支持绕过Cloudflare防护
   3. 梯子自备
3. 愿意承受一定的风险（~~指一觉醒来，房子归**OpenAI**了~~）
4. 至少有初中生的英语水平（Google Translate 欢迎您）
5. 一定的计算机知识
6. 一颗愿意折腾的心
7. 一台可以长期保证开机的电脑，用于挂QQ机器人

### 安装

```bash
git clone https://github.com/XYCode-Kerman/GeneralQBOT.git  # 克隆本仓库
```

~~~bash
# 如果你希望使用开发版
git clone -b develop https://github.com/XYCode-Kerman/GeneralQBOT.git
~~~

````bash
# 更新版本
git checkout origin/master  # 正式版
git checkout origin/develop # 开发版
````
````bash
# 安装依赖
pip install poetry
poetry install
````

> 我们欢迎您向我们提起**Issue**，以**解决Bug**或者**新增功能**。

如果可能，请尽量使用[Releases](https://github.com/XYCode-Kerman/GeneralQBOT/releases)版本。

### 配置

本项目的配置项存放在两处，`configs/config.py`和`.env`。

|        文件         |            内容            |
| :-----------------: | :------------------------: |
| `configs/config.py` |          常规配置          |
|       `.env`        | 机密配置（例如 Api key等） |



## For Developers

|  分支名称   |                             内容                             |
| :---------: | :----------------------------------------------------------: |
|   master    |               主分支，为稳定版本的GeneralQBOT                |
|   develop   |                           开发版本                           |
| feature_xxx | 某个功能的单独分支，最终合并到develop分支，再由develop分支合并到master |
|   hotfix    |          大部分增强代码的鲁棒性、修复项目bug的提交           |
| code_styles |  关于代码风格的提交（不涉及功能开发、bug修复、鲁棒性提升）   |
|   myself    | 你可以在这个分支中新增你自己需要的功能，但是千万**<span style="color: red">不要</span> 把这个分支推送到主仓库中（Fork的仓库除外）** |

### To Be a Developer

请在`configs/config.py`中的ADMIN_QQ找到XYCode-Kerman的QQ号，并且加为好友。

> 记得备注**来自 Github GeneralQBOT 项目**

你应该对Python有一定了解，所以开发者会让**General QBOT**去面试你。

### 其他的

参见我们的 [Wiki](https://github.com/XYCode-Kerman/GeneralQBOT/wiki)（请注意其最后编辑时间，部分内容可能已经过时）。

## 开发情况
[![Star History Chart](https://api.star-history.com/svg?repos=XYCode-Kerman/GeneralQBOT&type=Date)](https://star-history.com/#XYCode-Kerman/GeneralQBOT&Date)

(WIP)

### 注意事项

所有向main的提交都应该是Pull Requests！不要强制推送！！！

### 许可证

本项目遵循 **AGPL-3.0** 许可证。

> 请注意！AGPL-3.0 许可证是一个**传染性**许可证，如果您使用了本项目并修改了它的代码（**部署本项目不认为是修改源代码**），您必须**公开**您修改后的源代码。

AGPL-3.0许可证允许人们做以下事情：

1. 使用：您可以自由地使用AGPL-3.0许可证下的软件，无论是个人使用还是商业使用。
2. 修改：您可以对软件进行修改和定制，以满足您的特定需求。
3. 分发：您可以将软件分发给他人，无论是以二进制形式还是源代码形式。
4. 共享：您必须共享任何使用AGPL-3.0许可证软件的修改或派生作品的源代码，以便其他人可以自由访问、修改和分发这些变更。
5. 扩展：您可以使用AGPL-3.0许可证的软件作为基础，构建和发布自己的应用程序或服务。

AGPL-3.0许可证不允许人们做以下事情：

1. 专利授权限制：AGPL-3.0许可证禁止将该软件的使用与任何专利许可或授权相关联，以保护软件的自由性。
2. 版权声明修改：您不能修改或移除AGPL-3.0许可证的版权声明和许可证条款。
3. 私有化：如果您使用AGPL-3.0许可证的软件来构建一个网络服务或应用程序，您不能将其私有化，而是必须在用户访问时提供源代码，并使其可自由使用、修改和分发。
