from app.controllers.base_controller import BaseController


class ClientController(BaseController):
    def __init__(self, request):
        BaseController.__init__(self, request)

    def list_clients(self):
        clients = self.client_repo.get_unpaginated()

        client_list = [client.serialize() for client in clients.items]
        return self.handle_response("OK", payload={"clients": client_list})

    def list_client_engineers(self, client_id):
        engineers = self.user_client_repo.get_unpaginated(client_id=client_id)

        engineer_list = [engineer.serialize() for engineer in engineers]
        return self.handle_response("OK", payload={"clients": engineer_list})

    def get_client(self, client_id):
        client = self.client_repo.get(client_id)
        if client:
            return self.handle_response("OK", payload={"client": client.serialize()})
        return self.handle_response("Invalid or Missing client_id", status_code=400)

    def create_client(self):
        (
            institution_name,
            institution_url,
            institution_city,
            institution_country,
            institution_size,
            status,
            start_date,
        ) = self.request_params(
            "institution_name",
            "institution_url",
            "institution_city",
            "institution_country",
            "institution_size",
            "status",
            "start_date",
        )
        client1 = self.client_repo.find_first(institution_name=institution_name)

        if not client1:
            try:
                client = self.client_repo.new_client(
                    institution_name=institution_name,
                    institution_url=institution_url,
                    institution_city=institution_city,
                    institution_country=institution_country,
                    institution_size=institution_size,
                    status=status,
                    start_date=start_date,
                )
                return self.handle_response(
                    "OK", payload={"client": client.serialize()}, status_code=201
                )
            except Exception as e:
                return self.handle_response(
                    "Error processing: " + str(e), status_code=400
                )

        return self.handle_response(
            "Client with this name already exists", status_code=400
        )

    def update_client(self, client_id):
        (
            client_id,
            institution_name,
            institution_url,
            institution_city,
            institution_country,
            institution_size,
            status,
            start_date,
        ) = self.request_params(
            "client_id",
            "institution_name",
            "institution_url",
            "institution_city",
            "institution_country",
            "institution_size",
            "status",
            "start_date",
        )
        client = self.client_repo.get(client_id)
        if client:
            updates = {}
            if institution_name:
                client1 = self.client_repo.find_first(institution_name=institution_name)
                if client1:
                    return self.handle_response(
                        "Client with this name already exists", status_code=400
                    )
                updates["institution_name"] = institution_name
                updates["institution_url"] = institution_url
                updates["institution_city"] = institution_city
                updates["institution_country"] = institution_country
                updates["institution_size"] = institution_size
                updates["status"] = status
                updates["start_date"] = start_date

            client = self.client_repo.update(client, **updates)
            return self.handle_response("OK", payload={"client": client.serialize()})
        return self.handle_response(
            "Invalid or incorrect client_id provided", status_code=400
        )

    def delete_client(self, client_id):
        client = self.client_repo.get(client_id)
        if client:
            updates = {}
            updates["is_deleted"] = True
            self.client_repo.update(client, **updates)
            return self.handle_response("client deleted", payload={"status": "success"})
        return self.handle_response(
            "Invalid or incorrect client_id provided", status_code=404
        )
