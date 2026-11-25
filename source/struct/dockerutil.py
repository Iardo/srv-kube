#!/usr/bin/env python3

import subprocess

class DockerUtil:
    '''
    Gets correct "docker-compose" command based on installed version
    '''
    @staticmethod
    def get_command():
        cmd = None

        # Docker Compose Plugin
        if cmd is None:
            try:
                subprocess.call(['docker', 'compose', 'version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                cmd = ['docker', 'compose']
            except FileNotFoundError:
                pass

        # Docker Compose Legacy
        if cmd is None:
            try:
                subprocess.call(['docker-compose', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                cmd = ['docker-compose']
            except FileNotFoundError:
                pass

        return cmd
