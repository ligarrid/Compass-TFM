FROM python:3.7-buster

RUN apt install curl
RUN python -m pip install rasa==2.8.1

WORKDIR /app

# Copy any additional custom requirements, if necessary (uncomment next line)
COPY requirements-actions.txt ./
# Install extra requirements for actions code, if necessary (uncomment next line)
RUN python -m pip install -r requirements-actions.txt

#set entrypoint for interactive shells
ENTRYPOINT ["rasa"]

#command to run when container is called to run
CMD ["run","--enable-api","--port","8080", "--cors", '"*"', "--debug"]

# 8080
# 5005
