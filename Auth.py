from functools import wraps

# add userID of everyone you want to authenticate
# if you want to find your userID just send '/photo' or '/text' to the bot
# and the python script will print: "Unauthorized access denied for (your user ID)."
LIST_OF_ADMINS = []

#to use restricted, just put @restricted right above the function you want to be restricted

def restricted(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in LIST_OF_ADMINS:
            print("Unauthorized access denied for {}.".format(user_id))
            return
        return func(update, context, *args, **kwargs)
    return wrapped
