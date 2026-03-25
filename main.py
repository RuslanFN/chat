import asyncio
import websockets

clients = set()

async def handler(websocket):
    clients.add(websocket)
    try:
        ip, port = websocket.remote_address
        async for message in websocket:
            print(f"from {ip}: message")
            if clients:
                await asyncio.gather(*(client.send(f"{ip}: {message}") for client in clients))
    except websockets.exceptions.ConnectionClosed:
        print("Connection closed")
    finally:
        clients.remove(websocket)
    
async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        print('Server started on ws://localhost:8765')
        await asyncio.Future()

if __name__ == '__main__':
    asyncio.run(main())