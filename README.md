# UC-dev-tool

辅助开发 **UC 电商订单系统** 的 Claude 插件。

## 这是什么

这里有两样东西，别混淆：

1. **UC 电商订单系统**（`uc-ecommerce`）—— 一个 Spring Boot 电商 demo，是本插件的"服务对象"。
2. **UC-dev-tool**（本仓库）—— 一个 Claude 插件，把 UC 系统的架构、业务、规范和踩坑沉淀成 skill，让 AI 在开发 UC 时能自动加载、少犯错。

## 为什么需要它

Claude 开发 UC 时，如果不了解这个系统的约定，会犯这些错：库存扣减逻辑写错、支付回调不做幂等导致重复扣款、状态机流转搞错、直接操作 Product 表绕过 InventoryService…… 这些坑在 `uc-common-pitfalls` 里都有记录。

## 插件结构

这是一个 Claude plugin：

```
uc-dev-tool/
├── .claude-plugin/
│   └── plugin.json              # 插件清单（名字/版本/描述）
├── skills/
│   ├── uc-architecture/         # 系统架构
│   │   ├── SKILL.md             # 薄 SOP + 关键规则
│   │   └── references/architecture.md  # 厚细节（用到才读）
│   ├── uc-domain-model/         # 业务概念
│   │   ├── SKILL.md
│   │   └── references/domain-model.md
│   ├── uc-core-flows/           # 核心流程
│   │   ├── SKILL.md
│   │   └── references/flows.md
│   ├── uc-dev-guidelines/       # 开发规范
│   │   ├── SKILL.md
│   │   └── references/guidelines.md
│   └── uc-common-pitfalls/      # 踩坑清单
│       ├── SKILL.md
│       └── references/pitfalls.md
├── VERSION                      # 版本号
├── update.py                    # 自更新脚本
├── README.md
└── LICENSE
```

## skill 分层设计

每个 skill 的 `SKILL.md` 只放 SOP（触发描述 + 关键规则 + 指向），细节资料放 `references/`，AI 用到才读，省 token。

## 安装

把本仓库作为 plugin 安装到 Claude。装完后，开发 UC 相关功能时，AI 会自动触发对应 skill（靠 description 匹配，不用敲命令）。

## 自更新

`update.py` 对比本地 `VERSION` 和 GitHub 远程 `VERSION`，发现新版就自动 `git pull` 更新：

```bash
python update.py
```

原理是"每次对话检查最新版本自动更新"的三步：读版本号 → 对比 → 拉取。注意：Claude 宿主没有"每次对话自动跑脚本"的钩子，需要你定期手动运行。

## License

MIT
