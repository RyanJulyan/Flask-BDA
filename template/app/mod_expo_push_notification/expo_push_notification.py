
# Import the database object from the main app module
from app import app

# Import g for organisation
from flask import g

# Import Json
import json

from exponent_server_sdk import (
    DeviceNotRegisteredError,
    PushClient,
    PushMessage,
    PushServerError,
    PushTicketError,
)

from notifications.models import PushToken

# Basic arguments. You should extend this function with the push features you
# want to use, or simply pass in a `PushMessage` object.
def send_push_message(token, message, extra=None):
    try:
        response = PushClient().publish(
            PushMessage(to=token,
                        body=message,
                        data=extra))
    except PushServerError as exc:
        # Encountered some likely formatting/validation error.
        extra_data={
            'token': token,
            'message': message,
            'extra': extra,
            'errors': exc.errors,
            'response_data': exc.response_data,
        }
        app.logger.warning('PushServerError for organisation: ' + g.organization + '. Event details: ' + json.dumps(extra_data))
        
        raise
    except (ConnectionError) as exc:
        # Encountered some Connection or HTTP error - retry a few times in
        # case it is transient.
        extra_data={
            'token': token,
            'message': message,
            'extra': extra
        }
        app.logger.warning('ConnectionError for organisation: ' + g.organization + '. Event details: ' + json.dumps(extra_data))

        raise self.retry(exc=exc)

    try:
        # We got a response back, but we don't know whether it's an error yet.
        # This call raises errors so we can handle them with normal exception
        # flows.
        response.validate_response()
    except DeviceNotRegisteredError:
        extra_data={
            'token': token,
            'message': message,
            'extra': extra
        }
        app.logger.warning('DeviceNotRegisteredError for organisation: ' + g.organization + '. Event details: ' + json.dumps(extra_data))
        # Mark the push token as inactive
        PushToken.objects.filter(token=token).update(active=False)
    except PushTicketError as exc:
        # Encountered some other per-notification error.
        extra_data={
            'token': token,
            'message': message,
            'extra': extra,
            'push_response': exc.push_response._asdict(),
        }
        app.logger.warning('PushTicketError for organisation: ' + g.organization + '. Event details: ' + json.dumps(extra_data))

        raise self.retry(exc=exc)