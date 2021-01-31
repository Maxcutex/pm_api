from app.repositories.base_repo import BaseRepo
from app.models.client import Client


class ClientRepo(BaseRepo):
    def __init__(self):
        BaseRepo.__init__(self, Client)

    def new_client(
        self,
        institution_name,
        institution_url,
        institution_city,
        institution_country,
        institution_size,
        status,
        start_date,
        is_deleted=False,
    ):
        client = Client(
            institution_name=institution_name,
            institution_url=institution_url,
            institution_city=institution_city,
            institution_country=institution_country,
            institution_size=institution_size,
            status=status,
            start_date=start_date,
            is_deleted=is_deleted,
        )

        client.save()
        return client
