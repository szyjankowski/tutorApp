FROM python:3.11
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY requirements.txt /app/
COPY shell_commands/install_dependencies.sh /app/
COPY shell_commands/setup_commands.sh /app/
#COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN /app/install_dependencies.sh
COPY . /app/
