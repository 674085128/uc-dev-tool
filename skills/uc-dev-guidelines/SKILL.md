---
name: uc-dev-guidelines
description: "UC 系统的开发规范与约定：库存操作必须走 InventoryService、支付/退款必须幂等（唯一单号）、注意事务边界（自调用失效）、异常统一用 BusinessException。写任何 UC 相关代码前先读。"
---

# UC 开发规范

## 1. 库存：永远走 InventoryService

禁止在业务代码里直接 `product.setAvailableStock(...)` 改库存字段。所有库存变更必须通过 `InventoryService` 的四个方法（tryDeduct / confirmDeduct / releaseDeduct / restore），否则会绕过乐观锁和两阶段模型，导致库存错乱。

## 2. 支付/退款：必须幂等

- 支付回调入口必须先用 `existsByPayNo` 判断，已处理直接 return。
- 退款入口必须先用 `existsByRefundNo` 判断。
- 幂等检查要放在**第一步**，在任何状态校验之前。

## 3. 事务边界

- 涉及"改库存 + 改订单"要放在同一个 `@Transactional` 事务里。
- **坑**：类内部自调用（`this.method()`）会让 `@Transactional` 失效。需要独立事务的方法要拆到独立 bean（参考 `OrderTimeoutHandler`）。
- 乐观锁冲突（`OptimisticLockException`）会导致事务回滚，这是预期行为，不要吞掉。

## 4. 异常处理

- 业务错误统一抛 `BusinessException`（带中文 message），由 `GlobalExceptionHandler` 转成 HTTP 400。
- 不要在各处写 try-catch 返回自定义错误码，统一走全局处理。

## 5. 命名约定

- 订单号 orderNo：`ORD + 时间戳 + 随机串`（见 `OrderService.generateOrderNo`）。
- 幂等键 payNo / refundNo：由调用方传入，业务代码只负责"存在即返回"。
- 表名：`Order` 实体映射到 `orders` 表（order 是 SQL 保留字）。

## 6. 新接口

- Controller 用 `@RestController` + `@RequestMapping`，请求体用 Java record。
- 返回实体即可（demo 不做 DTO 分层），错误走异常。
