"""Example client shell used to send requests to all BFTList nodes."""


import asyncio

from comm import build_payload, broadcast

ops = ["APPEND"]


async def main():
    print("Welcome to BFT Client shell! Available operations are 'APPEND x'")
    while True:
        s = input("BFTList Client > ")
        parts = s.split(" ")
        if len(parts) != 2:
            print("Missing value for operation")
            continue
        op = parts[0]
        if op not in ops:
            print(f"Illegal operation {op}")
            continue
        val = int(parts[1])
        payload = build_payload(0, op, val)
        await broadcast(payload)

if __name__ == '__main__':
    asyncio.run(main())
