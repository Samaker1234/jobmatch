import socket

def test_port(host, port):
    try:
        print(f"Test de connexion vers {host}:{port}...")
        sock = socket.create_connection((host, port), timeout=5)
        print(f"OK: Connexion TCP etablie avec succes sur {host}:{port}")
        sock.close()
        return True
    except Exception as e:
        print(f"ERREUR: Impossible de se connecter a {host}:{port} : {e}")
        return False

if __name__ == "__main__":
    test_port("smtp.gmail.com", 587)
    test_port("smtp.gmail.com", 465)
