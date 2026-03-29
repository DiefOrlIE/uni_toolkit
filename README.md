# Uni Toolkit

一个轻量的静态网页工具箱仓库，收纳了我做的几个独立 HTML 小工具和学习页。

项目现在不依赖构建工具，也不需要后端服务。所有页面都是原生 HTML / CSS / JavaScript，克隆后可以直接在浏览器里打开使用。

## 项目内容

- `index.html`
  - 新的工具目录首页，用来集中展示和跳转所有小工具页面。
- `gulou-what-to-eat.html`
  - 原 `index.html` 复制出的独立工具页，对应“鼓楼今天吃什么”随机选择器。
- `bionic_reader.html`
  - 阅读增强工具页，适合粘贴文本或处理阅读内容。
- `python_bro.html`
  - Python List / Dict / Tuple / String 语法手册。
- `htmlqs.html`
  - 面向 CS 学生的 HTML Fundamentals 学习页。

## 使用方式

1. 克隆仓库到本地。
2. 直接用浏览器打开 `index.html`。
3. 在目录首页中点击对应入口，进入具体工具页面。

如果只想单独使用某个页面，也可以直接打开对应的 `.html` 文件。

## GitHub Pages 部署

如果想把这个仓库直接发布成静态网站，可以用 GitHub Pages：

1. 把当前仓库推送到 GitHub。
2. 进入仓库页面，打开 `Settings`。
3. 在左侧找到 `Pages`。
4. 在 `Build and deployment` 里选择：
   - `Source`: `Deploy from a branch`
   - `Branch`: `main`
   - `Folder`: `/ (root)`
5. 保存后等待 GitHub 完成部署。

部署完成后，站点会默认以根目录下的 `index.html` 作为首页，也就是现在这个工具目录页。

如果仓库名是 `uni_toolkit`，通常访问地址会是：

- `https://你的用户名.github.io/uni_toolkit/`

后续你只要继续往仓库根目录添加新的 `.html` 文件，并在 `index.html` 中补上入口，就可以继续扩展这个静态站点。

## 适合的场景

- 收纳个人做过的前端小工具
- 快速发布到静态托管平台
- 作为单文件网页作品集
- 给同学或朋友直接分享一个可打开即用的页面

## 目录建议

后续如果继续扩展，可以保持下面这类命名方式，方便目录页持续维护：

- 功能型工具：`feature-name.html`
- 学习资料页：`topic-notes.html`
- 作品展示页：`project-name.html`

## 备注

- 当前仓库是静态站点风格，适合部署到 GitHub Pages、Netlify、Vercel 静态托管等平台。
- `gulou-what-to-eat.html` 是从旧首页保留下来的原始工具页，新的 `index.html` 现在承担站点目录入口的角色。
