# utils/helpers.py

"""
Helpers Module

This module provides utility functions used across the simulation project:
  - format_event(event): Formats an event message by prepending a timestamp.
  - batch_messages(messages, batch_size): Splits a list of messages into smaller batches.
  
These functions support logging and efficient LLM interactions.
"""

from datetime import datetime
from typing import List

def format_event(event: str) -> str:
    """
    Format an event string by adding a timestamp.
    
    Args:
        event (str): The event message.
    
    Returns:
        str: The event message prefixed with the current timestamp.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"[{timestamp}] {event}"

def batch_messages(messages: List[str], batch_size: int) -> List[List[str]]:
    """
    Batch a list of messages into sublists of a specified size.
    
    Args:
        messages (List[str]): A list of message strings.
        batch_size (int): Number of messages per batch.
    
    Returns:
        List[List[str]]: A list containing sublists (batches) of messages.
    """
    return [messages[i:i + batch_size] for i in range(0, len(messages), batch_size)]
