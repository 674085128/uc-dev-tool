# UC-dev-tool

一个帮助 AI（Claude）辅助开发 **UC 电商订单系统** 的 skill 包。

## 这是什么

这里有两样东西，别混淆：

1. **UC 电商订单系统**（`uc-ecommerce`）—— 一个 Spring Boot 电商 demo，是本工具"记录的对象"，代码在[另一个仓库/目录](https://github.com/)里。
2. **UC-dev-tool**（本仓库）—— 一组 skill，把 UC 系统的架构、业务知识、开发规范和踩坑经验沉淀下来，让 Claude 在辅助开发 UC 时能"读懂"这个系统、少犯错。

## 为什么需要它

Claude 开发 UC 时，如果不了解这个系统的约定，会犯这些错：库存扣减逻辑写错、支付回调不做幂等导致重复扣款、状态机流转搞错、直接操作 Product 表绕过 InventoryService…… 这些坑在 `uc-common-pitfalls` 里都有记录。

## 安装

把这 5 个 skill 目录复制到 Claude 的 skills 目录即可。每个 skill 就是一个文件夹，里面一个 `SKILL.md`。

## 自更新

`update.py` 脚本会对比本地 `VERSION` 和 GitHub 远程 `VERSION`，发现新版就自动 `git pull` 更新：

```bash
python update.py
```

原理就是"每次对话检查最新版本自动更新"的三步：读版本号 → 对比 → 拉取。注意：Claude 宿主没有"每次对话自动跑脚本"的钩子，所以需要你定期手动运行一次（或加进定时任务）。

## 包含的 skill

| skill | 作用 | 何时触发 |
|---|---|---|
| `uc-architecture` | 系统架构总览 | 理解全貌、技术选型、定位模块 |
| `uc-domain-model` | 业务概念字典 | 理解术语、字段、状态机 |
| `uc-core-flows` | 核心业务流程 | 开发/排查下单支付库存退款 |
| `uc-dev-guidelines` | 开发规范 | 写任何 UC 代码前 |
| `uc-common-pitfalls` | 踩坑清单 | 涉及支付或库存的改动 |

## 目录结构

```
uc-dev-tool/
├── README.md
├── LICENSE
└── skills/
    ├── uc-architecture/SKILL.md
    ├── uc-domain-model/SKILL.md
    ├── uc-core-flows/SKILL.md
    ├── uc-dev-guidelines/SKILL.md
    └── uc-common-pitfalls/SKILL.md
```

## License

MIT
