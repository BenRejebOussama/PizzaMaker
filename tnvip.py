IAC  = 255
DO   = 253
DONT = 254
WILL = 251
WONT = 252
SB   = 250
SE   = 240

OPT_BINARY = 0
OPT_EOR    = 25
OPT_TTYPE  = 24

def negotiate_tnvip(sock):
    sock.settimeout(2)

    def send(b):
        sock.sendall(b)

    # Boucle de négociation
    while True:
        data = sock.recv(1024)
        if not data:
            break

        i = 0
        while i < len(data):
            if data[i] == IAC:
                cmd = data[i+1]
                opt = data[i+2]

                # Serveur: DO <opt>
                if cmd == DO:
                    if opt in (OPT_BINARY, OPT_EOR, OPT_TTYPE):
                        send(bytes([IAC, WILL, opt]))
                    else:
                        send(bytes([IAC, WONT, opt]))

                # Serveur: WILL <opt>
                elif cmd == WILL:
                    if opt in (OPT_BINARY, OPT_EOR):
                        send(bytes([IAC, DO, opt]))
                    else:
                        send(bytes([IAC, DONT, opt]))

                i += 3
            else:
                i += 1

        # Si le serveur a demandé TTYPE → on répond "VIP"
        if b"\xff\xfd\x18" in data:   # IAC DO TTYPE
            send(bytes([IAC, SB, OPT_TTYPE, 0]) + b"VIP" + bytes([IAC, SE]))
            print("🤝 TTYPE=VIP envoyé")

        # On sort quand on voit une vraie trame TNVIP écran
        if b"\xff\xef" in data:  # IAC EOR
            print("🎯 Trame TNVIP reçue")
            return data