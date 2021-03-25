FROM 'nikolaik/python-nodejs:python3.8-nodejs15'
WORKDIR /app
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git
RUN git clone https://github.com/ai-systems/Probe-Ably.git
WORKDIR /app/Probe-Ably
RUN pip install -r requirements.txt
WORKDIR /app/Probe-Ably/probe_ably/service
RUN yarn install
RUN yarn build
VOLUME /app/Probe-Ably/configurations
EXPOSE 8031/udp
EXPOSE 8031/tcp
WORKDIR /app/Probe-Ably/