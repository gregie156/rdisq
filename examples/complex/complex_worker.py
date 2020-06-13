import logging
from rdisq.service import RdisqService, remote_method
from rdisq.redis_dispatcher import PoolRedisDispatcher


class ComplexWorker(RdisqService):
    logger = logging.getLogger(__name__)
    log_returned_exceptions = True
    service_name = "Worker"
    response_timeout = 5
    stop_on_fail = False
    redis_dispatcher = PoolRedisDispatcher(host='localhost', port=6379, db=0)

    @staticmethod
    @remote_method
    def calculate(a, b, c):
        return (a * b) + c;

    @remote_method
    def add_log(self, log_line):
        # A very crude way to log :) just for the sake of the example
        print(log_line)
        return log_line

    def on_start(self):
        val = "Service started: %s!" % (self.service_name,)
        print(val)
        return  val

    def pre(self, q):
        val = "Processing from %s" % (q,)
        print(val)
        return val

    def post(self, q):
        val = "Finished processing from %s" % (q,)
        print(val)
        return val


if __name__ == '__main__':
    ComplexWorker().process()
