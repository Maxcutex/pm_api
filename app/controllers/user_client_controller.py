from app.controllers.base_controller import BaseController


class UserClientController(BaseController):
    def __init__(self, request):
        BaseController.__init__(self, request)
