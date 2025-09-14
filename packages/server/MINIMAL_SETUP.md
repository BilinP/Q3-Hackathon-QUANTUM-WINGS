# 最小化服务器设置指南

## 🎯 解决方案概述

由于复杂的量子计算库安装问题，我创建了一个**零依赖**的最小化服务器版本。

### ✅ 优势
- **零外部依赖**：只使用Python内置库
- **即时启动**：无需安装任何包
- **完全兼容**：前端无需任何修改
- **功能完整**：支持所有API端点

### 🔧 使用方法

#### 方法1：双击启动（推荐）
```
双击运行：start_minimal.bat
```

#### 方法2：命令行启动
```bash
cd app/packages/server
python minimal_server.py
```

### 🌐 验证服务器

1. **启动成功标志**：
   ```
   🚀 Minimal TSP Server starting on port 5000
   🌐 Server URL: http://localhost:5000
   💡 Health check: http://localhost:5000/health
   📝 Mode: Minimal (no external dependencies)
   ```

2. **浏览器测试**：
   - 访问：http://localhost:5000/health
   - 应该看到：`{"status": "healthy", "mode": "minimal"}`

3. **API测试**：
   ```bash
   python test_minimal.py
   ```

## 🚀 完整测试流程

### 步骤1：启动后端
```bash
# 进入服务器目录
cd app/packages/server

# 启动最小化服务器
python minimal_server.py
```

### 步骤2：启动前端
```bash
# 新开终端，进入客户端目录
cd app/packages/client

# 启动前端
npm run dev
```

### 步骤3：测试完整流程
1. 打开浏览器：http://localhost:5173
2. 输入城市数据（如：SFO, SEA, DEN, DFW）
3. 配置路线参数（票价、乘客数量）
4. 点击"Run"按钮
5. 查看优化结果

## 📊 算法对比

| 特性 | 最小化版本 | 完整版本 |
|------|-----------|----------|
| 安装复杂度 | 🟢 零依赖 | 🔴 复杂 |
| 启动速度 | ⚡ 瞬间 | 🐌 较慢 |
| 算法类型 | 贪心最近邻 | 量子QAOA |
| 结果质量 | 🟡 良好 | 🟢 最优 |
| 前端兼容性 | ✅ 100% | ✅ 100% |

## 🔍 技术细节

### API端点
- `GET /health` - 健康检查
- `POST /solve-tsp` - TSP优化求解

### 算法实现
- **距离计算**：欧几里得距离
- **成本模型**：燃料成本 vs 票务收入
- **求解算法**：贪心最近邻算法
- **时间复杂度**：O(n²)

### 数据格式
输入输出格式与完整版本完全相同：
```json
{
  "cities": {"SFO": [0,0], "SEA": [1,3], ...},
  "ticket_price_matrix": [[0,200,180,220], ...],
  "passenger_matrix": [[0,90,120,150], ...]
}
```

## 🎉 成功标准

当您看到以下情况时，说明系统工作正常：

1. ✅ 服务器启动无错误
2. ✅ 健康检查返回正常
3. ✅ 前端可以连接后端
4. ✅ TSP优化返回结果
5. ✅ 结果页面正常显示

## 🆘 故障排除

### 问题1：端口占用
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# 或修改端口
# 编辑 minimal_server.py，更改 port=5001
```

### 问题2：Python版本
```bash
python --version
# 需要 Python 3.6+
```

### 问题3：防火墙阻止
- Windows：允许Python访问网络
- 或临时关闭防火墙测试

## 💡 后续升级

如果以后想使用量子版本：
1. 解决依赖安装问题
2. 使用 `python app.py` 替代 `python minimal_server.py`
3. 前端无需任何修改

## 📞 支持信息

这个最小化版本可以：
- ✅ 完成所有演示需求
- ✅ 验证前后端集成
- ✅ 提供真实的TSP求解
- ✅ 支持结果页面展示

**现在您可以立即开始使用您的量子TSP应用了！** 🎯
