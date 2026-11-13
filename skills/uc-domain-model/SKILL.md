---
name: uc-domain-model
description: "UC 系统的核心业务概念与数据模型：订单 Order、商品 Product（availableStock+frozenStock 两阶段库存）、支付 Payment、退款 Refund，以及订单状态机（PENDING_PAYMENT→PAID→REFUNDED、PENDING_PAYMENT→CANCELLED）。当需要理解业务术语、字段含义、订单状态流转，或写涉及这些实体的代码时使用。"
---

# UC 业务概念（SOP）

## 四个核心实体

| 实体 | 表名 | 关键字段 |
|---|---|---|
| Product | product | availableStock, frozenStock, version |
| Order | orders | orderNo, status, amount |
| Payment | payment | payNo(唯一), orderNo |
| Refund | refund | refundNo(唯一), orderNo |

## 两个必须记住的约定

1. **库存两阶段**：`availableStock`（可售）+ `frozenStock`（冻结）。不要手改字段，只走 `InventoryService` 的四个方法。
2. **幂等键**：`payNo` / `refundNo` 唯一，重复回调靠 `existsByXxxNo` 挡掉。

## 细节

订单状态机全图、字段表、两阶段模型详解见 `references/domain-model.md`。
