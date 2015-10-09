import logging

from nefertari.view import BaseView

from example_api.models import Story

log = logging.getLogger(__name__)


class StoriesView(BaseView):
    Model = Story

    def index(self):
        return self.Model.get_collection(**self._query_params)

    def show(self, **kwargs):
        return self.Model.get_item(
            id=kwargs.pop('story_id'),
            __raise_on_empty=True)

    def create(self):
        item = self.Model(**self._json_params)
        return item.save(self.request)

    def update(self, **kwargs):
        item = self.Model.get_item(
            id=kwargs.pop('story_id'), **kwargs)
        return item.update(self._json_params, self.request)

    def replace(self, **kwargs):
        return self.update(**kwargs)

    def delete(self, **kwargs):
        item = self.Model.get_item(
            id=kwargs.pop('story_id'), **kwargs)
        item.delete(self.request)

    def delete_many(self):
        items = self.Model.get_collection(**self._query_params)
        return self.Model._delete_many(items, self.request)

    def update_many(self):
        items = self.Model.get_collection(**self._query_params)
        return self.Model._update_many(
            items, self._json_params, self.request)
