FROM python:3
LABEL author="Suhyun Park <me@shiftpsh.com>"

# Setting working directory. All the path will be relative to WORKDIR
WORKDIR /usr/src/app

RUN curl https://sh.rustup.rs -sSf | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . ./
EXPOSE 8000

# Running the app
CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]