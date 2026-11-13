# UC 系统架构 · 详细资料

## 技术栈

| 组件 | 选择 | 说明 |
|---|---|---|
| 语言 | Java 17 | Spring Boot 3 要求 Java 17+ |
| 框架 | Spring Boot 3.3.5 | 单体应用，Maven 构建 |
| ORM | Spring Data JPA (Hibernate) | 实体用 `@Entity`，`ddl-auto: update` 自动建表 |
| 数据库 | H2 内存库 | 重启即清空，无需安装 |
| 消息队列 | `InMemoryDelayQueue` | 替代 RocketMQ，见下 |
| 缓存 | `InMemoryCache` | 替代 Redis，见下 |

## 中间件替代策略

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

## 如何跑起来

```bash
cd uc-ecommerce
mvn spring-boot:run
```

- 端口 8080，H2 控制台在 `/h2-console`。
- 启动时 `DataInitializer` 预置两个商品（iPhone 15、AirPods Pro）。
- 订单超时时间在 `application.yml` 的 `uc.order.timeout-minutes` 配置，默认 5 分钟。
