---
name: uc-dev-guidelines
description: "UC 系统的开发规范与约定：库存操作必须走 InventoryService、支付/退款必须幂等（唯一单号）、注意事务边界（自调用失效）、异常统一用 BusinessException。写任何 UC 相关代码前先读。"
---

# UC 开发规范（SOP）

## 五条硬性规范

1. **库存永远走 InventoryService**——禁止直接改 `Product` 库存字段。
2. **支付/退款必须幂等**——唯一单号，检查放第一步。
3. **事务**——改库存 + 改订单同一事务；需要独立事务的方法拆独立 bean（避免自调用失效）。
4. **异常统一抛 `BusinessException`**——由 `GlobalExceptionHandler` 转 HTTP 400。
5. **新接口**——`@RestController` + record 请求体，返回实体，错误走异常。

## 细节

完整规范 + 命名约定见 `references/guidelines.md`。
