class JSONRPCRequestBuilder:
    def __init__(self):
        self.request = {
            "jsonrpc": "2.0",
            "method": None,
            "params": None,
            "id": None
        }

    def set_method(self, method):
        self.request["method"] = method
        return self

    def set_params(self, params):
        self.request["params"] = params
        return self

    def set_id(self, request_id):
        self.request["id"] = request_id
        return self

    def build(self):
        if self.request["method"] is None:
            raise ValueError("El método es obligatorio en una solicitud JSON-RPC")
        return self.request
