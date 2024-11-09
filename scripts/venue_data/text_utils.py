import tiktoken
from typing import List
from datetime import datetime, timedelta

# OpenAI's context window size for gpt-3.5-turbo
TOKEN_LIMIT = 4000 

def chunk_message(message: str) -> List[str]:
    """
    Split a message into chunks that fit within OpenAI's token limit.
    
    Args:
        message: The text content to be split into chunks
        
    Returns:
        A list of text chunks, each within OpenAI's token limit
    """
    encoding = tiktoken.get_encoding("cl100k_base")
    tokenized_str = encoding.encode(message)
    
    if len(tokenized_str) > TOKEN_LIMIT:
        return [
            encoding.decode(tokenized_str[i:i + TOKEN_LIMIT]) 
            for i in range(0, len(tokenized_str), TOKEN_LIMIT)
        ]
    
    return [message] 

def get_next_months(num_months: int = 3) -> List[str]:
    """Generate a list of month strings for the current and next few months."""
    months = []
    current_date = datetime.now()
    
    for i in range(num_months):
        next_date = current_date + timedelta(days=30*i)
        month_str = next_date.strftime("%B_%Y").lower()
        months.append(month_str)
    
    return months 