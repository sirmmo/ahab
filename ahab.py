#!/bin/env python

import json
import docker
import semantic_version
import os
import requests
import sys
import argparse

AHAB_SERVER = os.getenv("AHAB_SERVER","https://api.ahab.xyz/")



class AhabClient():
    __DEFAULT_FILE_NAME = "ahab.json"

    @classmethod
    def from_params(cls, argv):
        parser = argparse.ArgumentParser(description='Ahab Docker Client', prog="AHAB")
        parser.add_argument("--file", dest="file", help="Custom configuration file", type=str, nargs="?", default=cls.__DEFAULT_FILE_NAME)

        subparsers = parser.add_subparsers(help='Ahab Operations', dest="operation")
        
        parser_init = subparsers.add_parser('init', help='initialization')
        parser_init.add_argument('image', type=str)
        parser_init.add_argument('version', type=str, nargs="?", default="0.0.1")

        parser_pull = subparsers.add_parser('update', help='updates the latest image data from central server')

        parser_build = subparsers.add_parser('build', help='builds only')
        parser_build.add_argument('bump', type=str, default="patch", nargs='?')

        parser_push = subparsers.add_parser('push', help='builds and pushes')
        parser_push.add_argument('bump', type=str, default="patch", nargs='?')


        args = parser.parse_args(argv)
        args = vars(args)

        return args, AhabClient(file=args.get("file"))


    def __init__(self, folder = os.getcwd(), file = self.__DEFAULT_FILE_NAME):
        self.folder = folder 
        self.dockerclient = docker.from_env()
        self.descriptor = file

    def init(self, tag, version):
        try:
            self.read_descriptor()
            print("already initialized!")
        except:
            self.conf = {
                "global":{"image":tag},
                "local":{"version":version}
            }
            self.write_descriptor(init=True)

    def pull(self, mode = "latest"):
        self.read_descriptor()
        url = AHAB_SERVER + "?image="+self.conf.get("global")["image"]
        r = requests.get(url)
        cver = r.json.get("latest")
        self.conf.get("local")["version"] = cver
        self.write_descriptor()

    def read_descriptor(self):
        with open(self.descriptor, "rb") as tf:
            self.conf = json.load(tf)
            self.tag = self.conf.get("global").get("image")
            self.prev_version = self.conf.get("local").get("version")

    def generate_version(self, major = False, minor = False, patch = True):
        self.next_version = semantic_version.Version(self.prev_version, partial=True)
        if patch:
            self.next_version = self.next_version.next_patch()
        if minor:
            self.next_version = self.next_version.next_minor()
        if major:
            self.next_version = self.next_version.next_major()
        self.new_tag = self.tag.format(self.next_version)
        print("version bumped to {}".format(self.new_tag))

    def build(self):
        print("building {} in folder {}".format(self.new_tag, self.folder))
        self.built = self.dockerclient.images.build(path=self.folder, tag=self.new_tag)
        print("built")
        print("updating ahab")
        url = AHAB_SERVER + "?image=" + self.conf.get("global")["image"] + "&version={}".format(self.next_version)
        r = requests.get(url)
        print("updated ahab")

    def push(self):
        print("pushing {}".format(self.new_tag))
        self.dockerclient.images.push(self.new_tag)
        print("pushed")
        print("updating ahab")
        url = AHAB_SERVER + "?image="+self.conf.get("global")["image"]+"&version={}".format(self.next_version)
        r = requests.get(url)
        print("updated ahab")

    def write_descriptor(self, init = False):
        with open(self.descriptor, "wb") as tf:
            if not init:
                self.conf.get("local")["version"] = str(self.next_version)
            json.dump(self.conf, tf)

    def run(self, bump = "patch", push = True):
        self.pull()
        try:
            self.read_descriptor()
            if   bump == "patch":
                self.generate_version(False,False,True)
            elif bump == "minor":
                self.generate_version(False,True,False)
            elif bump == "major":
                self.generate_version(True,False,False)
            self.build()
            if push:
                self.push()
            self.write_descriptor()
        except IOError as ex:
            print("ARRR! {} is missing".format(self.descriptor))
        except Exception as ex:
            print("ARRR! We need a whale to go whale hunting. Docker must be running.")
            print(ex)

def main(argv):

    args, c = AhabClient.from_params(argv)
    if args.get("operation") == "init":
        c.init(args.get("image"), args.get("version"))
    if args.get("operation") == "update":
        c.pull()
    if args.get("operation") == "build":
        c.run(push=False, bump = args.get("bump"))
    if args.get("operation") == "push":
        c.run(bump = args.get("bump"))

if __name__ == "__main__":
    main(sys.argv[1:])
