id="aw1j5w"
# ==========================================
# OMMINSENTIRY AI
# IP RESOLVER
# ==========================================

import socket


def resolve_ip(domain: str):

    """
    Resolve a domain name to an IP address.

    Example:
        google.com
        -> 142.250.185.78
    """

    try:

        # Remove protocol if user enters it
        domain = domain.replace(
            "https://",
            ""
        )

        domain = domain.replace(
            "http://",
            ""
        )

        # Remove trailing slash
        domain = domain.strip("/")

        ip_address = socket.gethostbyname(
            domain
        )

        return {

            "success":
                True,

            "domain":
                domain,

            "ip_address":
                ip_address
        }

    except Exception as e:

        return {

            "success":
                False,

            "domain":
                domain,

            "ip_address":
                None,

            "error":
                str(e)
        }


# ==========================================
# TEST MODE
# ==========================================

if __name__ == "__main__":

    test_domain = "google.com"

    result = resolve_ip(
        test_domain
    )

    print(
        "\nIP Resolver Test\n"
    )

    print(result)
