FROM ubuntu/python:3.12-24.04_stable
WORKDIR tgbot
COPY . .
RUN pip install -r ./requirements.txt
CMD ['python ./main.py']