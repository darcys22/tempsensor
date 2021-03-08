"""The Python implementation of the gRPC Godbledger client."""

import random
import logging

import grpc

import temp_pb2
import temp_pb2_grpc


def run():
    with grpc.insecure_channel('192.168.1.98:30051') as channel:
        stub = temp_pb2_grpc.TransactorStub(channel)
        print("-------------- Sending Temperature --------------")
        response = stub.SendTemp(temp_pb2.TempEvent(
                deviceId = 1,
                eventId = 2,
                humidity = 3.0,
                tempCel = 4.0,
                heatIdxCel = 5.0
            ))


if __name__ == '__main__':
    logging.basicConfig()
    run()
