from queue import Queue


#######################################################################################


class MessageBroker:
    def __init__(self):
        # Hash to keep track of all the queues
        self.channels = dict()

    def subscribe(self, channel: str, maxsize: int = 2) -> Queue:
        """ Create a message queue with name `channel` and returns the queue.
        Subscribed client can listen on this queue to recieve messages.
        """

        self.channels[channel] = Queue(maxsize)
        return self.channels[channel]

    def publish(self, channel: str, message: str) -> None:
        """ Insert `message` to the queue with name `channel`, if exists. """

        if self.channels.get(channel, None):
            self.channels[channel].put_nowait(message)
        else:
            raise Exception(f'Channel {channel} does not exists!')


#######################################################################################


def format_SSE(message: str):
    """ Format `message` to be sent in SSE """

    return f'data: {message}\n\n'
