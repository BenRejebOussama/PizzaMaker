import asyncio
import socket

BIND_ADDR = "1.2.3.4"  # ton IP source locale

async def handle_client(reader, writer):
    request_line = await reader.readline()
    if not request_line:
        writer.close()
        return

    method, target, _ = request_line.decode().split()
    if method == "CONNECT":
        host, port = target.split(":")
        port = int(port)

        # créer une socket bindée
        rsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        rsock.bind((BIND_ADDR, 0))
        rsock.setblocking(False)
        await asyncio.get_event_loop().sock_connect(rsock, (host, port))

        r_reader, r_writer = await asyncio.open_connection(sock=rsock)

        # réponse au navigateur
        writer.write(b"HTTP/1.1 200 Connection Established\r\n\r\n")
        await writer.drain()

        # pompage bidirectionnel
        async def pipe(src, dst):
            try:
                while True:
                    data = await src.read(4096)
                    if not data:
                        break
                    dst.write(data)
                    await dst.drain()
            except Exception:
                pass
            finally:
                dst.close()

        await asyncio.gather(pipe(reader, r_writer), pipe(r_reader, writer))

    else:
        writer.close()

async def main():
    server = await asyncio.start_server(handle_client, "127.0.0.1", 8080)
    async with server:
        print("Proxy actif sur 127.0.0.1:8080")
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())