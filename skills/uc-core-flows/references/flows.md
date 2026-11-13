# UC 核心流程 · 详细资料

## 1. 下单流程（OrderService.createOrder）

1. 查商品，算金额 `price × quantity`
2. **预扣库存**：`InventoryService.tryDeduct` —— available 减、frozen 加
3. 创建订单，状态 `PENDING_PAYMENT`
4. 投递**延迟关单任务**：`delayQueue.schedule(..., timeoutMinutes * 60 * 1000)`

要点：步骤 2-3 在同一个事务里，预扣失败则订单不创建。

## 2. 支付流程（PaymentService.handlePayCallback）

1. **幂等检查**：`existsByPayNo(payNo)` 为 true 直接返回
2. 查订单，校验状态必须是 `PENDING_PAYMENT`
3. 记录支付（SUCCESS）
4. **确认扣库存**：`InventoryService.confirmDeduct` —— frozen 减
5. 订单状态 → `PAID`

要点：幂等检查必须**最先**做，否则重复回调会在状态校验处报错或造成重复扣减。

## 3. 退款流程（RefundService.refund）

1. **幂等检查**：`existsByRefundNo(refundNo)` 为 true 直接返回
2. 查订单，校验状态必须是 `PAID`
3. 记录退款（SUCCESS）
4. **回补库存**：`InventoryService.restore` —— available 加
5. 订单状态 → `REFUNDED`

## 4. 超时关单流程（OrderTimeoutHandler.handleTimeout）

1. 延迟任务触发（模拟 RocketMQ 延迟消息）
2. 查订单，若状态仍是 `PENDING_PAYMENT`：
   - 订单状态 → `CANCELLED`
   - **释放库存**：`InventoryService.releaseDeduct` —— frozen 减、available 加
3. 其他状态（已支付/已取消/已退款）不处理
