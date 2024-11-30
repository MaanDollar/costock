FROM node:20
LABEL author="Suhyun Park <me@shiftpsh.com>"

# Setting working directory. All the path will be relative to WORKDIR
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . ./
EXPOSE 8000

# Running the app
CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]