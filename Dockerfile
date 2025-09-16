FROM python:3.12-slim

ENV PATH="/home/jovyan/.local/bin:${PATH}"

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir jupyterlab

WORKDIR /home/jovyan/work

CMD ["jupyter-lab", "--ip=0.0.0.0", "--allow-root", "--notebook-dir=/home/jovyan/work"]