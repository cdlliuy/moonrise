# 🌐 多云部署策略 - Moonrise

## 概览

Moonrise现在支持**两个云平台**部署，各有优势，可根据需求选择：

| 平台 | Railway | Azure Container Apps |
|------|---------|---------------------|
| **难度** | ⭐ 非常简单 | ⭐⭐ 中等 |
| **免费额度** | 500小时/月 | 50-100小时/月 |
| **部署方式** | Git Push | Docker镜像 |
| **服务器位置** | 美国 | 全球（可选East Asia） |
| **中国访问延迟** | ~150ms | ~50ms（香港） |
| **冷启动** | 10-20秒 | 10-30秒 |
| **配置文件** | Procfile, railway.json | Dockerfile, azure/ |
| **推荐场景** | 全球用户 | 亚洲用户优化 |

---

## 🎯 部署方案选择

### 方案1: Railway单独部署（最简单）

**适合**:
- 第一次部署
- 全球用户访问
- 不想配置Docker

**步骤**:
1. 访问 https://railway.app/
2. GitHub登录
3. 选择moonrise仓库
4. 自动部署
5. 获取域名

**文档**: [RAILWAY_DEPLOYMENT.md](RAILWAY_DEPLOYMENT.md)

---

### 方案2: Azure单独部署（区域优化）

**适合**:
- 亚洲用户为主
- 需要低延迟
- 熟悉Azure生态

**步骤**:
```powershell
# Windows
.\azure\deploy-azure.ps1

# Linux/Mac
./azure/deploy-azure.sh
```

**文档**: [AZURE_DEPLOYMENT.md](AZURE_DEPLOYMENT.md)

---

### 方案3: 双部署（推荐）⭐

**适合**:
- 需要高可用
- 全球用户分布
- 成本控制在免费额度内

**架构**:
```
GitHub (代码)
    ↓
    ├→ Railway (美国)          → railway-domain.up.railway.app
    └→ Azure (East Asia)       → moonrise.eastasia.azurecontainerapps.io
```

**优势**:
- ✅ 两个独立部署，互为备份
- ✅ 亚洲用户访问Azure（快）
- ✅ 其他用户访问Railway（稳定）
- ✅ 两者都免费（在额度内）

**配置**:
- Railway: 已配置完成
- Azure: 运行部署脚本

---

## 📁 文件结构

### 配置文件隔离

```
moonrise/
├── Procfile              # Railway专用
├── railway.json          # Railway Scale to Zero配置
├── Dockerfile            # Azure专用
├── docker-compose.yml    # 本地Docker测试
├── .dockerignore         # Docker构建优化
├── azure/                # Azure配置目录
│   ├── deploy-azure.sh   # Linux/Mac部署脚本
│   ├── deploy-azure.ps1  # Windows部署脚本
│   └── container-app.yaml # Container App配置
├── config.py             # 通用配置
├── run.py                # 应用入口（支持两种平台）
└── app/                  # 应用代码（共享）
```

### 环境识别

应用会自动识别部署环境：

```python
# run.py
port = int(os.environ.get('PORT', 5000))
is_production = 'PORT' in os.environ
deployment = os.environ.get('DEPLOYMENT_PLATFORM', 'local')

# Railway: PORT=随机端口, DEPLOYMENT_PLATFORM未设置
# Azure: PORT=8080, DEPLOYMENT_PLATFORM=azure
# Local: PORT=5000, DEPLOYMENT_PLATFORM=local
```

---

## 🚀 部署对比

### Railway部署流程

```bash
# 1. 代码已推送到GitHub (✅ 已完成)
git push

# 2. Railway自动部署
# - 检测Procfile
# - 安装requirements.txt
# - 启动gunicorn
# - 分配域名

# 3. 完成！
# https://moonrise-production.up.railway.app
```

**时间**: 2-5分钟

### Azure部署流程

```powershell
# 1. 运行部署脚本
.\azure\deploy-azure.ps1

# 2. Azure自动执行：
# - 创建资源组
# - 创建Container Registry
# - 构建Docker镜像
# - 推送到Registry
# - 创建Container App
# - 配置Scale to Zero
# - 分配域名

# 3. 完成！
# https://moonrise.eastasia.azurecontainerapps.io
```

**时间**: 10-15分钟（首次）

---

## 💰 成本对比

### Railway

**免费额度**: 500小时/月

**Scale to Zero使用**:
```
预计: 15-76小时/月
成本: $0/月 ✅
```

### Azure Container Apps

**免费额度**:
- 50 vCPU小时/月
- 100 GB·小时内存/月

