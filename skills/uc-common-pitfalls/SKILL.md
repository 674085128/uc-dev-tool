---
name: uc-common-pitfalls
description: "UC 系统开发中已知的坑：支付回调重复、并发超卖、库存两阶段状态搞混、@Transactional 自调用失效、order 表名是 SQL 保留字、H2 内存库重启数据清空。凡涉及支付或库存的改动，必须先读此 skill。"
---

# UC 踩坑清单（SOP）

## 六个已知坑（速查）

1. **支付回调重复** → 幂等（`existsByPayNo`）
2. **并发超卖** → 乐观锁（`@Version`）
3. **库存两阶段搞混** → 只用 InventoryService 四方法
4. **@Transactional 自调用失效** → 拆独立 bean
5. **order 是保留字** → `@Table(name = "orders")`
6. **H2 重启清空** → `DataInitializer` 预置

## 细节

每个坑的现象 / 解法 / 教训见 `references/pitfalls.md`。
