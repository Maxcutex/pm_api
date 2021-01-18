from app.repositories.base_repo import BaseRepo
from app.models.user_project import UserProject


class UserProjectRepo(BaseRepo):
    def __init__(self):
        BaseRepo.__init__(self, UserProject)

    def new_user_project(
        self,
        user_id,
        project_name,
        project_url,
        project_description,
        start_date,
        end_date,
        is_current,
    ):
        user_project = UserProject(
            project_name=project_name,
            project_url=project_url,
            project_description=project_description,
            start_date=start_date,
            end_date=end_date,
            user_id=user_id,
            is_current=is_current,
        )
        user_project.save()
        return user_project
