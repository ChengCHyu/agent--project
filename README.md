# 马到成功考研助手

基于 LangChain 和 RAG 技术的智能考研辅导 AI Agent，具备自主思考与工具调用能力，为考研学子提供专业的备考指导。

## 项目简介

本项目是一个面向考研学生的智能助手系统，采用 ReAct（Reasoning + Acting）架构，能够：
- 自主分析用户需求，判断信息充分性
- 智能调用工具获取缺失信息
- 基于 RAG 技术检索考研专业知识
- 生成个性化的备考报告和建议

## 核心特性

### 1. ReAct 智能推理
- **思考（Reasoning）**：分析用户需求，判断当前信息是否足够
- **行动（Acting）**：调用合适工具获取缺失信息
- **观察（Observing）**：接收工具返回结果
- **再思考**：评估信息充分性，决定回答或继续调用

### 2. 丰富的工具集

| 工具名称 | 功能描述 | 使用场景 |
|---------|---------|---------|
| `rag_summarize` | RAG检索工具 | 从知识库检索考研专业资料 |
| `get_weather` | 天气查询 | 获取指定城市天气信息 |
| `get_user_location` | 位置获取 | 获取用户所在城市 |
| `get_user_id` | 用户ID获取 | 获取当前用户标识 |
| `get_current_month` | 月份获取 | 获取当前月份 |
| `fetch_external_data` | 历史记录查询 | 获取用户历史查询记录 |
| `fill_context_for_report` | 报告上下文 | 触发报告生成场景 |

### 3. RAG 知识检索
- 基于 Chroma 向量数据库
- 支持考研政策、复习方法、院校信息等资料检索
- 智能摘要和知识整合

### 4. 个性化报告生成
- 用户历史记录分析
- 个性化备考建议
- 多维度数据可视化

## 项目结构

```
agentproject/
├── agent/                      # Agent 核心模块
│   ├── react_agent.py         # ReAct Agent 实现
│   └── tools/                 # 工具模块
│       ├── agent_tools.py     # 工具定义
│       └── middleware.py      # 中间件（监控、日志、提示词切换）
├── rag/                       # RAG 模块
│   ├── rag_service.py         # RAG 服务
│   └── vector_store.py        # 向量存储
├── model/                     # 模型模块
│   └── factory.py             # 模型工厂
├── utils/                     # 工具类
│   ├── config_handler.py      # 配置处理
│   ├── file_handler.py        # 文件处理
│   ├── logger_handler.py      # 日志处理
│   ├── path_tool.py           # 路径工具
│   └── prompt_loader.py       # 提示词加载
├── prompts/                   # 提示词模板
│   ├── main_prompt.txt        # 主提示词
│   ├── rag_summarize_prompt.txt # RAG摘要提示词
│   └── report_prompt.txt      # 报告生成提示词
├── config/                    # 配置文件
│   ├── agent.yml              # Agent配置
│   ├── chroma.yml             # Chroma配置
│   ├── prompts.yml            # 提示词配置
│   └── rag.yml                # RAG配置
├── data/                      # 数据目录
│   ├── external/              # 外部数据
│   │   └── user_queries.json  # 用户查询记录
│   └── rag测试资料*.txt       # RAG测试资料
├── chroma_db/                 # Chroma向量数据库
├── log/                       # 日志目录
├── app.py                     # Streamlit Web应用
└── README.md                  # 项目说明
```

## 快速开始

### 环境要求

- Python 3.10+
- 依赖包：见 requirements.txt

### 安装依赖

```bash
pip install -r requirements.txt
```

### 配置

1. 修改 `config/` 目录下的配置文件：
   - `agent.yml`：配置外部数据路径
   - `chroma.yml`：配置向量数据库参数
   - `rag.yml`：配置 RAG 服务参数

2. 准备 RAG 知识库：
   - 将考研相关资料放入 `data/` 目录
   - 运行向量存储初始化脚本

### 运行方式

#### 方式1：命令行运行

```bash
python -m agent.react_agent
```

#### 方式2：Web 界面

```bash
streamlit run app.py
```

## 使用示例

### 示例1：查询考研政策

```
用户：2025年考研报名时间是什么时候？
AI：【思考】用户询问考研报名时间，需要检索最新政策信息
    【行动】调用 rag_summarize(query="2025考研报名时间")
    【观察】获取到报名时间安排
    【回答】2025年考研报名时间为...
```

### 示例2：生成个人报告

```
用户：查看我的使用记录
AI：【思考】用户需要查看个人使用记录，需要获取用户ID
    【行动1】调用 get_user_id()
    【观察】获取到用户ID：U001
    【行动2】调用 fill_context_for_report()
    【观察】上下文已注入
    【行动3】调用 fetch_external_data(user_id="U001")
    【观察】获取到历史查询记录
    【回答】生成个人使用报告...
```

### 示例3：天气查询

```
用户：北京今天天气怎么样？
AI：【思考】用户询问天气，需要获取北京天气
    【行动】调用 get_weather(city="北京")
    【观察】获取到天气信息
    【回答】北京今天天气晴朗，气温26℃...
```

## 核心流程

```
用户提问
    ↓
[思考] 分析需求，判断信息是否足够
    ↓
信息足够？ → 是 → 生成回答
    ↓ 否
[行动] 调用工具获取信息
    ↓
[观察] 接收工具返回
    ↓
[再思考] 信息是否足够？
    ↓ 否（循环，最多5次）
生成最终回答
```

## 工具调用规则

### 个人使用报告生成流程

当用户明确需求为生成/查询个人使用报告时，**严格遵循**以下调用顺序：

1. **get_user_id()** → 获取用户ID
2. **fill_context_for_report()** → 注入报告上下文
3. **fetch_external_data(user_id)** → 获取历史记录

### 工具调用限制

- 最多 **5次** 工具调用
- 超过5次仍无法回答，回复「我不知道」
- 入参必须与工具定义完全一致

## 配置说明

### agent.yml

```yaml
external_data_path: data/external/user_queries.json
```

### rag.yml

```yaml
vector_store_path: chroma_db
embedding_model: text-embedding-3-small
chunk_size: 500
chunk_overlap: 50
```

## 开发计划

- [ ] 支持更多考研数据源接入
- [ ] 实现用户登录和持久化会话
- [ ] 添加更多专业工具（院校排名查询、分数线预测等）
- [ ] 优化 RAG 检索准确率
- [ ] 支持多轮对话上下文理解

## 技术栈

- **LangChain**：Agent 框架和工具链
- **LangGraph**：工作流编排
- **ChromaDB**：向量数据库存储
- **OpenAI API**：大语言模型
- **Streamlit**：Web 界面
- **YAML**：配置文件管理

## 贡献指南

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License

## 联系方式

如有问题或建议，欢迎联系项目维护者。

---

**祝各位考研学子马到成功！** 🎓
