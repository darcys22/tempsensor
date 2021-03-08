package main

import (
	"context"
	"fmt"
	"log"
	"net"
	"os"
	"time"

	temp "github.com/darcys22/tempserver/pb"

	"github.com/influxdata/influxdb-client-go/v2"
	"github.com/influxdata/influxdb-client-go/v2/api"
	"google.golang.org/grpc"
)

const (
	//INFLUX CONFIG
	influxdbaddr = "http://192.168.1.98:8086"
	token        = "8a0RAWGIgqFZiS8mx41R3yQPGjrMi4mVWOsCg0IKElk3rUw4OcxIAu1tAuHCX0WNMSJNXyc7Csy8p-Mq6yFCIg=="
	bucket       = "temperature"
	org          = "home"

	//GRPC CONFIG
	network  = "tcp"
	grpcaddr = "192.168.1.98:30051"
)

var (
	db       influxdb2.Client
	writeAPI api.WriteAPI
)

type TempServer struct {
	temp.UnimplementedTransactorServer
}

func (s *TempServer) SendTemp(ctx context.Context, in *temp.TempEvent) (*temp.Void, error) {

	fmt.Printf("{DeviceID:%d, EventID:%d, Temp: %.2f, Humidity:%.2f%%, HeatIndex:%.2f}\n",
		in.GetDeviceId(),
		in.GetEventId(),
		in.GetTempCel(),
		in.GetHumidity(),
		in.GetHeatIdxCel(),
	)

	if db != nil {
		log.Println("posting temp event to influxDB")

		tags := map[string]string{
			"deviceId": fmt.Sprintf("%d", in.GetDeviceId()),
			"eventId":  fmt.Sprintf("%d", in.GetDeviceId()),
		}

		fields := map[string]interface{}{
			"temp":      in.GetTempCel(),
			"humidity":  in.GetHumidity(),
			"heatIndex": in.GetHeatIdxCel(),
		}

		p := influxdb2.NewPoint("sensor-temp", tags, fields, time.Now())
		// write point asynchronously
		writeAPI.WritePoint(p)
		// Flush writes
		writeAPI.Flush()

	}

	return &temp.Void{}, nil
}

func main() {

	client := influxdb2.NewClient(influxdbaddr, token)
	defer client.Close()
	db = client

	ln, err := net.Listen(network, grpcaddr)
	if err != nil {
		log.Println(err)
		os.Exit(1)
	}
	defer ln.Close()

	// get non-blocking write client
	writeAPI = client.WriteAPI(org, bucket)

	log.Printf("Starting Temperator Service: (%s) %s\n", network, grpcaddr)

	// connection loop
	var opts []grpc.ServerOption
	grpcServer := grpc.NewServer(opts...)

	tempServer := &TempServer{}

	temp.RegisterTransactorServer(grpcServer, tempServer)
	if err := grpcServer.Serve(ln); err != nil {
		fmt.Errorf("Could not serve gRPC: %v", err)
	}
}
