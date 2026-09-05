# Security Policy

这是早期参考实现，不应直接作为生产环境的安全边界。

请不要在公开 Issue 中提交 API key、个人数据、私钥或真实生产日志。发现可能导致约束绕过、
数据泄露或错误放行的问题，请通过 GitHub Security Advisories 私下报告；如果该入口不可用，
先创建不含敏感细节的 Issue，说明需要私下沟通。

已知边界包括：输出审计属于 best-effort；默认示例使用 MockGrok；本项目没有提供 OS 级沙箱、
硬件密钥保护或任意外部执行器的系统级强制阻断。
