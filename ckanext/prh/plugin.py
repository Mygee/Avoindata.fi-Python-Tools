from ckan import plugins
from .commands import prh_tools

class PRHTools(plugins.SingletonPlugin):
    plugins.implements(plugins.IClick)

    # IClick

    def get_commands(self):
        return [prh_tools]
