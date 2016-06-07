import argparse

import asyncio

from autobahn.asyncio.websocket import WebSocketClientFactory

from daocuratorbot.etherscan import EtherscanClientProtocol

def main():
    parser = argparse.ArgumentParser(description='DAO Curator Bot')
    parser.add_argument('config', nargs='?', help='Config module',
        default='config.development')

    args = parser.parse_args()

    config_mod = __import__(args.config, globals(), locals(), ['AppConfig'])

    appconfig = config_mod.AppConfig

    factory = WebSocketClientFactory(appconfig.ETHERSCAN_WEBSOCKET_URL)
    factory.protocol = EtherscanClientProtocol
    factory.appconfig = appconfig

    loop = asyncio.get_event_loop()
    coro = loop.create_connection(factory, factory.host, factory.port,
        ssl=factory.isSecure)
    loop.run_until_complete(coro)
    loop.run_forever()
    loop.close()


if __name__ == "__main__":
    main()
