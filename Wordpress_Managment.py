#!/usr/bin/env python3

import os
import subprocess
import sys

def check_installed(package):
    try:
        subprocess.check_output([package, '--version'])
        return True
    except OSError:
        return False

def install_package(package):
    print(f"Installing {package}...")
    subprocess.call(['sudo', 'apt', 'install', '-y', package])

def create_wordpress_site(site_name):
    os.makedirs(site_name, exist_ok=True)
    os.chdir(site_name)
    with open('docker-compose.yml', 'w') as compose_file:
        compose_file.write(f'''version: '3'
services:
  wordpress:
    image: wordpress:latest
    ports:
      - 80:80
    volumes:
      - ./wp-content:/var/www/html/wp-content
    environment:
      - WORDPRESS_DB_HOST=db
      - WORDPRESS_DB_USER=wordpress
      - WORDPRESS_DB_PASSWORD=wordpress
      - WORDPRESS_DB_NAME=wordpress
  db:
    image: mysql:5.7
    environment:
      - MYSQL_ROOT_PASSWORD=wordpress
      - MYSQL_DATABASE=wordpress
      - MYSQL_USER=wordpress
      - MYSQL_PASSWORD=wordpress
''')

    subprocess.call(['docker-compose', 'up', '-d'])

def create_hosts_entry(site_name):
    with open('/etc/hosts', 'a') as hosts_file:
        hosts_file.write(f'127.0.0.1 {site_name}\n')

def open_in_browser(site_name):
    print(f"Open http://{site_name} in a browser.")

def enable_disable_site(action):
    subprocess.call(['docker-compose', action])

def delete_site(site_name):
    subprocess.call(['docker-compose', 'down'])
    os.chdir('..')
    subprocess.call(['rm', '-rf', site_name])

if __name__ == '__main__':
    if not check_installed('docker'):
        install_package('docker')
    if not check_installed('docker-compose'):
        install_package('docker-compose')

    if len(sys.argv) < 3:
        print("Usage: python3 script.py create <site_name>")
        print("       python3 script.py enable|disable")
        print("       python3 script.py delete <site_name>")
        sys.exit(1)

    action = sys.argv[1]

    if action == 'create':
        site_name = sys.argv[2]
        create_wordpress_site(site_name)
        create_hosts_entry(site_name)
        open_in_browser(site_name)
    elif action == 'enable' or action == 'disable':
        enable_disable_site(action)
    elif action == 'delete':
        site_name = sys.argv[2]
        delete_site(site_name)
    else:
        print(f"Invalid action: {action}")
