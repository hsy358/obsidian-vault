"""德勤 AI Native —— Autoloop 风格调度内核（原型 v0.1）

设计目标：只做四件事 —— 收事件、按规则分活、派给 Agent、记每一步。
不碰 Agent 内部、不做模型决策、不做人类学治理。

内核基线（8 条不可砍，逐条可自动验收，见 tests/test_kernel.py）：
  1. 唯一写入点 + 单事务
  2. 授权不可变 + 规则版本化
  3. 指令数据分离 + 事件字段白名单
  4. 跳数熔断（MAX_HOPS）
  5. 事件溯源 + 一条命令查清来龙去脉
  6. 核心零出站网络
  7. 厂商中立接口
  8. 首投 observe 灰度
"""

__all__ = ["MAX_HOPS", "__version__"]

__version__ = "0.1.0"

#: 单轮事件链最大层数，超过即熔断（借鉴 Agent Autoloop decide.ts 的 MAX_HOPS = 8）
MAX_HOPS = 8
