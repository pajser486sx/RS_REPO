import asyncio

async def timer(name, delay):
    for i in range(delay, 0, -1):
        print(f'{name}: {i} sekundi preostalo...')
        await asyncio.sleep(1)
    print(f'{name}: Vrijeme je isteklo!')

async def main():
    timers = [
        asyncio.create_task(timer('Timer 1', 3)),
        asyncio.create_task(timer('Timer 2', 5)),
        asyncio.create_task(timer('Timer 3', 7))
    ]

    await asyncio.gather(*timers)

asyncio.run(main())

## prvo se svi taskovi kreiraju u main metodi, main() je u event loopu
## main() je suspended
## timer 1 u event loopu, ispisuje 3 sek, nakon 1 sekunde ide spat i suspendira se
## kad se probudi, timer 2 je u event loopu, ispisuje 5 sek, nakon 1 sekunde ide spat i suspendira se
## kad se probudi, timer 3 je u event loopu, ispisuje 7 sek, nakon 1 sekunde ide spat i suspendira se
## kad se probudi, timer 1 je u event loopu, ispisuje 2 sek, nakon 1 sekunde ide spat i suspendira se
## kad se probudi, timer 2 je u event loopu, ispisuje 4 sek, nakon 1 sekunde ide spat i suspendira se
## kad se probudi, timer 3 je u event loopu, ispisuje 6 sek, nakon 1 sekunde ide spat i suspendira se
## kad se probudi, timer 1 je u event loopu, ispisuje 1 sek, nakon 1 sekunde ide spat i suspendira se
## kad se probudi, timer 2 je u event loopu, ispisuje 3 sek, nakon 1 sekunde ide spat i suspendira se
## kad se probudi, timer 3 je u event loopu, ispisuje 5 sek, nakon 1 sekunde ide spat i suspendira se
## kad se probudi, timer 1 je u event loopu, ispisuje "Vrijeme je isteklo!", timer 1 je gotov
## timer 2 se probudi (u event loopu je), ispisuje 2 sek, nakon 1 sekunde ide spat i suspendira se
## kad se probudi, timer 3 je u event loopu, ispisuje 4 sek, nakon 1 sekunde ide spat i suspendira se
## kad se probudi, timer 2 je u event loopu, ispisuje 1 sek, nakon 1 sekunde ide spat i suspendira se
## kad se probudi, timer 3 je u event loopu, ispisuje 3 sek, nakon 1 sekunde ide spat i suspendira se
## kad se probudi, timer 2 je u event loopu, ispisuje "Vrijeme je isteklo!", timer 2 je gotov
## timer 3 se probudi (u event loopu je), ispisuje 2 sek, nakon 1 sekunde ide spat i suspendira se
## kad se probudi, timer 3 je u event loopu, ispisuje 1 sek, nakon 1 sekunde ide spat i suspendira se
## kad se probudi, timer 3 je u event loopu, ispisuje "Vrijeme je isteklo!", timer 3 je gotov
## event loop je gotov, main() se probudio i završio, oslobađaju se resursi