**Scale to Zero使用 (0.5 vCPU, 1GB)**:
```
预计: 15-76小时/月
vCPU消耗: 7.5-38小时
内存消耗: 15-76 GB·小时
成本: $0/月 ✅
```

### 双部署总成本

```
Railway: $0/月
Azure: $0/月
总计: $0/月 🎉
```

**关键**: 两个平台都启用Scale to Zero，按需启动

---

## 🌍 访问速度对比

### 延迟测试（中国北京）

| 部署平台 | 位置 | 延迟 | 适用地区 |
|---------|-----|------|---------|
| **Railway** | 美国 | ~150ms | 美洲、欧洲 |
| **Azure East Asia** | 香港 | ~50ms | 亚洲、大洋洲 |
| **Azure Southeast Asia** | 新加坡 | ~80ms | 东南亚 |
| **Azure Japan East** | 东京 | ~100ms | 日本、韩国 |

### 推荐策略

**全球用户**: Railway（简单）
**亚洲用户**: Azure East Asia（快速）
**双部署**: Railway + Azure（最佳）

---

## 🔄 更新部署

### Railway更新

```bash
# 修改代码
git add .
git commit -m "Update features"
git push

# Railway自动重新部署（2-3分钟）
```

### Azure更新

**方法1: 重新运行脚本**
```powershell
.\azure\deploy-azure.ps1
```

**方法2: 仅更新镜像**
```bash
# 重新构建
az acr build --registry moonriseacr --image moonrise:latest .

# 更新应用
az containerapp revision copy -n moonrise -g moonrise-rg
```

---

## 📊 监控和管理

### Railway监控

1. 访问 https://railway.app/
2. 打开moonrise项目
3. 查看：
   - Deployments（部署历史）
   - Logs（实时日志）
   - Metrics（资源使用）
   - Usage（费用统计）

### Azure监控

```bash
# 查看状态
az containerapp show -n moonrise -g moonrise-rg

# 查看日志
az containerapp logs show -n moonrise -g moonrise-rg --follow

# 查看费用
# Azure Portal → Cost Management
```

或访问 https://portal.azure.com

---

## 🎯 推荐配置

### 个人使用

```
Railway（主）
- 简单维护
- 自动部署
- 500小时免费
```

### 专业使用

```
Railway + Azure（双部署）
- Railway: 全球访问
- Azure East Asia: 亚洲优化
- 智能路由（Cloudflare）
```

### 企业使用

```
Azure Container Apps
- 完整监控
- Azure生态集成
- 自定义域名
- 专业支持
```

---

## 🚨 故障恢复

### Railway故障

**症状**: Railway无法访问

**备用**:
- 使用Azure域名访问
- 或重新部署到Railway

### Azure故障

**症状**: Azure无法访问

**备用**:
- 使用Railway域名访问
- 或重新部署到其他Azure区域

### 双部署优势

```
Railway ────┐
            ├── 其中一个故障，另一个继续服务
Azure ──────┘
```

---

## 📝 快速参考

### Railway

**部署**: 自动（Git Push）
**配置**: Procfile, railway.json
**域名**: *.up.railway.app
**文档**: [RAILWAY_DEPLOYMENT.md](RAILWAY_DEPLOYMENT.md)

### Azure

**部署**: `.\azure\deploy-azure.ps1`
**配置**: Dockerfile, azure/*
**域名**: *.azurecontainerapps.io
**文档**: [AZURE_DEPLOYMENT.md](AZURE_DEPLOYMENT.md)

---

## 🎉 现在开始

### 步骤1: Railway部署（已完成✅）

您的代码已在GitHub，Railway会自动检测并部署。

### 步骤2: Azure部署（可选）

```powershell
# Windows
cd moonrise
.\azure\deploy-azure.ps1

# 等待10-15分钟
# 获得Azure域名
```

### 步骤3: 配置智能路由（高级，可选）

使用Cloudflare设置地理路由：
- 亚洲流量 → Azure
- 其他流量 → Railway

---

## 📞 获取帮助

**Railway**:
- 文档: [RAILWAY_DEPLOYMENT.md](RAILWAY_DEPLOYMENT.md)
- 支持: https://discord.gg/railway

**Azure**:
- 文档: [AZURE_DEPLOYMENT.md](AZURE_DEPLOYMENT.md)
- 支持: https://portal.azure.com

**通用**:
- GitHub: https://github.com/cdlliuy/moonrise/issues
- 分析: [AZURE_DEPLOYMENT_ANALYSIS.md](AZURE_DEPLOYMENT_ANALYSIS.md)

---

**选择适合您的部署方式，开始月相之旅！** 🌙✨
