FROM python:3.10
# ENV http_proxy http://proxy-chain.xxx.com:911/
# ENV https_proxy http://proxy-chain.xxx.com:912/
WORKDIR /app

COPY requirements.txt /tmp
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY . ${WORKDIR}
