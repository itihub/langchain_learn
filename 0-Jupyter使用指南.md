## Jupyter 使用指南
Jupyter Notebook 和 JupyterLab 都是非常流行的交互式计算环境，广泛应用于数据科学、机器学习和教学等领域。它们允许用户创建和共享包含代码、文本、图像和可视化的文档。以下是关于 Jupyter 的使用和安装方式的详细说明

### Jupyter Notebook 和 JupyterLab 的区别
- Jupyter Notebook：
  - 采用传统的笔记本界面，以单个文档为中心，代码和文本单元格交错排列。
  - 界面相对简单，易于上手，适合初学者和简单的交互式任务。
- JupyterLab：
  - 提供更现代化的集成开发环境（IDE），采用标签页式布局，允许在一个窗口中同时打开多个笔记本、编辑器、终端等。
  - 界面更灵活，支持拖放、调整窗口大小等操作，适合复杂的数据分析和开发任务。
Jupyter Notebook 更加轻量级，适合简单的任务，而JupyterLab 提供了更强大的功能和更灵活的界面，适合复杂的开发任务。

### 安装方式
Jupyter 的安装主要有两种方式：使用 Anaconda 或使用 pip。
- 使用 Anaconda 安装：
  - Anaconda 是一个流行的 Python 发行版，包含了许多常用的数据科学包，包括 Jupyter。
  - 如果您已经安装了 Anaconda，那么 Jupyter Notebook 已经默认安装。
  - 安装 Anaconda 的步骤：访问 Anaconda 官网（https://www.anaconda.com/）下载适合您操作系统的安装包。
  - 安装Jupyter Lab：打开Anaconda Prompt或者您的终端，输入指令 conda install -c conda-forge jupyterlab
- 使用 pip 安装：
  - 如果您已经安装了 Python 和 pip，可以使用 pip 安装 Jupyter。
  - 安装步骤：
    - 打开终端或命令提示符，输入以下命令：
      - `pip install jupyter notebook` (安装 Jupyter Notebook)
      - `pip install jupyterlab` (安装 JupyterLab)

### 使用方式
- 启动 Jupyter Notebook：
  - 在终端或命令提示符中，输入 `jupyter notebook` 并按回车键。
  - Jupyter Notebook 将在您的默认浏览器中打开。
- 启动 JupyterLab：
  - 在终端或命令提示符中，输入 `jupyter lab` 并按回车键。
  - JupyterLab 将在您的默认浏览器中打开
  - 创建新的 Notebook：
    - 在 Jupyter 界面中，点击 "New" 按钮，然后选择您想要创建的 Notebook 类型（例如，Python 3）。
  - 运行代码：
    - 在 Notebook 的代码单元格中输入代码，然后按 Shift + Enter 键运行代码。
  - 添加文本：
    - 在 Notebook 中，您可以添加 Markdown 单元格来编写文本、添加标题、插入图像等。
  - 保存和导出：
    - 您可以将 Notebook 保存为 .ipynb 文件，也可以导出为 HTML、PDF 等格式。

### 魔法命令
Jupyter Notebook 和 JupyterLab 中的魔法命令（Magic Commands）是 IPython 内核提供的特殊命令，用于执行一些超出标准 Python 功能范围的操作。它们以 `%` 或 `%%` 开头，分为行魔法命令（line magics）和单元格魔法命令（cell magics）。
1. 魔法命令的类型：
   - 行魔法命令（Line Magics）：
     - 以 `%` 开头，作用于单行代码。
     - 例如：`%timeit` 用于测量单行代码的执行时间。
   - 单元格魔法命令（Cell Magics）：
     - 以 `%%` 开头，作用于整个单元格的代码。
     - 例如：`%%time` 用于测量整个单元格代码的执行时间。
2. 常用魔法命令：
   - 代码计时：
     - `%timeit`：测量单行代码的平均执行时间。
     - `%%time`：测量整个单元格代码的执行时间。
   - 文件操作：
     - `%pwd`：显示当前工作目录。
     - `%ls`：列出当前目录中的文件。
     - `%cd`：更改当前工作目录。
     - `%%writefile filename.py`：将单元格内容写入到指定文件中。
     - `%run filename.py`：运行指定的 Python 脚本。
   - 变量查看：
     - `%who`：显示当前环境中定义的所有变量。
     - `%whos`：显示当前环境中定义的所有变量及其详细信息。
     - `%reset`：删除当前环境中定义的所有变量。
   - 性能分析：
     - `%prun`：使用 Python 的性能分析器运行代码。
   - 系统命令：
     - `!`：在 Jupyter 中执行 shell 命令。例如：`!pip install <package_name>`。
   - 其他魔法命令：
     - `%matplotlib inline`：在 Notebook 中显示 matplotlib 生成的图表。
     - `%%HTML`：将单元格内容渲染为 HTML。
     - `%%javascript`：在 Notebook 中运行 JavaScript 代码。
     - `%%latex`：将单元格内容渲染为 LaTeX 公式。
3. `!pip` 和 `%pip` 安装 Python 依赖包关键区别
   - `!pip` (系统 shell 命令)：
     - `!pip` 实际上是在 Jupyter Notebook 或 JupyterLab 的内核运行的系统 shell 中执行 pip 命令。
     - 这意味着它会使用系统默认的 Python 环境和 pip 安装包。
     - 如果您在虚拟环境中使用 Jupyter，`!pip` 可能会安装到系统默认的 Python 环境中，而不是您的虚拟环境中，导致包安装在错误的位置。
    -使用 ! 可以执行任何系统 shell 命令，不仅仅是 pip。
   - `%pip` (IPython 魔法命令)：
     - `%pip` 是 IPython 内核提供的一个魔法命令，专门用于在当前 Jupyter 内核的 Python 环境中安装包。
     - 这意味着它会始终在您当前运行的 Jupyter Notebook 或 JupyterLab 的 Python 环境中安装包，无论您是否在使用虚拟环境。
     - 因此，`%pip` 是在 Jupyter 中安装包的推荐方式，因为它能确保包安装在正确的环境中。
   - 区别总结：
        - 执行环境：
          - `!pip`：系统 shell 环境。
          - `%pip`：当前 Jupyter 内核环境。
        - 虚拟环境支持：
          - `!pip`：可能安装到错误的 Python 环境中。
          - `%pip`：始终安装到正确的 Python 环境中。
        - 推荐用法：
          - `%pip` 是在 Jupyter 中安装包的推荐方式。
