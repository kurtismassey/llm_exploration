FROM python:3.11

RUN apt-get update && apt-get upgrade -y

RUN mkdir /llm_exploration
COPY app/ /llm_exploration/app
COPY .env /llm_exploration
WORKDIR /llm_exploration

RUN pip install -r app/requirements.txt --no-cache-dir --extra-index-url https://download.pytorch.org/whl/cpu

CMD ["python3", "app/chat.py"]