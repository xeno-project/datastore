# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from google.cloud.talent_v4beta1.proto import (
    tenant_pb2 as google_dot_cloud_dot_talent__v4beta1_dot_proto_dot_tenant__pb2,
)
from google.cloud.talent_v4beta1.proto import (
    tenant_service_pb2 as google_dot_cloud_dot_talent__v4beta1_dot_proto_dot_tenant__service__pb2,
)
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


class TenantServiceStub(object):
    """A service that handles tenant management, including CRUD and enumeration.
  """

    def __init__(self, channel):
        """Constructor.

    Args:
      channel: A grpc.Channel.
    """
        self.CreateTenant = channel.unary_unary(
            "/google.cloud.talent.v4beta1.TenantService/CreateTenant",
            request_serializer=google_dot_cloud_dot_talent__v4beta1_dot_proto_dot_tenant__service__pb2.CreateTenantRequest.SerializeToString,
            response_deserializer=google_dot_cloud_dot_talent__v4beta1_dot_proto_dot_tenant__pb2.Tenant.FromString,
        )
        self.GetTenant = channel.unary_unary(
            "/google.cloud.talent.v4beta1.TenantService/GetTenant",
            request_serializer=google_dot_cloud_dot_talent__v4beta1_dot_proto_dot_tenant__service__pb2.GetTenantRequest.SerializeToString,
            response_deserializer=google_dot_cloud_dot_talent__v4beta1_dot_proto_dot_tenant__pb2.Tenant.FromString,
        )
        self.UpdateTenant = channel.unary_unary(
            "/google.cloud.talent.v4beta1.TenantService/UpdateTenant",
            request_serializer=google_dot_cloud_dot_talent__v4beta1_dot_proto_dot_tenant__service__pb2.UpdateTenantRequest.SerializeToString,
            response_deserializer=google_dot_cloud_dot_talent__v4beta1_dot_proto_dot_tenant__pb2.Tenant.FromString,
        )
        self.DeleteTenant = channel.unary_unary(
            "/google.cloud.talent.v4beta1.TenantService/DeleteTenant",
            request_serializer=google_dot_cloud_dot_talent__v4beta1_dot_proto_dot_tenant__service__pb2.DeleteTenantRequest.SerializeToString,
            response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
        )
        self.ListTenants = channel.unary_unary(
            "/google.cloud.talent.v4beta1.TenantService/ListTenants",
            request_serializer=google_dot_cloud_dot_talent__v4beta1_dot_proto_dot_tenant__service__pb2.ListTenantsRequest.SerializeToString,
            response_deserializer=google_dot_cloud_dot_talent__v4beta1_dot_proto_dot_tenant__service__pb2.ListTenantsResponse.FromString,
        )


class TenantServiceServicer(object):
    """A service that handles tenant management, including CRUD and enumeration.
  """

    def CreateTenant(self, request, context):
        """Creates a new tenant entity.
    """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def GetTenant(self, request, context):
        """Retrieves specified tenant.
    """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def UpdateTenant(self, request, context):
        """Updates specified tenant.
    """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def DeleteTenant(self, request, context):
        """Deletes specified tenant.
    """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def ListTenants(self, request, context):
        """Lists all tenants associated with the project.
    """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")


def add_TenantServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
        "CreateTenant": grpc.unary_unary_rpc_method_handler(
            servicer.CreateTenant,
            request_deserializer=google_dot_cloud_dot_talent__v4beta1_dot_proto_dot_tenant__service__pb2.CreateTenantRequest.FromString,
            response_serializer=google_dot_cloud_dot_talent__v4beta1_dot_proto_dot_tenant__pb2.Tenant.SerializeToString,
        ),
        "GetTenant": grpc.unary_unary_rpc_method_handler(
            servicer.GetTenant,
            request_deserializer=google_dot_cloud_dot_talent__v4beta1_dot_proto_dot_tenant__service__pb2.GetTenantRequest.FromString,
            response_serializer=google_dot_cloud_dot_talent__v4beta1_dot_proto_dot_tenant__pb2.Tenant.SerializeToString,
        ),
        "UpdateTenant": grpc.unary_unary_rpc_method_handler(
            servicer.UpdateTenant,
            request_deserializer=google_dot_cloud_dot_talent__v4beta1_dot_proto_dot_tenant__service__pb2.UpdateTenantRequest.FromString,
            response_serializer=google_dot_cloud_dot_talent__v4beta1_dot_proto_dot_tenant__pb2.Tenant.SerializeToString,
        ),
        "DeleteTenant": grpc.unary_unary_rpc_method_handler(
            servicer.DeleteTenant,
            request_deserializer=google_dot_cloud_dot_talent__v4beta1_dot_proto_dot_tenant__service__pb2.DeleteTenantRequest.FromString,
            response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
        ),
        "ListTenants": grpc.unary_unary_rpc_method_handler(
            servicer.ListTenants,
            request_deserializer=google_dot_cloud_dot_talent__v4beta1_dot_proto_dot_tenant__service__pb2.ListTenantsRequest.FromString,
            response_serializer=google_dot_cloud_dot_talent__v4beta1_dot_proto_dot_tenant__service__pb2.ListTenantsResponse.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        "google.cloud.talent.v4beta1.TenantService", rpc_method_handlers
    )
    server.add_generic_rpc_handlers((generic_handler,))
