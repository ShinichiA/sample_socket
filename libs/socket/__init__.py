from twisted.internet import reactor
from twisted.internet.defer import Deferred
from twisted.internet.protocol import ReconnectingClientFactory
from threading import Thread
from libs import Log

log = Log(__name__)


class WCSClientFactory(ReconnectingClientFactory):
    initialDelay = 1
    maxDelay = 2

    def __init__(self, wcs_client):
        self._client = wcs_client
        self.force_close = False

    def startedConnecting(self, connector):
        log.info('Started to connect.')

    def buildProtocol(self, addr):
        log.info('Connected.')
        log.info('Resetting reconnection delay')
        self.resetDelay()
        return self._client

    def clientConnectionLost(self, connector, reason):
        log.error('Lost connection.  Reason: ' + str(reason))
        ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

    def clientConnectionFailed(self, connector, reason):
        log.error('Connection failed. Reason: ' + str(reason))
        ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)


class TCPCommunication:
    def __init__(self, host, port, wcs_client):
        self._wcs_client = wcs_client
        self.irefactor = reactor.connectTCP(host, port, WCSClientFactory(self._wcs_client))
        thread = Thread(target=self.connect, args=())
        thread.start()

    def connect(self):
        reactor.run()

    def change_host(self, host, port):
        self.irefactor = reactor.connectTCP(host, port, WCSClientFactory(self._wcs_client))

    def close(self):
        print("stop connection")
        self.irefactor.factory.stopTrying()
        self.irefactor.disconnect()
