# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from google.api import metric_pb2 as google_dot_api_dot_metric__pb2
from google.api import (
    monitored_resource_pb2 as google_dot_api_dot_monitored__resource__pb2,
)
from google.cloud.monitoring_v3.proto import (
    metric_service_pb2 as google_dot_cloud_dot_monitoring__v3_dot_proto_dot_metric__service__pb2,
)
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


class MetricServiceStub(object):
    """Manages metric descriptors, monitored resource descriptors, and
  time series data.
  """

    def __init__(self, channel):
        """Constructor.

    Args:
      channel: A grpc.Channel.
    """
        self.ListMonitoredResourceDescriptors = channel.unary_unary(
            "/google.monitoring.v3.MetricService/ListMonitoredResourceDescriptors",
            request_serializer=google_dot_cloud_dot_monitoring__v3_dot_proto_dot_metric__service__pb2.ListMonitoredResourceDescriptorsRequest.SerializeToString,
            response_deserializer=google_dot_cloud_dot_monitoring__v3_dot_proto_dot_metric__service__pb2.ListMonitoredResourceDescriptorsResponse.FromString,
        )
        self.GetMonitoredResourceDescriptor = channel.unary_unary(
            "/google.monitoring.v3.MetricService/GetMonitoredResourceDescriptor",
            request_serializer=google_dot_cloud_dot_monitoring__v3_dot_proto_dot_metric__service__pb2.GetMonitoredResourceDescriptorRequest.SerializeToString,
            response_deserializer=google_dot_api_dot_monitored__resource__pb2.MonitoredResourceDescriptor.FromString,
        )
        self.ListMetricDescriptors = channel.unary_unary(
            "/google.monitoring.v3.MetricService/ListMetricDescriptors",
            request_serializer=google_dot_cloud_dot_monitoring__v3_dot_proto_dot_metric__service__pb2.ListMetricDescriptorsRequest.SerializeToString,
            response_deserializer=google_dot_cloud_dot_monitoring__v3_dot_proto_dot_metric__service__pb2.ListMetricDescriptorsResponse.FromString,
        )
        self.GetMetricDescriptor = channel.unary_unary(
            "/google.monitoring.v3.MetricService/GetMetricDescriptor",
            request_serializer=google_dot_cloud_dot_monitoring__v3_dot_proto_dot_metric__service__pb2.GetMetricDescriptorRequest.SerializeToString,
            response_deserializer=google_dot_api_dot_metric__pb2.MetricDescriptor.FromString,
        )
        self.CreateMetricDescriptor = channel.unary_unary(
            "/google.monitoring.v3.MetricService/CreateMetricDescriptor",
            request_serializer=google_dot_cloud_dot_monitoring__v3_dot_proto_dot_metric__service__pb2.CreateMetricDescriptorRequest.SerializeToString,
            response_deserializer=google_dot_api_dot_metric__pb2.MetricDescriptor.FromString,
        )
        self.DeleteMetricDescriptor = channel.unary_unary(
            "/google.monitoring.v3.MetricService/DeleteMetricDescriptor",
            request_serializer=google_dot_cloud_dot_monitoring__v3_dot_proto_dot_metric__service__pb2.DeleteMetricDescriptorRequest.SerializeToString,
            response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
        )
        self.ListTimeSeries = channel.unary_unary(
            "/google.monitoring.v3.MetricService/ListTimeSeries",
            request_serializer=google_dot_cloud_dot_monitoring__v3_dot_proto_dot_metric__service__pb2.ListTimeSeriesRequest.SerializeToString,
            response_deserializer=google_dot_cloud_dot_monitoring__v3_dot_proto_dot_metric__service__pb2.ListTimeSeriesResponse.FromString,
        )
        self.CreateTimeSeries = channel.unary_unary(
            "/google.monitoring.v3.MetricService/CreateTimeSeries",
            request_serializer=google_dot_cloud_dot_monitoring__v3_dot_proto_dot_metric__service__pb2.CreateTimeSeriesRequest.SerializeToString,
            response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
        )


