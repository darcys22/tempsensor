#!/usr/bin/python3

import Adafruit_DHT
import time

import config

import grpc

import temp_pb2
import temp_pb2_grpc

from typing import Union

C = [
    0.363445176,
    0.988622465,
    4.777114035,
    -0.114037667,
    -8.50208e-4,
    - 2.0716198e-2,
    6.87678e-4,
    2.74954e-4,
    0
]

def from_celsius(temperature, relative_humidity):
    """
    :type temperature: Union[int, float]
    :type relative_humidity: Union[int, float]
    :rtype: float
    Take temperature in Celsius and relative humidity in % value and return calculated heat index
    """
    # convert temperature to Fahrenheit
    T = float(temperature) * 9 / 5 + 32

    # get heat-index
    heat_index_in_fahrenheit = from_fahrenheit(T, relative_humidity)

    # convert back to Celsius
    heat_index_in_celsius = (heat_index_in_fahrenheit - 32) * 5 / 9

    return heat_index_in_celsius


def from_fahrenheit(temperature, relative_humidity):
    """
    :type temperature: Union[int, float]
    :type relative_humidity: Union[int, float]
    :rtype: float
    Take temperature in Fahrenheit and relative humidity in % value and return calculated heat index
    """
    T = float(temperature)
    R = float(relative_humidity)
    # create temperary values for ease of use
    T2 = pow(T, 2)
    R2 = pow(R, 2)

    # Calculating heat-index
    heat_index = C[0] + C[1] * T + C[2] * R + C[3] * T * R + \
        C[4] * T2 + C[5] * R2 + C[6] * T2 * R + \
        C[7] * T * R2 + C[8] * T2 * R2

    return heat_index
 
DHT_SENSOR = Adafruit_DHT.DHT11

with grpc.insecure_channel('192.168.1.98:30051') as channel:
	hum, tmp = Adafruit_DHT.read(DHT_SENSOR, config.DHT_PIN)
	if hum is not None and tmp is not None:
		hiCel = from_celsius(tmp, hum);
		stub = temp_pb2_grpc.TransactorStub(channel)
		response = stub.SendTemp(temp_pb2.TempEvent(
			deviceId = config.deviceId,
			eventId = config.eventId,
			humidity = hum,
			tempCel = tmp,
			heatIdxCel = hiCel
		))
			
 
