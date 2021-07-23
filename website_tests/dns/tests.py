import socket


def resolve(domain_name):
    try:
        return socket.gethostbyname(domain_name)
    except socket.gaierror:
        return ""
