#!/usr/bin/python
import os
import json
from pprint import pprint

docker_path = "/var/lib/docker"
containers_path = docker_path + "/containers"
graph_path = docker_path + "/graph"

class Containers:

    def __init__(self, path, graph_path):
        self.path = path
        self.graph_path = graph_path

    def get_number_of_containers(self):
        number_of_containers = 0
        for _ in os.listdir(self.path):
            number_of_containers += 1

        return number_of_containers

    def get_container(self):
        container = []
        for container_id in os.listdir(self.path):
            container.append(Container(container_id))

        return container

class Container:

    def __init__(self, id):
        self.id = id

    def short_id(self):
        return self.id[:12]

    def get_image(self):
        with open(containers_path + "/" + self.id + "/config.json") as data_file:
            data = json.load(data_file)

        return data["Image"]


def main():
    print("Container info")

    containers = Containers(containers_path, graph_path)
    print("Number of containers ", containers.get_number_of_containers())

    containers = containers.get_container()

    for container in containers:
        print("Container ID: ", container.short_id())
        print("\tImage: ", container.get_image())



if __name__ == "__main__":
    main()
