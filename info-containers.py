#!/usr/bin/python
import os

docker_path = "/var/lib/docker"
containers_path = docker_path + "/containers"


class Containers:

    def __init__(self, path):
        self.path = path

    def get_number_of_containers(self):
        number_of_containers = 0
        for _ in os.listdir(self.path):
            number_of_containers += 1

        return number_of_containers



def main():
    print("Container info")

    containers = Containers(containers_path)
    print("Number of containers ", containers.get_number_of_containers())


if __name__ == "__main__":
    main()
