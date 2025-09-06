# 使用一個包含 Jupyter 和科學計算工具的官方鏡像作為基礎
FROM jupyter/scipy-notebook:latest

# 切換到工作目錄
WORKDIR /home/jovyan/work

# 將 requirements.txt 複製到容器中
COPY requirements.txt .

# 安裝所有 Python 套件
RUN pip install --no-cache-dir -r requirements.txt

# 啟動 Jupyter Notebook
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--allow-root", "--notebook-dir=/home/jovyan/work"]