class MetricServiceServicer(object):
    """Manages metric descriptors, monitored resource descriptors, and
  time series data.
  """

    def ListMonitoredResourceDescriptors(self, request, context):
        """Lists monitored resource descriptors that match a filter. This method does not require a Stackdriver account.
    """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def GetMonitoredResourceDescriptor(self, request, context):
        """Gets a single monitored resource descriptor. This method does not require a Stackdriver account.
    """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def ListMetricDescriptors(self, request, context):
        """Lists metric descriptors that match a filter. This method does not require a Stackdriver account.
    """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def GetMetricDescriptor(self, request, context):
        """Gets a single metric descriptor. This method does not require a Stackdriver account.
    """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def CreateMetricDescriptor(self, request, context):
        """Creates a new metric descriptor.
    User-created metric descriptors define
    [custom metrics](/monitoring/custom-metrics).
    """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def DeleteMetricDescriptor(self, request, context):
        """Deletes a metric descriptor. Only user-created
    [custom metrics](/monitoring/custom-metrics) can be deleted.
    """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def ListTimeSeries(self, request, context):
        """Lists time series that match a filter. This method does not require a Stackdriver account.
    """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def CreateTimeSeries(self, request, context):
        """Creates or adds data to one or more time series.
    The response is empty if all time series in the request were written.
    If any time series could not be written, a corresponding failure message is
    included in the error response.
    """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")


def add_MetricServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
        "ListMonitoredResourceDescriptors": grpc.unary_unary_rpc_method_handler(
            servicer.ListMonitoredResourceDescriptors,
            request_deserializer=google_dot_cloud_dot_monitoring__v3_dot_proto_dot_metric__service__pb2.ListMonitoredResourceDescriptorsRequest.FromString,
            response_serializer=google_dot_cloud_dot_monitoring__v3_dot_proto_dot_metric__service__pb2.ListMonitoredResourceDescriptorsResponse.SerializeToString,
        ),
        "GetMonitoredResourceDescriptor": grpc.unary_unary_rpc_method_handler(
            servicer.GetMonitoredResourceDescriptor,
            request_deserializer=google_dot_cloud_dot_monitoring__v3_dot_proto_dot_metric__service__pb2.GetMonitoredResourceDescriptorRequest.FromString,
            response_serializer=google_dot_api_dot_monitored__resource__pb2.MonitoredResourceDescriptor.SerializeToString,
        ),
        "ListMetricDescriptors": grpc.unary_unary_rpc_method_handler(
            servicer.ListMetricDescriptors,
            request_deserializer=google_dot_cloud_dot_monitoring__v3_dot_proto_dot_metric__service__pb2.ListMetricDescriptorsRequest.FromString,
            response_serializer=google_dot_cloud_dot_monitoring__v3_dot_proto_dot_metric__service__pb2.ListMetricDescriptorsResponse.SerializeToString,
        ),
        "GetMetricDescriptor": grpc.unary_unary_rpc_method_handler(
            servicer.GetMetricDescriptor,
            request_deserializer=google_dot_cloud_dot_monitoring__v3_dot_proto_dot_metric__service__pb2.GetMetricDescriptorRequest.FromString,
            response_serializer=google_dot_api_dot_metric__pb2.MetricDescriptor.SerializeToString,
        ),
        "CreateMetricDescriptor": grpc.unary_unary_rpc_method_handler(
            servicer.CreateMetricDescriptor,
            request_deserializer=google_dot_cloud_dot_monitoring__v3_dot_proto_dot_metric__service__pb2.CreateMetricDescriptorRequest.FromString,
            response_serializer=google_dot_api_dot_metric__pb2.MetricDescriptor.SerializeToString,
        ),
        "DeleteMetricDescriptor": grpc.unary_unary_rpc_method_handler(
            servicer.DeleteMetricDescriptor,
            request_deserializer=google_dot_cloud_dot_monitoring__v3_dot_proto_dot_metric__service__pb2.DeleteMetricDescriptorRequest.FromString,
            response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
        ),
        "ListTimeSeries": grpc.unary_unary_rpc_method_handler(
            servicer.ListTimeSeries,
            request_deserializer=google_dot_cloud_dot_monitoring__v3_dot_proto_dot_metric__service__pb2.ListTimeSeriesRequest.FromString,
            response_serializer=google_dot_cloud_dot_monitoring__v3_dot_proto_dot_metric__service__pb2.ListTimeSeriesResponse.SerializeToString,
        ),
        "CreateTimeSeries": grpc.unary_unary_rpc_method_handler(
            servicer.CreateTimeSeries,
            request_deserializer=google_dot_cloud_dot_monitoring__v3_dot_proto_dot_metric__service__pb2.CreateTimeSeriesRequest.FromString,
            response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        "google.monitoring.v3.MetricService", rpc_method_handlers
    )
    server.add_generic_rpc_handlers((generic_handler,))
