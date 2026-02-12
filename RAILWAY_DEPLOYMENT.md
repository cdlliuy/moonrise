# Railway部署指南 - 月升月落程序

## ✅ 准备工作已完成

您的项目现在已经完全准备好部署到Railway了！

**已完成的配置：**
- ✅ Procfile（Railway启动命令）
- ✅ runtime.txt（Python 3.11）
- ✅ requirements.txt（包含gunicorn）
- ✅ run.py（生产环境适配）
- ✅ .railwayignore（排除不必要文件）
- ✅ Git仓库初始化和首次提交

---

## 🚀 部署步骤（详细图文）

### 步骤1: 创建GitHub仓库

#### 1.1 访问GitHub
打开浏览器，访问 https://github.com/

#### 1.2 登录您的GitHub账号
- 如果没有账号，点击"Sign up"注册
- 如果有账号，点击"Sign in"登录

#### 1.3 创建新仓库
1. 点击右上角的"+"号
2. 选择"New repository"
3. 填写信息：
   - **Repository name**: `moonrise`（建议使用这个名称）
   - **Description**: "月升月落 - 月相和月升月落时间计算程序"
   - **Public/Private**: 选择Public（公开，免费）或Private（私有）
   - **不要**勾选"Add a README file"（我们已经有了）
   - **不要**勾选"Add .gitignore"（我们已经有了）
4. 点击"Create repository"

#### 1.4 复制仓库地址
创建成功后，GitHub会显示一个地址，类似：
```
https://github.com/您的用户名/moonrise.git
```
复制这个地址（后面会用到）

---

### 步骤2: 推送代码到GitHub

#### 2.1 在PowerShell中连接GitHub仓库

打开PowerShell（在moonrise目录下），运行以下命令：

```powershell
# 添加远程仓库（替换成您自己的GitHub地址）
git remote add origin https://github.com/您的用户名/moonrise.git

# 重命名分支为main（GitHub默认使用main）
git branch -M main

# 推送到GitHub
git push -u origin main
```

**注意**: 如果是第一次使用Git，可能需要配置用户名和邮箱：
```powershell
git config --global user.name "您的名字"
git config --global user.email "您的邮箱"
```

#### 2.2 输入GitHub凭据
- 如果要求输入用户名密码，输入您的GitHub用户名和密码
- **重要**: 现在GitHub需要使用Personal Access Token代替密码
  - 访问 https://github.com/settings/tokens
  - 点击"Generate new token (classic)"
  - 勾选"repo"权限
  - 生成token并复制（只显示一次！）
  - 在密码处粘贴这个token

#### 2.3 验证推送成功
刷新GitHub仓库页面，应该能看到所有代码文件了。

---

### 步骤3: 注册Railway账号

#### 3.1 访问Railway官网
打开浏览器，访问 https://railway.app/

#### 3.2 注册/登录
**推荐方式**：使用GitHub账号登录
1. 点击"Login"
2. 选择"Login with GitHub"
3. 授权Railway访问您的GitHub账号
4. 完成登录

**优点**: 直接连接GitHub，后续部署更方便

---

### 步骤4: 在Railway创建项目

#### 4.1 创建新项目
1. 登录Railway后，点击"New Project"
2. 选择"Deploy from GitHub repo"

#### 4.2 授权访问GitHub
如果是第一次，需要授权：
1. 点击"Configure GitHub App"
2. 选择"All repositories"或"Only select repositories"
3. 如果选择"Only select repositories"，勾选`moonrise`仓库
4. 点击"Save"

#### 4.3 选择仓库
1. 回到Railway，刷新页面
2. 在列表中找到`moonrise`仓库
3. 点击它开始部署

---

### 步骤5: 等待自动部署

#### 5.1 部署过程
Railway会自动：
1. ✅ 检测Python项目
2. ✅ 读取`runtime.txt`确定Python版本
3. ✅ 安装`requirements.txt`中的依赖
4. ✅ 下载Skyfield星历表文件（~17MB，需要几分钟）
5. ✅ 执行`Procfile`中的启动命令

#### 5.2 查看部署日志
1. 点击"Deployments"标签
2. 点击最新的部署记录
3. 点击"View Logs"查看实时日志
4. **正常情况下会看到**：
   ```
   Installing dependencies...
   Downloading skyfield...
   Starting web server...
   ```

#### 5.3 等待时间
- **首次部署**: 约5-10分钟（下载依赖+星历表）
- **后续部署**: 约2-3分钟（有缓存）

---

### 步骤6: 获取访问域名

#### 6.1 生成域名
1. 等待部署状态变为"Active"（绿色）
2. 点击"Settings"标签
3. 找到"Domains"部分
4. 点击"Generate Domain"按钮
5. Railway会自动生成一个域名，类似：
   ```
   moonrise-production-xxxx.up.railway.app
   ```

#### 6.2 访问您的应用
1. 复制这个域名
2. 在浏览器中打开
3. **恭喜！您的月相程序已经上线了！** 🎉

