# Import ALL blueprints here
from .index import index_views
from .auth import auth_views
from .application import application_views
from .employer import employer_views
# If you have these, also include:
# from .position import position_views
from .shortlist import shortlist_views
# from .user import user_views

# Add all views to this list so main.py can register them
views = [
    index_views,
    auth_views,
    application_views,
    employer_views,
    # position_views,
    shortlist_views,
    # user_views,
]
