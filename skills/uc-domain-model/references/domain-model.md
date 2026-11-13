# UC 业务概念 · 详细资料

## 订单状态机（OrderStatus）

```
PENDING_PAYMENT（待支付）
   ├── 支付成功 ──→ PAID（已支付）
   │                    └── 退款 ──→ REFUNDED（已退款）
   └── 超时未支付 ──→ CANCELLED（已取消）
```

- **PENDING_PAYMENT**：下单后、支付前。此时库存已**预扣**（冻结）。
- **PAID**：支付成功，库存已**实扣**（冻结转实扣）。
- **CANCELLED**：超时关单，库存已**释放**回可售。
- **REFUNDED**：退款完成，库存已**回补**。

注：枚举里还有 `REFUNDING`，但 demo 的退款是同步完成的（`RefundService.refund` 直接 PAID→REFUNDED），`REFUNDING` 目前未作为中间态使用。

## 库存两阶段模型（核心概念）

商品库存分两个字段，这是 UC 最核心的业务概念：

| 字段 | 含义 | 谁在变 |
|---|---|---|
| availableStock | 可售库存 | 下单(-)、超时释放(+)、退款回补(+) |
| frozenStock | 冻结库存（预扣未支付） | 下单(+)、支付确认(-)、超时释放(-) |

**为什么分两个字段**：如果下单直接扣 availableStock，超时取消还要记得加回来，容易漏；分成"可售/冻结"，状态一目了然，且支付成功那一刻的"确认扣减"有明确落点（frozen 减）。

## 幂等键约定

- 支付幂等键：`payNo`，`PaymentRepository.existsByPayNo` 判断是否已处理。
- 退款幂等键：`refundNo`，`RefundRepository.existsByRefundNo` 判断是否已处理。

任何涉及支付/退款的改动，必须先确认幂等键的处理逻辑。
