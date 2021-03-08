"""The Python implementation of the temp sensor server."""
from concurrent import futures
import grpc

import temp_pb2
import temp_pb2_grpc


class TempTransactor(temp_pb2_grpc.TransactorServicer):
    """Provides methods that implement functionality of temp server."""

    def SendTemp(self, request, context):
        print("Message Received")
        print("deviceId = {}".format(request.deviceId))
        print("eventId = {}".format(request.eventId))
        print("humidity = {}".format(request.humidity))
        print("tempCel = {}".format(request.tempCel))
        print("heatIdxCel = {}".format(request.heatIdxCel))
        return temp_pb2.Void()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    temp_pb2_grpc.add_TransactorServicer_to_server(
        TempTransactor(), server)
    # server.add_insecure_port('192.168.1.98:30051')
    server.add_insecure_port('[::]:30051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
