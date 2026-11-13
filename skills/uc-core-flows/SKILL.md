---
name: uc-core-flows
description: "UC 下单、支付、扣库存、退款、超时关单的端到端流程。下单走「预扣库存+延迟关单」，支付走「幂等+确认扣库存」，退款走「幂等+回补库存」。当开发或排查这些主流程的功能时使用。"
---

# UC 核心流程（SOP）

四条主链路：下单、支付、退款、超时关单。

## 库存四方法对照表（改代码前必查）

| 方法 | 触发时机 | 库存变化 |
|---|---|---|
| tryDeduct | 下单 | available − , frozen + |
| confirmDeduct | 支付成功 | frozen − |
| releaseDeduct | 超时关单 | frozen − , available + |
| restore | 退款 | available + |

## 两条硬规则

1. 支付/退款入口**第一步**做幂等检查（`existsByXxxNo`），已处理直接 return。
2. 改状态前先校验当前状态（支付要求 `PENDING_PAYMENT`，退款要求 `PAID`）。

## 细节

每条链路的逐步流程见 `references/flows.md`。
