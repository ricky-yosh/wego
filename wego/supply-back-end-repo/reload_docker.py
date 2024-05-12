# supply-cloud reload_docker.py
import subprocess

def run_command(command):
    subprocess.run(command, shell=True)

run_command("docker ps -aq | xargs docker stop | xargs docker rm")
run_command("docker rmi -f $(docker images -aq)")

# Run Docker Compose without starting the containers
run_command("docker-compose up --no-start")