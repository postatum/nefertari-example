from pkg_resources import get_distribution
import logging

from pyramid.config import Configurator

import nefertari
from nefertari.tweens import enable_selfalias
from nefertari.utils import dictset

APP_NAME = __package__.split('.')[0]
_DIST = get_distribution(APP_NAME)
PROJECTDIR = _DIST.location
__version__ = _DIST.version

log = logging.getLogger(__name__)

Settings = dictset()


def bootstrap(config):
    Settings.update(config.registry.settings)
    Settings[APP_NAME + '.__version__'] = __version__
    Settings[nefertari.APP_NAME+'.__version__'] = nefertari.__version__

    config.include('nefertari')

    root = config.get_root_resource()

    config.include('example_api.models')
    # config.include('nefertari.view')
    config.include('nefertari.json_httpexceptions')

    enable_selfalias(config, 'user_username')

    if Settings.asbool('enable_get_tunneling'):
        config.add_tween('nefertari.tweens.get_tunneling')

    if Settings.asbool('cors.enable'):
        config.add_tween('nefertari.tweens.cors')

    if Settings.asbool('ssl_middleware.enable'):
        config.add_tween('nefertari.tweens.ssl')

    if Settings.asbool('request_timing.enable'):
        config.add_tween('nefertari.tweens.request_timing')


def main(global_config, **settings):
    Settings.update(settings)
    Settings.update(global_config)
    config = Configurator(
        settings=settings,
    )

    config.include('nefertari.engine')
    config.include(includeme)

    from nefertari.engine import setup_database
    setup_database(config)
    config.commit()

    return config.make_wsgi_app()


def includeme(config):
    log.info("%s %s" % (APP_NAME, __version__))
    bootstrap(config)
    config.scan(package='example_api.views')
    create_resources(config)


def create_resources(config):
    root = config.get_root_resource()

    user = root.add(
        'user', 'users',
        id_name='user_username')

    user.add('profile',
             view='example_api.views.users.UserProfileView')
    root.add(
        'story', 'stories',
        id_name='story_id')
