# Contributing

感谢参与 Cognitive Gate / ORIGIN 早期参考实现。

请先创建 Issue 描述问题或提案，再提交 Pull Request。PR 应包含：

- 可复现步骤和预期行为；
- 相关测试；
- 对兼容性的影响说明；
- 不把 best-effort 审计描述成绝对安全保证。

本地验证：

```bash
python -m unittest discover -s tests -v
python -m pip install .
cognitive-gate --demo
```
