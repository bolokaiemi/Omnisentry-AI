import socket


def get_location(domain):

    try:

        ip_address = socket.gethostbyname(domain)

        return {

            "ip_address":
                ip_address,

            "country":
                "Unknown",

            "city":
                "Unknown",

            "latitude":
                None,

            "longitude":
                None
        }

    except Exception:

        return {

            "ip_address":
                None,

            "country":
                "Unknown",

            "city":
                "Unknown",

            "latitude":
                None,

            "longitude":
                None
        }