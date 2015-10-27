from organization.models import Organization


def in_group(user=None, group_names=None):
    """
    Check whether user exists in given group or not.
    :param user: User object
    :return: True/False
    """
    if user and group_names:
        user_groups = set([group.name.lower() for group in user.groups.all()])
        if isinstance(group_names, list):
            if set(user_groups).issubset(set(group_names)):
                return True
            else:
                return False
        else:
            if group_names.lower() in user_groups:
                return True
            else:
                return False
    else:
        return False


def get_user_organizations(user):
    """
    If the user role is admin then append its descendants organization as well, otherwise not

    :params self_object:
    :return organization_list:
    """
    if user.is_superuser:
        return Organization.objects.all()

    logged_in_user = user.userprofile

    if in_group(user, ['admin', 'operator', 'viewer']):
        organizations = logged_in_user.organization.get_descendants(include_self=True)
    else:
        organizations = Organization.objects.filter(id=logged_in_user.organization.id)

    return organizations

def get_child_users(user=None, limit='org'):
    if user:
        # Get organizations user associated or linked with.
        link_org = get_user_organizations(user)
        child_users = user.userprofile.get_children()
        if limit == 'org':
            # Get child users existing within user's organizations.
            child_users = child_users.filter(organization__in=link_org)

        return child_users
