#!/usr/bin/python
import os
import json

docker_path = "/var/lib/docker"
containers_path = docker_path + "/containers"
graph_path = docker_path + "/graph"

class Docker:

    def __init__(self):
        self.containers = {}
        self.images = {}

        for image_id in os.listdir(graph_path):
            if image_id != "_tmp":
                self.images[image_id] = Image(image_id)

        for container_id in os.listdir(containers_path):
            self.containers[container_id] = Container(container_id, self)

    def get_number_of_containers(self):
        return len(self.containers)


class Container:

    def __init__(self, id, docker):
        self.id = id
        self.docker = docker

        with open(containers_path + "/" + self.id + "/config.json") as data_file:
            data = json.load(data_file)

        self.image = data["Image"]
        self.name = data["Name"]
        self.images = []

        self.read_image(self.image)

    def read_image(self, image_id):
        image = self.docker.images[image_id]
        self.images.append(image)

        if hasattr(image, "parent_id") and image.parent_id:
            self.read_image(image.parent_id)

    def short_id(self):
        return self.id[:12]


class Image:

    def __init__(self, id):
        self.id = id

        with open(graph_path + "/" + id + "/json") as data_file:
            data = json.load(data_file)

        if "parent" in data:
            self.parent_id = data["parent"]

        if "Size" in data:
            self.size = data["Size"] // 1000000
        else:
            self.size = 0

    def __str__(self):
        return self.id


class Statistics:

    def __init__(self):
        self.images_used = {}

    def used(self, image_id):
        if image_id not in self.images_used:
            self.images_used[image_id] = 0

        self.images_used[image_id] = self.images_used[image_id] + 1

    def get_most_used_images(self):
        ordered = ((k, self.images_used[k]) for k in sorted(self.images_used, key=self.images_used.get, reverse=True))
        return ordered


def main():
    print("Container info")

    docker = Docker()
    print("Number of containers ", docker.get_number_of_containers())

    statistics = Statistics()

    for container in docker.containers.values():
        print("Container ID '{0}' Name '{1}'".format(container.short_id(), container.name))
        print("\tImage: ", container.image)
        print("\tNumber of images: ", len(container.images))

        for image in container.images:
            print("\t\tImage: ", image)
            statistics.used(image.id)

        print()

    print("Most used (ID | Quantity):")
    for k, v in statistics.get_most_used_images():
        print(k, " ", v)
    print()

    print("Not used (ID | Size MB):")
    for image_id in docker.images:
        if image_id in statistics.images_used:
            print(image_id, " ", docker.images[image_id].size)


if __name__ == "__main__":
    main()