---

### 步骤7: 在手机上访问

#### 7.1 手机浏览器访问
1. 在手机上打开任意浏览器（Chrome、Safari等）
2. 输入Railway给您的域名
3. 访问您的月相程序

#### 7.2 添加到主屏幕（可选）

**iPhone用户**:
1. 在Safari中打开网站
2. 点击底部的分享按钮
3. 选择"添加到主屏幕"
4. 点击"添加"
5. 像App一样使用！

**Android用户**:
1. 在Chrome中打开网站
2. 点击右上角三个点
3. 选择"添加到主屏幕"
4. 点击"添加"

---

## 🎯 部署后验证清单

### 功能测试
- [ ] 页面能正常打开
- [ ] 城市选择器工作正常
- [ ] 可以切换月份
- [ ] 点击日期显示详细信息
- [ ] 月相图标显示正确
- [ ] 月升月落时间显示
- [ ] 农历日期显示正确
- [ ] 手机端布局正常

### 性能检查
- [ ] 首次加载速度可接受（可能较慢）
- [ ] 后续访问速度快
- [ ] 月份切换流畅

---

## 🔧 常见问题排查

### 问题1: 部署失败，显示"Build failed"

**原因**: 依赖安装失败

**解决方案**:
1. 查看部署日志，找到错误信息
2. 常见原因：
   - Python版本不兼容 → 检查`runtime.txt`
   - 依赖冲突 → 检查`requirements.txt`格式
3. 修复后，推送新代码：
   ```powershell
   git add .
   git commit -m "Fix deployment issues"
   git push
   ```
4. Railway会自动重新部署

### 问题2: 部署成功但访问报错

**原因**: 应用崩溃

**解决方案**:
1. 在Railway点击"Deployments" → "View Logs"
2. 查找Python错误信息
3. 常见问题：
   - 端口配置错误 → 确认`Procfile`正确
   - 导入错误 → 确认所有文件都已推送

### 问题3: 星历表下载超时

**原因**: Railway构建时下载星历表文件超时

**解决方案A**: 等待重试
- Railway会自动重试
- 或手动点击"Redeploy"

**解决方案B**: 预先下载星历表（高级）
- 将`de421.bsp`文件包含在仓库中
- 修改`.gitignore`不排除它
- 重新推送

### 问题4: 访问速度很慢

**原因**: Railway服务器在美国

**解决方案**:
- 首次访问会较慢（冷启动）
- 后续访问会快很多（有缓存）
- 如果持续慢，考虑使用国内云服务器

### 问题5: 超出免费额度

**原因**: 月运行时间超过500小时

**解决方案**:
1. 查看Railway仪表板的使用情况
2. 选项：
   - 接受少量费用（约$5/月）
   - 仅在需要时启用部署
   - 设置自动暂停不活跃服务

---

## 💰 费用说明

### Railway免费额度
- **运行时间**: 500小时/月
- **内存**: 512MB
- **磁盘**: 1GB
- **流量**: 100GB/月

### 预估消耗
- **24小时运行**: 720小时/月 ❌ 超出免费额度
- **每天8小时**: 240小时/月 ✅ 在免费额度内
- **按需使用**: 0-100小时/月 ✅ 完全免费

### 超额费用
- **计费方式**: $0.000231/小时
- **超额220小时**: 约$5/月

### 建议
- 个人使用，免费额度足够
- 如果24小时运行，接受约$5/月费用
- 或使用内网穿透作为备选方案

---

## 🔄 后续更新部署

### 自动部署
Railway支持自动部署：
1. 修改本地代码
2. 提交并推送到GitHub：
   ```powershell
   git add .
   git commit -m "Update feature"
   git push
   ```
3. Railway自动检测并重新部署
4. 约2-3分钟后更新生效

### 手动部署
在Railway仪表板：
1. 点击"Deployments"
2. 点击"Redeploy"

---

## 📞 获取帮助

### Railway官方文档
https://docs.railway.app/

### Railway社区
https://discord.gg/railway

### 本项目GitHub Issues
如果您将项目公开，可以在GitHub Issues中提问

---

## 🎉 恭喜您！

您已经成功将月升月落程序部署到云端！

**现在您可以：**
- ✅ 在任何地方通过手机访问
- ✅ 分享链接给朋友
- ✅ 随时查看月相和月升月落时间
- ✅ 体验专业级的天文计算

**域名示例**:
```
https://your-project-name.up.railway.app
```

**记得保存您的Railway域名！** 🌙✨

---

## 附录：完整部署命令速查

```powershell
# 1. Git配置（首次使用）
git config --global user.name "您的名字"
git config --global user.email "您的邮箱"

# 2. 连接GitHub
git remote add origin https://github.com/您的用户名/moonrise.git
git branch -M main
git push -u origin main

# 3. 后续更新
git add .
git commit -m "更新说明"
git push
```

---

**部署愉快！** 🚀
