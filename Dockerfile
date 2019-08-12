FROM arm32v7/python:3-alpine
RUN apk update; apk add --no-cache build-base openssl-dev libffi-dev cmake

# set working directory
WORKDIR /usr/src/app

# add requirements
COPY requirements.txt ./

# install requirements
RUN pip install --no-cache-dir -r requirements.txt

# add entrypoint.sh
COPY . .

# run server
CMD ["./entrypoint.sh"]
