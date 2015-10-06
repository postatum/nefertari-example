import logging
from random import random

from nefertari.view import BaseView
from nefertari_guards.view import ACLFilterViewMixin
from nefertari_guards import engine as guards_engine
from pyramid.security import Allow

from example_api.models import Story

log = logging.getLogger(__name__)


class ArbitraryObject(object):
    def __init__(self, *args, **kwargs):
        self.attr = random()

    def to_dict(self, *args, **kwargs):
        return dict(attr=self.attr)


class StoriesView(ACLFilterViewMixin, BaseView):
    Model = Story

    def index(self):
        return self.get_collection_es()

    def show(self, **kwargs):
        return self.context

    def create(self):
        if 'owner' not in self._json_params:
            self._json_params['owner'] = self.request.user
        if not self._json_params.get('_acl'):
            self._json_params['_acl'] = []
        acl = guards_engine.ACLField.stringify_acl([
            (Allow, self.request.user.username, 'update')])
        self._json_params['_acl'] = acl + self._json_params['_acl']
        story = self.Model(**self._json_params)
        story.arbitrary_object = ArbitraryObject()
        return story.save(self.request)

    def update(self, **kwargs):
        story = self.Model.get_item(
            id=kwargs.pop('story_id'), **kwargs)
        return story.update(self._json_params, self.request)

    def replace(self, **kwargs):
        return self.update(**kwargs)

    def delete(self, **kwargs):
        story = self.Model.get_item(
            id=kwargs.pop('story_id'), **kwargs)
        story.delete(self.request)

    def delete_many(self):
        es_stories = self.get_collection_es()
        stories = self.Model.filter_objects(es_stories)
        return self.Model._delete_many(stories, self.request)

    def update_many(self):
        es_stories = self.get_collection_es()
        stories = self.Model.filter_objects(es_stories)
        return self.Model._update_many(
            stories, self._json_params, self.request)
