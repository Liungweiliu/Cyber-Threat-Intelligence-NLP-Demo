FROM python:3.12-slim

RUN useradd -ms /bin/bash liangwei

ENV PATH="/home/liangwei/.local/bin:${PATH}"
WORKDIR /home/liangwei/work

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir jupyterlab

USER liangwei
