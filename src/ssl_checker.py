import ssl
import socket

def check_ssl(domain):

    try:

        context = ssl.create_default_context()

        with socket.create_connection((domain, 443)) as sock:
            with context.wrap_socket(
                sock,
                server_hostname=domain
            ):

                return True

    except Exception:
        return False