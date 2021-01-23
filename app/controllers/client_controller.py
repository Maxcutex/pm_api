from app.controllers.base_controller import BaseController


class ClientController(BaseController):
    def __init__(self, request):
        BaseController.__init__(self, request)
