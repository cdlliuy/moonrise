# Azure Container Apps部署完整指南

## 📋 目录
1. [前置要求](#前置要求)
2. [快速部署](#快速部署)
3. [详细步骤](#详细步骤)
4. [配置说明](#配置说明)
5. [成本分析](#成本分析)
6. [故障排查](#故障排查)
7. [多云对比](#多云对比)

---

## 前置要求

### 1. Azure账号
- 访问 https://azure.microsoft.com/free/
- 注册免费账号（需要信用卡，但不会扣费）
- 获得$200免费额度（30天）+ 永久免费服务

### 2. 安装Azure CLI

**Windows (PowerShell)**:
```powershell
# 使用winget
winget install Microsoft.AzureCLI

# 或下载安装包
# https://aka.ms/installazurecliwindows
```

**macOS**:
```bash
brew install azure-cli
```

**Linux**:
```bash
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
```

### 3. 安装Docker（可选，用于本地测试）

**Windows**:
- 下载Docker Desktop: https://www.docker.com/products/docker-desktop/

**macOS/Linux**:
```bash
# macOS
brew install docker

# Linux
sudo apt-get install docker.io
```

---

## 🚀 快速部署

### 方法1: 一键部署脚本（推荐）

**Windows PowerShell**:
```powershell
cd path\to\moonrise
.\azure\deploy-azure.ps1
```

**Linux/macOS**:
```bash
cd /path/to/moonrise
chmod +x azure/deploy-azure.sh
./azure/deploy-azure.sh
```

**等待时间**: 10-15分钟

**完成后**:
- 自动创建所有Azure资源
- 构建并推送Docker镜像
- 部署Container App
- 输出应用URL

### 方法2: 手动部署

见下方[详细步骤](#详细步骤)

---

## 详细步骤

### 步骤1: 登录Azure

```bash
az login
```

浏览器会打开，登录您的Azure账号。

### 步骤2: 设置配置变量

```bash
# 配置参数
RESOURCE_GROUP="moonrise-rg"
LOCATION="eastasia"  # 香港，亚洲用户最佳
ENVIRONMENT="moonrise-env"
APP_NAME="moonrise"
ACR_NAME="moonriseacr"  # 需要全局唯一，如果冲突请修改
```

### 步骤3: 创建资源组

```bash
az group create \
  --name $RESOURCE_GROUP \
  --location $LOCATION
```

### 步骤4: 创建Container Registry

```bash
az acr create \
  --name $ACR_NAME \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION \
  --sku Basic \
  --admin-enabled true
```

### 步骤5: 构建Docker镜像

```bash
# Azure自动构建（推荐）
az acr build \
  --registry $ACR_NAME \
  --image moonrise:latest \
  --file Dockerfile \
  .
```

或本地构建：
```bash
# 本地构建
docker build -t moonrise:latest .

# 登录ACR
az acr login --name $ACR_NAME

# 标记镜像
ACR_SERVER=$(az acr show --name $ACR_NAME --query loginServer -o tsv)
docker tag moonrise:latest $ACR_SERVER/moonrise:latest

# 推送镜像
docker push $ACR_SERVER/moonrise:latest
```

### 步骤6: 创建Container Apps环境

```bash
az containerapp env create \
  --name $ENVIRONMENT \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION
```

### 步骤7: 获取ACR凭据

```bash
ACR_SERVER=$(az acr show --name $ACR_NAME --query loginServer -o tsv)
ACR_USERNAME=$(az acr credential show --name $ACR_NAME --query username -o tsv)
ACR_PASSWORD=$(az acr credential show --name $ACR_NAME --query passwords[0].value -o tsv)
```

### 步骤8: 部署Container App

```bash
az containerapp create \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --environment $ENVIRONMENT \
  --image $ACR_SERVER/moonrise:latest \
  --registry-server $ACR_SERVER \
  --registry-username $ACR_USERNAME \
  --registry-password $ACR_PASSWORD \
  --target-port 8080 \
  --ingress external \
  --cpu 0.5 \
  --memory 1Gi \
  --min-replicas 0 \
  --max-replicas 3 \
  --env-vars DEPLOYMENT_PLATFORM=azure PORT=8080
```

### 步骤9: 获取应用URL

```bash
az containerapp show \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --query properties.configuration.ingress.fqdn \
  -o tsv
```

---

## 配置说明

### Scale to Zero配置

```bash
--min-replicas 0      # 最小0个实例（自动缩减到0）
--max-replicas 3      # 最大3个实例（自动扩展）
```

**效果**:
- 无访问时：0实例运行（不计费）
- 有访问时：自动启动（10-30秒冷启动）
- 高流量时：自动扩展到3个实例

### 资源配置

```bash
--cpu 0.5       # 0.5 vCPU
--memory 1Gi    # 1GB内存
```

**说明**:
- 对于本应用已足够
- 可根据需要调整
- 影响成本和性能

### 环境变量

```bash
--env-vars DEPLOYMENT_PLATFORM=azure PORT=8080
```

- `DEPLOYMENT_PLATFORM`: 标识部署平台
- `PORT`: 应用监听端口（Azure固定8080）

---

## 💰 成本分析

### Azure Container Apps免费额度

**每月免费**:
- vCPU时间: 180,000秒 (50小时 @ 1 vCPU)
- 内存: 360,000 GiB秒 (100小时 @ 3.6GB)
- 请求数: 200万次

### 本项目消耗（0.5 vCPU, 1GB内存）

**Scale to Zero启用**:
```
假设每天使用10次，每次10分钟：
每天运行时间 = 10次 × 10分钟 = 100分钟 ≈ 1.67小时
每月运行时间 = 1.67小时 × 30天 = 50小时

vCPU消耗 = 50小时 × 0.5 vCPU = 25 vCPU小时
内存消耗 = 50小时 × 1GB = 50 GB小时

对比免费额度：
vCPU: 25 / 50 = 50% ✅ 在免费额度内
内存: 50 / 100 = 50% ✅ 在免费额度内
```

**结论**: 完全免费 $0/月

### 超额费用（如果超出免费额度）

```
vCPU: $0.000012/秒 ≈ $0.043/小时
内存: $0.0000012/GiB秒 ≈ $0.0043/GB小时

即使24小时运行：
vCPU: 720小时 × 0.5 × $0.043 = ~$15/月
内存: 720小时 × 1GB × $0.0043 = ~$3/月
总计: ~$18/月
```

但使用Scale to Zero，实际费用约$0-5/月。

---

## 🔧 维护和更新

### 更新应用

**方法1: 重新构建镜像**
```bash
# 1. 构建新镜像
az acr build \
  --registry $ACR_NAME \
  --image moonrise:latest \
  --file Dockerfile \
  .

# 2. 重启Container App（自动拉取新镜像）
az containerapp revision copy \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP
```

**方法2: 使用GitHub Actions自动部署**
见下方CI/CD部分

### 查看日志

```bash
# 实时日志
az containerapp logs show \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --follow

# 历史日志
az containerapp logs show \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --tail 100
```

### 监控状态

```bash
# 查看应用状态
az containerapp show \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP

# 查看副本数
az containerapp revision list \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP
```

---

## 🌍 区域选择

### 推荐区域

**亚洲用户**:
```bash
LOCATION="eastasia"        # 香港（推荐）
LOCATION="southeastasia"   # 新加坡
LOCATION="japaneast"       # 日本东京
```

**北美用户**:
```bash
LOCATION="westus2"         # 美国西海岸
LOCATION="eastus"          # 美国东海岸
```

**欧洲用户**:
```bash
LOCATION="westeurope"      # 荷兰
LOCATION="northeurope"     # 爱尔兰
```

### 延迟对比

| 区域 | 中国大陆延迟 | 美国延迟 | 欧洲延迟 |
|------|-------------|---------|---------|
| East Asia (香港) | ~50ms | ~150ms | ~250ms |
| Southeast Asia (新加坡) | ~80ms | ~180ms | ~270ms |
| Railway (美国) | ~150ms | ~50ms | ~150ms |

**建议**: 选择离目标用户最近的区域

---

## 🚨 故障排查

### 问题1: 部署失败

**症状**: `az containerapp create` 报错

**解决**:
```bash
# 查看详细错误
az containerapp create ... --debug

# 常见原因：
# 1. ACR名称已被占用 → 修改ACR_NAME
# 2. 配额不足 → 检查订阅配额
# 3. 镜像拉取失败 → 检查ACR凭据
```

### 问题2: 应用无法访问

**症状**: URL打开显示404或错误

**解决**:
```bash
# 1. 检查应用状态
az containerapp show -n $APP_NAME -g $RESOURCE_GROUP

# 2. 查看日志
az containerapp logs show -n $APP_NAME -g $RESOURCE_GROUP --tail 50

# 3. 检查健康检查
curl https://$APP_URL/health
```

### 问题3: 冷启动太慢

**症状**: 首次访问等待超过30秒

**优化**:
1. 减小Docker镜像体积
2. 预下载星历表（已在Dockerfile中实现）
3. 增加CPU配置（从0.5增加到1）

```bash
az containerapp update \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --cpu 1
```

### 问题4: 超出免费额度

**症状**: 收到Azure账单

**解决**:
1. 检查使用情况：Azure Portal → Cost Management
2. 启用预算警报
3. 调整min-replicas配置
4. 考虑Railway备用部署

---

## 📊 多云对比

### Railway vs Azure Container Apps

| 特性 | Railway | Azure Container Apps |
|------|---------|---------------------|
| **免费额度** | 500小时/月 | 50-100小时/月（vCPU+内存） |
| **部署方式** | Git Push | Docker镜像 |
| **配置难度** | ⭐ 简单 | ⭐⭐ 中等 |
| **Scale to Zero** | ✅ 支持 | ✅ 支持 |
| **冷启动时间** | 10-20秒 | 10-30秒 |
| **服务器位置** | 美国 | 全球多区域 |
| **中国访问速度** | ~150ms | ~50ms（East Asia） |
| **自定义域名** | 免费 | 免费 |
| **监控日志** | 基础 | 丰富（Azure Monitor） |
| **生态集成** | GitHub | Azure全家桶 |

### 推荐使用策略

**策略1: Railway主站 + Azure备用**
- Railway: 主要部署（简单快速）
- Azure East Asia: 亚洲用户优化

**策略2: 智能路由**
- 使用Cloudflare/Azure Front Door
- 亚洲用户 → Azure East Asia
- 其他用户 → Railway

**策略3: 仅Azure**
- 需要Azure服务集成
- 或需要特定区域部署

---

## 🎯 CI/CD自动部署

### 方法1: GitHub Actions（推荐）

创建 `.github/workflows/azure-deploy.yml`:

```yaml
name: Deploy to Azure Container Apps

on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Azure Login
        uses: azure/login@v1
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}

      - name: Build and push image
        run: |
          az acr build \
            --registry moonriseacr \
            --image moonrise:${{ github.sha }} \
            --image moonrise:latest \
            --file Dockerfile \
            .

      - name: Deploy to Container Apps
        run: |
          az containerapp update \
            --name moonrise \
            --resource-group moonrise-rg \
            --image moonriseacr.azurecr.io/moonrise:latest
```

### 方法2: Azure CLI本地部署

每次更新代码后运行：
```bash
./azure/deploy-azure.sh
```

---

## 📝 下一步

### 立即部署
```powershell
# Windows
cd path\to\moonrise
.\azure\deploy-azure.ps1

# Linux/macOS
cd /path/to/moonrise
./azure/deploy-azure.sh
```

### 本地测试
```bash
# 使用Docker Compose测试
docker-compose up

# 访问 http://localhost:8080
```

### 配置自定义域名
```bash
# 添加自定义域名
az containerapp hostname add \
  --name $APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --hostname yourdomain.com
```

---

## 🆘 获取帮助

- **Azure文档**: https://docs.microsoft.com/azure/container-apps/
- **Azure支持**: https://portal.azure.com（创建支持票证）
- **GitHub Issues**: https://github.com/cdlliuy/moonrise/issues
- **Azure CLI参考**: https://docs.microsoft.com/cli/azure/

---

## 📋 快速参考

### 常用命令

```bash
# 查看应用状态
az containerapp show -n moonrise -g moonrise-rg

# 查看日志
az containerapp logs show -n moonrise -g moonrise-rg --follow

# 重启应用
az containerapp revision copy -n moonrise -g moonrise-rg

# 删除应用
az containerapp delete -n moonrise -g moonrise-rg

# 删除所有资源
az group delete -n moonrise-rg --yes
```

### 配置文件位置

```
moonrise/
├── Dockerfile                 # Docker镜像定义
├── docker-compose.yml         # 本地测试
├── azure/
│   ├── deploy-azure.sh       # Linux/macOS部署脚本
│   ├── deploy-azure.ps1      # Windows部署脚本
│   └── container-app.yaml    # Container App配置
└── ...
```

---

**🎉 开始您的Azure部署之旅！**
