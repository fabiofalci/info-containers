#!/usr/bin/python

docker_path = "/var/lib/docker"
containers_path = docker_path + "/containers"


class Containers:

    def __init__(self, path):
        self.path = path


def main():
    print("Container info")

    containers = Containers(containers_path)


if __name__ == "__main__":
    main()
