---
name: uc-architecture
description: "UC 电商订单系统的整体架构、技术栈与包结构。技术栈：Spring Boot 3.3.5 + Java 17 + Maven + H2；RocketMQ 用 InMemoryDelayQueue 替代、Redis 用 InMemoryCache 替代。当需要理解系统全貌、设计新功能、做技术选型，或定位某功能该放哪个包时使用。"
---

# UC 系统架构（SOP）

UC 是一个单体电商订单系统，核心链路：**下单 → 支付 → 扣库存 → 退款**。

## 四条不可违反的架构规则

1. **库存两阶段**：`Product.availableStock`（可售）+ `frozenStock`（冻结）；下单预扣、支付确认、超时释放、退款回补。
2. **防超卖靠乐观锁**：`Product.@Version`。
3. **幂等靠唯一单号**：`Payment.payNo` / `Refund.refundNo`。
4. **超时关单独立 bean**：`OrderTimeoutHandler`，避免 `@Transactional` 自调用失效。

## 新增功能的落位

- 新实体 → `domain/` + 配套 `repository/`
- 新业务逻辑 → `service/`（库存操作一律走 `InventoryService`）
- 新接口 → `web/`，异常统一抛 `BusinessException`

## 细节

完整技术栈表、包结构图、中间件替代策略、启动方式见 `references/architecture.md`。
