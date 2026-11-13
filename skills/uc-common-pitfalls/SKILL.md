---
name: uc-common-pitfalls
description: "UC 系统开发中已知的坑：支付回调重复、并发超卖、库存两阶段状态搞混、@Transactional 自调用失效、order 表名是 SQL 保留字、H2 内存库重启数据清空。凡涉及支付或库存的改动，必须先读此 skill。"
---

# UC 踩坑清单

每个坑都曾在真实开发中出现过，写涉及支付/库存的代码前先过一遍。

## 1. 支付回调重复到达

**现象**：第三方支付可能对同一笔订单回调多次，导致重复扣库存/重复改状态。
**解法**：`Payment.payNo` 唯一 + `existsByPayNo` 幂等，回调入口第一步先查，已处理直接返回。
**教训**：任何外部回调（支付、退款、消息）都必须假设"可能重复"。

## 2. 并发下单导致超卖

**现象**：两个请求同时买最后一件商品，都通过"库存足够"检查，结果库存变成负数。
**解法**：`Product.@Version` 乐观锁，并发修改同一商品时后提交的事务抛 `OptimisticLockException` 回滚。
**注意**：乐观锁检查发生在事务提交时（save 之后），不是 save 那一刻。

## 3. 库存两阶段状态搞混

**现象**：available / frozen 两个字段加错位置，比如超时关单该"frozen 减、available 加"，却只减了 frozen。
**解法**：对照 `uc-core-flows` 里的"库存操作四方法对照表"，只用 `InventoryService` 的四个方法，不手改字段。

## 4. @Transactional 自调用失效

**现象**：在 Service 内部调用自己的 `@Transactional` 方法，事务不生效（Spring 事务是 AOP 代理，this 调用绕过代理）。
**解法**：需要独立事务的方法拆到独立 bean。参考 `OrderTimeoutHandler` —— 它被延迟队列跨 bean 调用，事务才生效。
**识别信号**：改了数据却不回滚 / 事务边界和预期不符，先怀疑自调用。

## 5. order 是 SQL 保留字

**现象**：实体名 Order 默认映射到表 `order`，H2/MySQL 里 `order` 是保留字，建表或查询报错。
**解法**：`@Table(name = "orders")` 显式指定表名。

## 6. H2 内存库重启数据清空

**现象**：重启应用后商品/订单全没了。
**解法**：这是 H2 内存库的预期行为。演示数据靠 `DataInitializer` 启动时预置，生产环境换 MySQL 后此问题消失。
