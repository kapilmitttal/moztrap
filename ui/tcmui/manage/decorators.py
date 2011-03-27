from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect

from ..core import errors



def handle_actions(list_model, allowed_actions, fall_through=False):
    """
    View decorator that handles any POST keys named "action-method", where
    "method" must be in ``allowed_actions``. The value of the key should be an
    ID of ``list_model``, and "method" will be called on it, with any errors
    handled.

    By default, any "POST" request will be redirected back to the same URL. If
    ``fall_through`` is set to True, the redirect will only occur if an action
    was found in the POST data (allowing this decorator to be used with views
    that also do normal form handling.)

    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.method == "POST":
                action_taken = False
                actions = [(k, v) for k, v in request.POST.iteritems()
                           if k.startswith("action-")]
                if actions:
                    action, obj_id = actions[0]
                    action = action[len("action-"):]
                    if action in allowed_actions:
                        obj = list_model.get_by_id(obj_id, auth=request.auth)
                        try:
                            getattr(obj, action)()
                        except obj.Conflict, e:
                            messages.error(
                                request, errors.error_message(e, unicode(obj)))
                        action_taken = True
                if action_taken or not fall_through:
                    return redirect(request.get_full_path())
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator