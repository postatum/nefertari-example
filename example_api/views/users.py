import logging

from nefertari.view import BaseView

from example_api.models import User, Profile


log = logging.getLogger(__name__)


class UsersView(BaseView):
    Model = User

    def index(self):
        return self.Model.get_collection(**self._query_params)

    def show(self, **kwargs):
        return self.Model.get_item(
            username=kwargs.pop('user_username'),
            __raise_on_empty=True)

    def create(self):
        item = self.Model(**self._json_params)
        return item.save(self.request)

    def update(self, **kwargs):
        item = self.Model.get_item(
            username=kwargs.pop('user_username'), **kwargs)
        return item.update(self._json_params, self.request)

    def replace(self, **kwargs):
        return self.update(**kwargs)

    def delete(self, **kwargs):
        item = self.Model.get_item(
            username=kwargs.pop('user_username'), **kwargs)
        item.delete(self.request)

    def delete_many(self):
        items = self.Model.get_collection(**self._query_params)
        return self.Model._delete_many(items, self.request)

    def update_many(self):
        items = self.Model.get_collection(**self._query_params)
        return self.Model._update_many(
            items, self._json_params, self.request)


class UserProfileView(BaseView):
    Model = Profile

    def show(self, **kwargs):
        user = User.get_item(
            username=kwargs.pop('user_username'), **kwargs)
        return user.profile

    def create(self, **kwargs):
        obj = User.get_item(
            username=kwargs.pop('user_username'), **kwargs)
        profile = self.Model(**self._json_params)
        profile = profile.save()
        obj.update({'profile': profile})
        return obj.profile

    def update(self, **kwargs):
        user = User.get_item(
            username=kwargs.pop('user_username'), **kwargs)
        return user.profile.update(self._json_params)

    def replace(self, **kwargs):
        return self.update(**kwargs)
