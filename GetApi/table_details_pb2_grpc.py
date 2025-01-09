# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import table_details_pb2 as table__details__pb2


class TableDetailServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CreateTable = channel.unary_unary(
                '/table_details.TableDetailService/CreateTable',
                request_serializer=table__details__pb2.Table.SerializeToString,
                response_deserializer=table__details__pb2.Table.FromString,
                )
        self.CreateField = channel.unary_unary(
                '/table_details.TableDetailService/CreateField',
                request_serializer=table__details__pb2.Field.SerializeToString,
                response_deserializer=table__details__pb2.Field.FromString,
                )
        self.GetTableById = channel.unary_unary(
                '/table_details.TableDetailService/GetTableById',
                request_serializer=table__details__pb2.TableIdRequest.SerializeToString,
                response_deserializer=table__details__pb2.Table.FromString,
                )


class TableDetailServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def CreateTable(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateField(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetTableById(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_TableDetailServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'CreateTable': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateTable,
                    request_deserializer=table__details__pb2.Table.FromString,
                    response_serializer=table__details__pb2.Table.SerializeToString,
            ),
            'CreateField': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateField,
                    request_deserializer=table__details__pb2.Field.FromString,
                    response_serializer=table__details__pb2.Field.SerializeToString,
            ),
            'GetTableById': grpc.unary_unary_rpc_method_handler(
                    servicer.GetTableById,
                    request_deserializer=table__details__pb2.TableIdRequest.FromString,
                    response_serializer=table__details__pb2.Table.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'table_details.TableDetailService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class TableDetailService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def CreateTable(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/table_details.TableDetailService/CreateTable',
            table__details__pb2.Table.SerializeToString,
            table__details__pb2.Table.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CreateField(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/table_details.TableDetailService/CreateField',
            table__details__pb2.Field.SerializeToString,
            table__details__pb2.Field.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetTableById(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/table_details.TableDetailService/GetTableById',
            table__details__pb2.TableIdRequest.SerializeToString,
            table__details__pb2.Table.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class ApiMetaServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CreateApiMeta = channel.unary_unary(
                '/table_details.ApiMetaService/CreateApiMeta',
                request_serializer=table__details__pb2.ApiMeta.SerializeToString,
                response_deserializer=table__details__pb2.ApiMeta.FromString,
                )
        self.AddApiTable = channel.unary_unary(
                '/table_details.ApiMetaService/AddApiTable',
                request_serializer=table__details__pb2.AddApiDetail.SerializeToString,
                response_deserializer=table__details__pb2.AddApiDetail.FromString,
                )
        self.AddApiField = channel.unary_unary(
                '/table_details.ApiMetaService/AddApiField',
                request_serializer=table__details__pb2.AddApiDetail.SerializeToString,
                response_deserializer=table__details__pb2.AddApiDetail.FromString,
                )
        self.GetApiDetailById = channel.unary_unary(
                '/table_details.ApiMetaService/GetApiDetailById',
                request_serializer=table__details__pb2.ApiMetaRequest.SerializeToString,
                response_deserializer=table__details__pb2.ApiMeta.FromString,
                )


class ApiMetaServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def CreateApiMeta(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AddApiTable(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AddApiField(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetApiDetailById(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ApiMetaServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'CreateApiMeta': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateApiMeta,
                    request_deserializer=table__details__pb2.ApiMeta.FromString,
                    response_serializer=table__details__pb2.ApiMeta.SerializeToString,
            ),
            'AddApiTable': grpc.unary_unary_rpc_method_handler(
                    servicer.AddApiTable,
                    request_deserializer=table__details__pb2.AddApiDetail.FromString,
                    response_serializer=table__details__pb2.AddApiDetail.SerializeToString,
            ),
            'AddApiField': grpc.unary_unary_rpc_method_handler(
                    servicer.AddApiField,
                    request_deserializer=table__details__pb2.AddApiDetail.FromString,
                    response_serializer=table__details__pb2.AddApiDetail.SerializeToString,
            ),
            'GetApiDetailById': grpc.unary_unary_rpc_method_handler(
                    servicer.GetApiDetailById,
                    request_deserializer=table__details__pb2.ApiMetaRequest.FromString,
                    response_serializer=table__details__pb2.ApiMeta.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'table_details.ApiMetaService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ApiMetaService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def CreateApiMeta(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/table_details.ApiMetaService/CreateApiMeta',
            table__details__pb2.ApiMeta.SerializeToString,
            table__details__pb2.ApiMeta.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def AddApiTable(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/table_details.ApiMetaService/AddApiTable',
            table__details__pb2.AddApiDetail.SerializeToString,
            table__details__pb2.AddApiDetail.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def AddApiField(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/table_details.ApiMetaService/AddApiField',
            table__details__pb2.AddApiDetail.SerializeToString,
            table__details__pb2.AddApiDetail.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetApiDetailById(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/table_details.ApiMetaService/GetApiDetailById',
            table__details__pb2.ApiMetaRequest.SerializeToString,
            table__details__pb2.ApiMeta.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)