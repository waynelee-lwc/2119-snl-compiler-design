# jlu-2119-compiler-design
吉林大学编译原理课程设计——SNL编译器实现

## 技术目录
### 词法分析
- 实现语言：node.js
- token命名
  - RESERVED
  - ID
  - SEPERATOR
  - ASSIGN
  - UNDERANGE
  - CHARC
  - NUMBER
  - EOF

### 语法分析
#### 语法树节点命名
- 标志节点
  - ProK
  - PheadK
  - TypeK
  - VarK
  - ProcDecK
  - StmLK
- 具体节点
  - DecK
    - ArrayK
    - CharK
    - IntegerK
    - RecordK
    - IdK
  - StmtK
    - IfK
    - WhileK
    - AssignK
    - ReadK
    - WriteK
    - CallK
    - ReturnK
  - ExpK
    - OpK
    - ConstK
    - IdEK
### 语义分析
### web服务

## 会议记录
### 3月12日
- 确定整体开发时间3.13-4.17
- 确定总体测试和报告撰写时间4.17-4.20
- 确定开发任务
  - 词法分析
    - 基础框架
    - 内容填充
  - 两种语法分析（并行开发）
    - 递归下降
    - LL(1)
  - 语义分析
  - 编译日志和错误的产生和收集
  - 展示和交互平台(前端页面)
  - 编译流程控制(后端服务)
  - 格式化程序再生成(支线任务)
- TODO
  - 熟悉C/C++语言
  - 阅读《设计与实现》的简介和词法分析部分
  - 构思词法分析框架

### 3月15日
- 重新确认开发语言
  - 词法分析 js
  - 语法分析 java | python | go
  - 语义分析待定
  - web后端服务待定
- 中间产物输出格式
  - 词法分析token序列
    - json[{"type":"typename(string)", "name":"name(string", "line":"line_num(int)" },{}...]

### 3月16日
- DONE
  - 更改git仓库权限
  - 粗读词法分析部分，掌握原理
- TODO
  - 完善脚手架，多加注释
  - 编写DFA节点，增加Token和error
  - 尝试测试一个完整的从输入到输入

### 3月17日
- 近期安排
  - @yhls  编写DFA节点 
  - @lwc 准备语法分析递归下降部分
  - @fyb 语法分析LL1
- TODO
  - 约定token类型的命名

### 3月21日
- DONE
  - 词法分析大部
- TODO
  - 测试词法分析
  - 约定语法分析输出格式
  - 开发语法分析模块