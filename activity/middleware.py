from channels.db import database_sync_to_async
from urllib.parse import parse_qs
import logging

logger = logging.getLogger(__name__)

@database_sync_to_async
def get_user_from_token(token_key):
    from django.contrib.auth.models import AnonymousUser
    from rest_framework.authtoken.models import Token
    
    try:
        token = Token.objects.select_related('user').get(key=token_key)
        user = token.user
        if user.is_active:
            return user
        else:
            return AnonymousUser()
    except Token.DoesNotExist:
        return AnonymousUser()
    except Exception as e:
        logger.error(f"Error getting user from token: {e}")
        return AnonymousUser()

class TokenAuthMiddleware:
    """
    Custom middleware that authenticates WebSocket connections using token from URL params
    """
    
    def __init__(self, inner):
        self.inner = inner
    
    async def __call__(self, scope, receive, send):
        # Only process WebSocket connections
        if scope["type"] != "websocket":
            return await self.inner(scope, receive, send)
        
        # Get token from query string
        query_string = scope.get("query_string", b"").decode()
        query_params = parse_qs(query_string)
        token_key = query_params.get("token", [None])[0]
        
        logger.info(f"WebSocket auth: query_string={query_string}, token_key={token_key}")
        
        if token_key:
            user = await get_user_from_token(token_key)
            scope["user"] = user
            logger.info(f"WebSocket auth: token found, user={user.username if user.is_authenticated else 'anonymous'}, is_authenticated={user.is_authenticated}")
        else:
            from django.contrib.auth.models import AnonymousUser
            scope["user"] = AnonymousUser()
            logger.info("WebSocket auth: no token found")
        
        return await self.inner(scope, receive, send)