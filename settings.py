#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
settings controller

Dev: fa11en
Date Created: September 16, 2017
Last Modified: September 18, 2017

Dev: K4YT3X
Last Modified: April 18, 2018
"""
import os

# ------global variables------

# filepaths
CONFPATH = '/etc/DefenseMatrix.conf'
INSTALLPATH = '/usr/share/DefenseMatrix'
SSHD_CONFIG = '/etc/ssh/sshd_config'

# configuration variables
required_packages = ['ufw', 'iptables', 'arptables']
installed_packages = []


def write_file(data, filename, mode='wb'):
    if not os.path.exists(filename):
        os.system('touch {}'.format(filename))
    with open(filename, mode) as fname:
        fname.writelines(data)


def read_file(filename, mode='r'):
    content = []
    with open(filename, mode) as fname:
        for line in fname:
            content.append(line)

    return content


def get_ifaces():
    return [line.split(':')[0] for line in read_file('/proc/net/dev')
            if line.split(':')]


def get_package_manager(manager):
    if os.path.isfile('/usr/bin/{}'.format(manager.strip())):
        return True
    return False


def gen_pack_install(manager, packs):
    if manager not in valid_managers.keys():
        return False
    if manager == 'apt':
        return 'apt install {} -y'.format(packs)
    elif manager == 'yum':
        return 'yum install {} -y'.format(packs)
    elif manager == 'pacman':
        return 'pacman -S {} --noconfirm'.format(packs)


def gen_pack_remove(manager, packs):
    if manager not in valid_managers.keys():
        return False
    if manager == 'apt':
        return 'apt autoremove {} -y'.format(packs)
    elif manager == 'yum':
        return 'yum remove {} -y'.format(packs)
    elif manager == 'pacman':
        return 'pacman -R {} --noconfirm'.format(packs)


valid_managers = {
    'apt': get_package_manager('apt'),
    'yum': get_package_manager('yum'),
    'pacman': get_package_manager('pacman')
}

package_manager = [man for man in valid_managers.keys() if valid_managers[man]][0]
ifaces = get_ifaces()
