"""Logging utilities"""
import logging
from functools import wraps

logger = logging.getLogger(__name__)

def log_errors(func):
    """Decorator to log errors"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}", exc_info=True)
            raise
    return wrapper

def log_order_event(order_id, event, details=None):
    """Log order-related events"""
    logger.info(f"Order {order_id} - {event}: {details or ''}")

def log_payment_event(order_id, status, amount=None):
    """Log payment events"""
    logger.info(f"Payment for Order {order_id} - Status: {status}, Amount: {amount}")
