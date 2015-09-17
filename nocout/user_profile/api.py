from rest_framework.response import Response
from rest_framework.views import APIView
from user_profile.models import UserProfile
from nocout.settings import ISOLATED_NODE
from django.db.models import Max


class UserSoftDeleteDisplayData(APIView):
    """
    Generate display data for user soft deletion request.

    Allow: GET, HEAD, OPTIONS

    URL: "http://127.0.0.1:8000/api/user_soft_delete_display_data/4/"
    """
    def get(self, request, value):
        """
        Processing API request.

        Args:
            value (int): Selected user ID.

        Returns:
            result (dict): Dictionary containing device information.
                           For e.g.,
                                {
                                    "message": "Successfully render form.",
                                    "data": {
                                        "meta": "",
                                        "objects": {
                                            "form_type": "user",
                                            "eligible": [
                                                {
                                                    "value": "gisoperator",
                                                    "key": 3
                                                },
                                                {
                                                    "value": "gisadmin",
                                                    "key": 10
                                                }
                                            ],
                                            "form_title": "user",
                                            "id": 4,
                                            "name": "gisviewer"
                                        }
                                    },
                                    "success": 1
                                }
        """
        user = UserProfile.objects.get(id=value)

        result = dict()
        result['data'] = {}
        result['success'] = 0
        result['message'] = "Failed to render form correctly."
        result['data']['meta'] = ''
        result['data']['objects'] = {}
        result['data']['objects']['form_type'] = 'user'
        result['data']['objects']['form_title'] = 'user'
        result['data']['objects']['id'] = user.id
        result['data']['objects']['name'] = user.username

        # List of eligible parents.
        result['data']['objects']['eligible'] = []

        # Get immediate children of the user.
        user_children = user.get_children()

        if user_children:
            user_parent = user.parent

            if user_parent:
                # Get immediate children of the user's parent.
                user_parent_children = user_parent.get_children()

                # Exclude 'user' from list of eligible parent.
                user_parent_children = set(user_parent_children) - {user}

                if len(user_parent_children) > 0:
                    for e_user in user_parent_children:
                        e_dict = dict()
                        e_dict['key'] = e_user.id
                        e_dict['value'] = e_user.username
                        result['data']['objects']['eligible'].append(e_dict)
                else:
                    # If 'user_parent_children' is empty then the user's parent will
                    # be assigned as a default parent to the user's children.
                    result['data']['objects']['eligible'].append({'key': user_parent.id, 'value': user_parent.username})

        result['success'] = 1
        result['message'] = "Successfully render form."

        return Response(result)


class UserSoftDelete(APIView):
    """
    Soft delete user i.e. not deleting user from database, it just set
    it's 'is_deleted' bit to 1, remove it's relationship with any other user
    & make some other user parent of associated user's.

    Allow: GET, HEAD, OPTIONS

    URL: "http://127.0.0.1:8000/api/user_soft_delete/4/5/"
    """
    def get(self, request, value, new_parent_id):
        """
        Processing API request.

        Args:
            user_id (unicode): Selected user ID.
            new_parent_id (unicode): New parent/manager for child user's of user which need to be deleted.

        Returns:
            result (str): Result which needs to be returned.
                           for e.g.
                                {
                                    "message": "User successfully deleted.",
                                    "data": {
                                        "meta": "",
                                        "objects": {
                                            "name": "vasu",
                                            "id": "11"
                                        }
                                    },
                                    "success": 1
                                }
        """
        user = UserProfile.objects.get(id=value)

        result = dict()
        result['data'] = {}
        result['success'] = 0
        result['message'] = "No data exists."
        result['data']['meta'] = ''
        result['data']['objects'] = {}
        result['data']['objects']['id'] = value
        result['data']['objects']['name'] = user.username

        try:
            new_parent_id = int(new_parent_id)
        except Exception, e:
            new_parent_id = 0
            pass

        if new_parent_id:
            new_parent = UserProfile.objects.get(id=new_parent_id)

            # Get immediate children of the user.
            user_children = user.get_children()

            for user_child in user_children:
                user_child.move_to(new_parent)

        max_tree_id = UserProfile.objects.aggregate(Max('tree_id'))['tree_id__max']
        user.tree_id = max_tree_id + 1
        user.is_deleted = 1
        user.lft = ISOLATED_NODE.lft
        user.rght = ISOLATED_NODE.rght
        user.level = ISOLATED_NODE.level
        user.parent = None
        user.save()

        # Rebuilds whole tree in database using `parent` link.
        UserProfile._default_manager.rebuild()

        result['success'] = 1
        result['message'] = "User successfully deleted."

        return Response(result)


class RestoreUser(APIView):
    """
    Restore user to user's inventory from archived inventory.

    Allow: GET, HEAD, OPTIONS

    URL: "http://127.0.0.1:8000/api/restore_user/11/"
    """
    def get(self, request, value):
        """
        Processing API request.

        Args:
            value (int): Selected user ID.

        Returns:
            result (str): Result which needs to be returned.
                           for e.g.
                                {
                                    "message": "User successfully restored.",
                                    "data": {
                                        "meta": "",
                                        "objects": {
                                            "id": "12"
                                        }
                                    },
                                    "success": 1
                                }
        """
        UserProfile.objects.filter(id=value).update(**{'is_deleted': 0})

        result = dict()
        result['data'] = {}
        result['success'] = 1
        result['message'] = "User successfully restored."
        result['data']['meta'] = ''
        result['data']['objects'] = {}
        result['data']['objects']['id'] = value

        return Response(result)


class DeleteUser(APIView):
    """
    Delete user from user inventory. This action permanently delete user from database.

    Allow: GET, HEAD, OPTIONS

    URL: "http://127.0.0.1:8000/api/delete_user/11/"
    """
    def get(self, request, value):
        """
        Processing API request.

        Args:
            value (int): Selected user ID.

        Returns:
            result (str): Result which needs to be returned.
                           for e.g. {
                                        "result": {
                                            "message": "User Successfully Deleted.",
                                            "data": {},
                                            "success": 1
                                        }
                                    }
        """
        UserProfile.objects.filter(id=value).delete()

        result = dict()
        result['data'] = {}
        result['success'] = 1
        result['message'] = "User successfully deleted."

        return Response(result)