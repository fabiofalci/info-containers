#!/usr/bin/python
import os
import json

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
        with open(containers_path + "/" + self.id + "/config.json") as data_file:
            data = json.load(data_file)

        self.image = data["Image"]
        self.name = data["Name"]
        self.images = []

        self.read_image(self.image)

    def read_image(self, image_id):
        self.images.append(image_id)

        with open(graph_path + "/" + image_id + "/json") as data_file:
            image = json.load(data_file)

        if "parent" in image:
            parent_id = image["parent"]
            if parent_id:
                self.read_image(parent_id)

    def short_id(self):
        return self.id[:12]


def main():
    print("Container info")

    containers = Containers(containers_path, graph_path)
    print("Number of containers ", containers.get_number_of_containers())

    containers = containers.get_container()

    for container in containers:
        print("Container ID '{0}' Name '{1}'".format(container.short_id(), container.name))
        print("\tImage: ", container.image)
        print("\tNumber of images: ", len(container.images))

        for image in container.images:
            print("\t\tImage: ", image)


        print()


if __name__ == "__main__":
    main()
