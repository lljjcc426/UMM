# 导入 lljjcc426/UMM

## 本次状态

2026-10-15：
- GitHub连接器读取成功；目标仓库为公开空仓库，默认分支main。
- 元数据为`pull=true, push=false`。
- 尝试创建README，返回`403 Resource not accessible by integration`。
- **没有文件成功写入，没有远端提交，没有Pull Request。**

本包是已经整理并验证的本地仓库文件，而不是“已经推送成功”的证明。

## 使用连接器继续写入所需条件

应由仓库拥有者确认当前GitHub连接所关联的身份/应用已包含该仓库，并具备写文件所需的Contents写权限。
ChatGPT的“是否每次询问”设置不等于GitHub的仓库授权；不需要在聊天中发送token、密码或私钥。

## 使用你自己已经有权限的Git环境导入

下面命令**没有由本次助手执行**。先解压并进入本包顶层目录，检查本目录文件确实是准备公开的资料。

如果远端仍然是空仓库：

```bash
git init -b main
git remote add origin https://github.com/lljjcc426/UMM.git
git ls-remote --heads origin
```

检查上一条输出。若已有任何分支，停止以下空仓库流程，采用后面的非空仓库流程。

```bash
python scripts/validate_catalog.py
python -m unittest discover -s tests -v
git add README.md CHANGELOG.md PUBLISH_TO_GITHUB.md .gitignore docs data archive scripts tests examples reports
git commit -m "docs: organize UMM and Chinese stroke-process research"
git push -u origin main
```

Git会使用你本机已经设置的授权。不要把凭据写进URL，不要使用`--force`。

## 如果仓库已不再为空

先克隆到新目录并创建资料分支；将本包中的资料复制进去，逐项审查差异，不要整体覆盖已有README或其他文件：

```bash
git clone https://github.com/lljjcc426/UMM.git UMM-existing
cd UMM-existing
git switch -c docs/umm-handwriting-research-20261015
```

复制/合并本包资料后运行验证，再正常commit和push该分支。通过仓库页面创建Pull Request，审查后合并。不要重写远端历史。

## 导入前最后检查

- 本包没有匿名稿件和字体/数据/权重文件。
- 历史结果标为继承，不是本轮实测。
- `data/experiment_template.csv`尚无真实成绩。
- `data/provenance.json`里的写入失败是本次交付历史，后续成功上传可追加新记录，不应伪造原状态。
