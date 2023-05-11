# 通用QQ机器人

## 项目说明

本项目旨在建立一个通用的QQ机器人，方便各群群主对群聊进行管理。

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
- [ ] 签到
- [ ] 积分兑换礼品
  - [ ] 调用配置好的 API 发放奖励
  - [ ] 给予群中的某项权限作为奖励
  - [ ] 购买入群邀请码
- [ ] 加群自动审批
  - [x] 根据邀请码判断能否入群
  - [ ] 根据邀请人判断能否入群（Yiri Mirai 在 pypi 上的版本暂不支持该功能，请使用 Github 上的 master 分支）
- [ ] 基于 ChatGPT 的自动面试（针对需要一定知识的游戏交流群和其他需要面试的场景）

## 使用

参见我们的 [Wiki](https://github.com/XYCode-Kerman/GeneralQBOT/wiki)。

## 参与开发![Star History Chart](https://api.star-history.com/svg?repos=XYCode-Kerman/GeneralQBOT&type=Timeline)

(WIP)

### 注意事项

所有向main的提交都应该是Pull Requests！不要强制推送！！！