#!/usr/bin/env python3

import argparse
import concurrent.futures
import contextlib
import fnmatch
import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile



def main():

        run_docker_universe()

        response = input("Do you want to clean up the Docker Container when finished (y/n)? ")

        if response == 'n':
                sys.exit()
        elif response == 'y':
                stop_docker_universe()


def run_docker_universe():
    print('Start Universe Docker Container.')
    command = [ 'docker', 'run', '-d', '-p', '5000:5000', '--name',
        'mesosphere-universe', '-e', 'REGISTRY_HTTP_TLS_CERTIFICATE=/certs/domain.crt', '-e', 'REGISTRY_HTTP_TLS_KEY=/certs/domain.key',
        'mesosphere/universe:latest', 'registry', 'serve', '/etc/docker/registry/config.yml']

    subprocess.check_call(command)


def stop_docker_universe():
    print('Stopping Universe Docker Container.')
    command = [ 'docker', 'stop', 'mesosphere-universe']

    subprocess.check_call(command)

    print('Removing docker Universe Container.')
    command = [ 'docker', 'rm', '-f', 'mesosphere-universe']
    subprocess.check_call(command)

### TK - DEF BELOW IS FOR REFERENCE HOW to work with lists and switch to strings etc.
def upload_docker_image(name):
    print('Pushing docker image: {}'.format(name))
    command = ['docker', 'tag', name,
        format_image_name('localhost:5000', name)]

    ### TK added separator and separator join below becasue command var is a list and we turn it into a string
    separator = ' '
    print("TK-Docker tag Command to run is " + separator.join(command))

    subprocess.check_call(command)

    command = ['docker', 'push', format_image_name('localhost:5000', name)]

    print("TK-Original Docker push Command to run is " + separator.join(command))
    ##
    dockerimage = command[2:3]
    print("TK-Universe Docker Image Name " + separator.join(dockerimage))

    subprocess.check_call(command)



if __name__ == '__main__':
    sys.exit(main())
