FROM python:3.10-buster

WORKDIR /app

COPY . .

RUN pip install poetry -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN poetry lock
RUN poetry install

CMD [ "poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000" ]
EXPOSE 8000