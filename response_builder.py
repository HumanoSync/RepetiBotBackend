class JSONRPCResponseBuilder:
    def __init__(self):
        self.response = {
            "jsonrpc": "2.0",
            "result": None,
            "error": None,
            "id": None
        }

    def set_result(self, result):
        self.response["result"] = result
        return self

    def set_error(self, code, message, data=None):
        self.response["error"] = {
            "code": code,
            "message": message,
            "data": data
        }
        self.response["result"] = None  # Si hay error, no debe haber resultado
        return self

    def set_id(self, response_id):
        self.response["id"] = response_id
        return self

    def build(self):
        if self.response["id"] is None:
            raise ValueError("El ID es obligatorio en una respuesta JSON-RPC")
        if self.response["result"] is not None and self.response["error"] is not None:
            raise ValueError("Una respuesta no puede tener ambos, result y error")
        return self.response
