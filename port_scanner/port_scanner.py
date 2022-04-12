import re
import socket
import time

from common_ports import ports_and_services


def get_open_ports(target, port_range, verbose=False):
    open_ports = []
    ipv4_re = re.compile(r'^\d+[.]\d+[.]\d+[.]\d+$')

    address = None
    try:
        address = socket.gethostbyname(target)
    except socket.gaierror:
        if ipv4_re.match(target):
            return "Error: Invalid IP address"
        else:
            return "Error: Invalid hostname"

    if address:
        for port in range(port_range[0], port_range[1] + 1):
            s = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
            try:
                s.settimeout(1)
                s.connect((address, port))
                time.sleep(0.5)
                s.shutdown(socket.SHUT_RDWR)
                s.close()
                open_ports.append(port)
            except Exception as err:
                s.close()
                pass

    if verbose:
        def lookup_service(port):
            try:
                service = ports_and_services[port]
            except KeyError:
                service = 'unknown'
            return port, service

        # format the open ports
        hostname = None
        if ipv4_re.match(target):
            try:
                hostname = socket.gethostbyaddr(target)[0]
            except socket.herror:
                pass
        else:
            hostname = target

        open_ports = list(map(lookup_service, open_ports))

        if hostname:
            result = "Open ports for {} ({})\n".format(hostname, address)
        else:
            result = "Open ports for {}\n".format(address)
        result += "PORT     SERVICE\n"
        for port, name in open_ports:
            result += "{} {}\n".format(str(port).ljust(8), name)
        return result.strip()
    else:
        return open_ports