---
name: mac-disk-cleanup
description: 给整台 Mac 腾磁盘空间的完整打法（不是整理某个文件夹，那是 folder-organizer）。按「纯缓存 → 已删App孤儿数据 → 开发工具大镜像 → 聊天App容器 → Downloads过程件 → 长期未用App」六层由安全到危险扫描，先测 TCC 挡住的 iPhone备份/照片/信息/邮件能否读（读不到就声明数字是下限），出一张「安全可删 / 需在App内清 / 系统挡住需授权 / 别碰」四档清单让用户一次确认，然后一律移废纸篓不硬删。凡用户说「电脑/磁盘/储存空间满了、清理一下 Mac、系统数据怎么这么大、腾点空间、C盘满了(Mac)、帮我清内存(实指磁盘)」时使用。查重放最后做，个人 Mac 上重复文件通常只有几十MB～1G。
---

# Mac Disk Cleanup · 给整台机子腾空间

## 先说清一件事：磁盘 ≠ 内存
用户说「清内存」十有八九指**储存空间/磁盘**。第一句就纠正口径，并用 `df -h /System/Volumes/Data` 报一个「已用/可用/占比」基线。

## 核心反常识（实战 82G 沉淀）
1. **别从查重开始。** 个人 Mac 的字节级重复通常 <1G；大头在「系统数据」里的 App 缓存、已删 App 孤儿数据、开发工具镜像。查重是最后一步。
2. **「系统数据 200G+」的本体终端读不到。** iPhone 备份 `~/Library/Application Support/MobileSync/Backup`、照片图库、`~/Library/Messages`、`~/Library/Mail` 被 TCC 挡住，`du` **静默漏算**（实战：家目录算 105G、实际 345G）。必须先测可读性，读不到就明说「以下数字是下限」，导向 系统设置→通用→储存空间 面板，或让用户开 完全磁盘访问→(本App)。
3. **安全护栏是用户敢放手的前提**（见下）。

## 流程

### 0 · 基线 + 可读性
```
python3 scripts/scan_disk.py            # 一次跑完 1-4 层，末尾给四档清单 + JSON
```
脚本会：df 基线；测 TCC 目录可读性；家目录/`~/Library` 大头；六层候选；输出四档。

### 1 · 六层候选（由安全到危险）
| 层 | 位置 | 判定 | 动作 |
|---|---|---|---|
| ① 纯缓存 | `~/Library/Caches/*`、`~/.npm/_cacache`、`~/.cache`、`~/Library/Application Support/Google/Chrome/<Profile>/Service Worker`、各 Electron App 的 `Cache`/`Code Cache`/`GPUCache` | 永远安全，App 自动重建；清 Chrome SW **不退登录** | 安全可删 |
| ② 孤儿数据 | `~/Library/Application Support/<x>`、`~/.<x>` | `/Applications` 与 `~/Applications` 里**没有**对应 App | 安全可删（删前**重新核实**，用户会中途自己删 App） |
| ③ 大镜像 | Claude `Application Support/Claude/vm_bundles/claudevm.bundle`、Docker.raw、Xcode `DerivedData`/`CoreSimulator`、`~/.gemini`、ollama/lmstudio 模型 | 可重建但耗时/流量 | 问一句「用不用」再删 |
| ④ 聊天容器 | `~/Library/Containers/com.tencent.xinWeChat`、`com.bytedance.macos.feishu` | 手动 rm 会丢聊天记录 | **只在 App 内清**（微信→设置→通用→存储空间；飞书→设置→存储空间） |
| ⑤ Downloads 过程件 | `.dmg/.pkg` 安装包、`(1)/(2)/ 2` 重下、zip+解压目录并存、渲染/生成产物、屏幕录制 | 先按名字扫敏感件拎出 | 安全可删（走 folder-organizer 那套分桶） |
| ⑥ 长期未用 App | `mdls -raw -name kMDItemLastUsedDate` 为空或 >10 个月 | root 归属（iMovie/GarageBand/Pages）终端删不了 | 你的 App → Finder delete；root 的让用户访达拖 |

### 2 · 出四档清单（🚪 闸门）
每条标体积。四档：**安全可删 / 需在App内点 / 系统挡住需授权 / 别碰**。一次确认，别挤牙膏。

### 3 · 执行
```
bash scripts/trash.sh "<path1>" "<path2>" ...   # 逐条点名，走 Finder 移废纸篓，可恢复
```
- 一律移废纸篓，**不硬删**；空间在用户清倒废纸篓后才释放，要明说。
- 清浏览器前先退出它（`osascript -e 'tell application "Google Chrome" to quit'` 会超时也没关系，数据照样能移）。
- 自动模式会拦「通配扫描 + 批量 mv」，**逐条点名或走 Finder delete**。

### 4 · 收尾提醒
清倒废纸篓 · 重启浏览器 · 微信/飞书 App 内清 · 储存空间面板看 iPhone 备份/照片（访达→iPhone→管理备份 删旧备份）。

## 护栏（血泪）
- 批量前 `grep -iE '发票|简历|合同|薪|身份证|护照|银行|凭证'` 扫名字，敏感件**拎出不动**并主动告知。
- 删孤儿数据前重新 `ls /Applications` 核实——用户会中途删东西，别按旧扫描结果动手（实战一度误判「文件神秘消失」，其实是用户自己删的）。
- 名字相近的「版本残留」和 `(1)`/` 2` 后缀启发式**都会误报**（S02E03 vs E04、连拍照片）；只信字节 md5 与内容指纹。
- `du -s` 与 `-d1` 同用会**静默空输出**；`~/.Trash` 被 TCC 挡 `ls` 但 `mv` 进去可用。
- 用户自己的 App（stat 归属 = 本人）可 Finder delete；root 归属的需要密码，**不代输**，让用户拖。

## 给小白的产品形态
一键扫描 → 四档清单（每条标体积）→ 一次确认 → 全进废纸篓 → 提醒清倒废纸篓 + 重启浏览器。不给终端、不给命令、开头说清磁盘≠内存。
