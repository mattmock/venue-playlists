import tiktoken
from typing import List
from datetime import datetime, timedelta

# OpenAI's context window size for gpt-3.5-turbo
TOKEN_LIMIT = 4000 

def chunk_message(text: str, max_length: int = 2000) -> List[str]:
    """Split text into chunks of max_length, trying to break at sentence boundaries."""
    if not text:
        return []
        
    # If text is shorter than max_length, return it as is
    if len(text) <= max_length:
        return [text]
    
    chunks = []
    while text:
        if len(text) <= max_length:
            chunks.append(text)
            break
            
        # Try to find a sentence break near the max_length
        split_point = text.rfind('. ', 0, max_length)
        
        if split_point == -1:
            # No sentence break found, try other punctuation
            for punct in ['! ', '? ', '\n', '. ', ', ']:
                split_point = text.rfind(punct, 0, max_length)
                if split_point != -1:
                    break
            
            if split_point == -1:
                # No good break found, force split at max_length
                split_point = max_length
        else:
            split_point += 2  # Include the period and space
        
        chunks.append(text[:split_point].strip())
        text = text[split_point:].strip()
    
    return chunks

def get_next_months(num_months: int = 3) -> List[str]:
    """Get list of next N months in format 'Month_YYYY'."""
    months = []
    current_date = datetime.now()
    
    for i in range(num_months):
        if i == 0:
            # Include current month
            month_date = current_date
        else:
            # Add one month
            month_date = current_date.replace(day=1) + timedelta(days=32 * i)
            # Reset to first of month
            month_date = month_date.replace(day=1)
        
        month_str = month_date.strftime("%B_%Y")
        months.append(month_str)
    
    return months 