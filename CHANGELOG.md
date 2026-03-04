# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.1] - 2026-03-04

### Added
- 新增 `/tk` 指令，支持调用退款API
- 添加 `requirements.txt` 文件，声明 `aiohttp` 依赖

### Changed
- 更新插件版本至 1.0.1
- 修复 `/dd` 指令的响应消息格式

### Implementation Details
- `/tk` 指令支持格式：`/tk 单号 金额 原因`（示例：`/tk 0077 20元 车辆故障`）
- 解析用户输入，提取订单号、金额和原因
- 调用 API 端点 `https://cloud.moshisoft.cn/j2ee/merctx/openapi/robotic/dd`
- 返回 API 响应中的 `message` 字段给用户
- 包含完整的错误处理（格式校验、网络错误、API错误等）

## [1.0.0] - 2026-03-04

### Added
- 初始版本发布
- 实现 `/dd` 指令基础功能