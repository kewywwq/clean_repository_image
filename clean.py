#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = "Queenie Wang"

import json
import sys
import commands
from http_request import http_delete, http_get_content, http_get_info

PRIVATE_REGISTRY = sys.argv[1]
HEADER = {"Accept": "application/vnd.docker.distribution.manifest.v2+json"}


def clean_all():
    get_all_url = "{0}/v2/_catalog".format(PRIVATE_REGISTRY)
    ret_all = http_get_content(url=get_all_url, header=HEADER)
    all_images = json.loads(ret_all)["repositories"]
    for image in all_images:
        print image
        tags = get_tags(image=image)
        print tags
        if tags is not None:
            for tag in tags:
                if tag != "latest":
                    digest = get_digest(image=image, tag=tag)
                    del_url = "{0}/v2/{1}/manifests/{2}".format(PRIVATE_REGISTRY, image, digest)
                    http_delete(url=del_url)


def clean_repo(repo):
    tags = get_tags(image=repo)
    print tags
    if tags is not None:
        for tag in tags:
            if tag != "latest":
                digest = get_digest(image=repo, tag=tag)
                del_url = "{0}/v2/{1}/manifests/{2}".format(PRIVATE_REGISTRY, repo, digest)
                http_delete(url=del_url)


def clean_repo_tag(repo,tag):
    digest = get_digest(image=repo, tag=tag)
    del_url = "{0}/v2/{1}/manifests/{2}".format(PRIVATE_REGISTRY, repo, digest)
    http_delete(url=del_url)


def get_tags(image):
    url = "{0}/v2/{1}/tags/list".format(PRIVATE_REGISTRY,image)
    ret = http_get_content(url=url, header=HEADER)
    tags = json.loads(ret)["tags"]
    return tags


def get_digest(image, tag):
    url = "{0}/v2/{1}/manifests/{2}".format(PRIVATE_REGISTRY, image, tag)
    ret = http_get_info(url=url, header=HEADER)
    if ret != "":
        digest = ret.getheader("Docker-Content-Digest")
    else:
        digest = ""
    return digest


def registry_gc():
    cmd = "docker exec registry bin/registry garbage-collect /etc/docker/registry/config.yml"
    commands.getoutput(cmd)

if __name__ == "__main__":
    count = sys.argv.__len__()
    if count == 2:
        clean_all()
    elif count == 3:
        clean_repo(sys.argv[2])
    elif count == 4:
        clean_repo_tag(sys.argv[2], sys.argv[3])
    else:
        print "parameters are invalid."
    registry_gc()
