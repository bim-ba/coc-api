# <p align="center"> coc-api
<p align="center"><a href="https://developer.clashofclans.com/#/documentation">Clash of Clans API</a> implemented via Python.

## Contents

* [Getting started](#getting-started)
    * Requirements
    * Installation
* [Usage](#usage)
    * Basic usage
* [General API Documentation](#general-api-documentation)
    * Types
    * Methods
    * Exceptions
    * Aliases

## Getting started

This API is tested with Python 3.9-3.10.
There is only one way to install this library:

### Requirements

|Requirement|Version|
|:-----------|-------:|
|attrs|21.4.0|
|cattrs|1.10.0|
|aiohttp|3.8.1|

### Installation

For now, you can install it only from source. This package will be available on PyPi
if code will be good, I think now it is only raw version with raw code.

```
$ git clone https://github.com/bim-ba/coc-api.git
$ cd coc-api
$ pip install -r requirements.txt
```

## Usage

### Basic usage

```python
import asyncio
from client import Client

async def main():
    token = '...' # your token
    coc = Client(token)

    clans = await coc.clans(name='bomb', location='ru', max_members=30)
    print(clans)
    # ['#2P8QU22L2', '#2PPYL9928', '#2PPYL9928', ...]

    clan = await coc.clan(clans[0])
    print(clan.name, clan.location)
    # bomb Location(id=32000193, isCountry=true, name='russia', countryCode='ru')

if __name__ == '__main__':
    asyncio.run(main())
```