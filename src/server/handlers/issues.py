from server.handlers.base import ListResource
from server.models import Issue


class IssueListResource(ListResource):
    @property
    def resource(self):
        return Issue

    @property
    def key(self):
        return "issues"

