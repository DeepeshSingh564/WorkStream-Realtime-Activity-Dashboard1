"""
Signals are intentionally not used for WebSocket broadcasting.

Reason:
- Broadcasting activity updates requires access to the authenticated user
- Django signals are implicit and harder to debug
- Broadcasting is handled explicitly in the API view (perform_create)

This file is kept for future extensibility:
- background tasks
- analytics hooks
- audit logging
"""
