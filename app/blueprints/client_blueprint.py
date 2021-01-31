from app.blueprints.base_blueprint import (
    Blueprint,
    BaseBlueprint,
    request,
    Security,
    Auth,
)
from app.controllers.client_controller import ClientController

# from flasgger import swag_from

url_prefix = "{}/clients".format(BaseBlueprint.base_url_prefix)
client_blueprint = Blueprint("client", __name__, url_prefix=url_prefix)
client_controller = ClientController(request)

""" CLIENTS """


@client_blueprint.route("/", methods=["GET"])
@Auth.has_permission(["view_clients"])
# @swag_from('documentation/get_all_clients.yml')
def list_clients():
    return client_controller.list_clients()


@client_blueprint.route("/engineers", methods=["GET"])
@Auth.has_permission(["view_clients"])
# @swag_from('documentation/get_all_clients.yml')
def list_client_engineers():
    return client_controller.list_client_engineers()


@client_blueprint.route("/<int:client_id>", methods=["GET"])
@Auth.has_permission(["view_clients"])
# @swag_from('documentation/get_client_by_id.yml')
def get_client(client_id):
    return client_controller.get_client(client_id)


@client_blueprint.route("/", methods=["POST"])
@Security.validator(
    [
        "institution_name|required:string",
        "institution_url|required:string",
        "institution_city|required:string",
        "institution_country|optional:string",
        "institution_size|required:string",
        "status|required:string",
        "start_date|required:date",
    ]
)
@Auth.has_permission(["create_clients"])
# @swag_from('documentation/create_client.yml')
def create_client():
    return client_controller.create_client()


@client_blueprint.route("/<int:client_id>", methods=["PUT", "PATCH"])
@Security.validator(
    [
        "client_id|required:int",
        "institution_name|required:string",
        "institution_url|required:string",
        "institution_city|required:string",
        "institution_country|optional:string",
        "institution_size|required:string",
        "status|required:string",
        "start_date|required:date",
    ]
)
@Auth.has_permission(["update_clients"])
# @swag_from("documentation/update_client.yml")
def update_client(client_id):
    return client_controller.update_client(client_id)


@client_blueprint.route("/<int:client_id>", methods=["DELETE"])
@Auth.has_permission(["delete_clients"])
# @swag_from("documentation/delete_client.yml")
def delete_client(client_id):
    return client_controller.delete_client(client_id)
