---
name: uc-architecture
description: "UC 电商订单系统的整体架构、技术栈与包结构。技术栈：Spring Boot 3.3.5 + Java 17 + Maven + H2 内存数据库；RocketMQ 用 InMemoryDelayQueue 替代、Redis 用 InMemoryCache 替代（代码已留接口）。包结构：domain / repository / service / web / mq / cache / config / exception。当需要理解系统全貌、设计新功能、做技术选型、新增依赖，或定位某个功能该放在哪个包时使用。"
---

# UC 电商订单系统 · 架构总览

UC 是一个单体（monolith）电商订单系统，核心是**下单 → 支付 → 扣库存 → 退款**四条主链路。demo 的目标是把这四条链路跑通，并示范电商系统的几个经典设计：幂等、防超卖、超时关单。

## 技术栈

| 组件 | 选择 | 说明 |
|---|---|---|
| 语言 | Java 17 | Spring Boot 3 要求 Java 17+ |
| 框架 | Spring Boot 3.3.5 | 单体应用，Maven 构建 |
| ORM | Spring Data JPA (Hibernate) | 实体用 `@Entity`，`ddl-auto: update` 自动建表 |
| 数据库 | H2 内存库 | 重启即清空，无需安装 |
| 消息队列 | `InMemoryDelayQueue` | 替代 RocketMQ，见下 |
| 缓存 | `InMemoryCache` | 替代 Redis，见下 |

## 中间件替代策略（重要）

demo 不依赖真实 RocketMQ / Redis，用内存实现替代，但**接口语义对齐**，方便日后替换成真实中间件：

- **`InMemoryDelayQueue`**（`com.uc.ecommerce.mq`）替代 RocketMQ 延迟消息，用于超时关单。方法 `schedule(Runnable task, long delayMillis)`。
- **`InMemoryCache`**（`com.uc.ecommerce.cache`）替代 Redis。demo 里业务正确性靠数据库乐观锁 + 唯一约束保证，缓存不强制参与，仅作占位。

生产环境替换时：延迟关单用 RocketMQ 延迟消息；幂等/分布式锁/库存缓存用 Redis。

## 包结构

```
com.uc.ecommerce
├── domain/       实体 + 枚举（Product, Order, Payment, Refund, OrderStatus）
├── repository/   JPA 数据访问接口
├── service/      业务逻辑（OrderService, InventoryService, PaymentService, RefundService, OrderTimeoutHandler）
├── web/          REST 控制器（OrderController, PaymentController, RefundController, GlobalExceptionHandler）
├── mq/           消息队列抽象（InMemoryDelayQueue）
├── cache/        缓存抽象（InMemoryCache）
├── config/       启动配置（DataInitializer 预置商品）
└── exception/    业务异常（BusinessException）
```

## 核心设计决策（写代码前必读）

1. **库存两阶段模型**：`Product.availableStock`（可售）+ `frozenStock`（冻结）。下单预扣、支付确认、超时释放、退款回补——见 `uc-domain-model` 和 `uc-core-flows`。
2. **防超卖用乐观锁**：`Product` 有 `@Version` 字段，并发扣库存靠它兜底。
3. **幂等靠唯一单号**：`Payment.payNo`、`Refund.refundNo` 唯一，重复回调靠 `existsByXxxNo` 挡掉。
4. **超时关单独立 bean**：`OrderTimeoutHandler` 独立出来，避免 `@Transactional` 自调用失效（详见 `uc-common-pitfalls`）。

## 如何跑起来

```bash
cd uc-ecommerce
mvn spring-boot:run
```

- 端口 8080，H2 控制台在 `/h2-console`（JDBC URL 见 `application.yml`）。
- 启动时 `DataInitializer` 预置两个商品（iPhone 15、AirPods Pro）。
- 订单超时时间在 `application.yml` 的 `uc.order.timeout-minutes` 配置，默认 5 分钟。

## 新增功能的落位原则

- 新实体 → `domain/`，配套 `repository/`。
- 新业务逻辑 → `service/`，库存操作一律走 `InventoryService`（不要直接改 Product）。
- 新接口 → `web/`，异常统一抛 `BusinessException`，由 `GlobalExceptionHandler` 转成响应。
