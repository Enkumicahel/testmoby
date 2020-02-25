FROM python:3.5

RUN pip install python-telegram-bot --trusted-host pypi.org --trusted-host files.pythonhosted.org

RUN mkdir /bot-proj
ADD . /bot-proj
WORKDIR /bot-proj

CMD python /bot-proj/taskmobot.py