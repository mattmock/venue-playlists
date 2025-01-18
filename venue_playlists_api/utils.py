"""API utility functions."""
from datetime import datetime, timedelta

def get_next_months(num_months: int = 3) -> list[str]:
    """Get a list of the next few months in the format 'Month_YYYY'.
    
    Args:
        num_months: Number of months to return, including current month
        
    Returns:
        List of month strings in format 'Month_YYYY'
    """
    months = []
    current_date = datetime.now()
    
    for i in range(num_months):
        if i > 0:
            # Add one month
            if current_date.month == 12:
                current_date = current_date.replace(year=current_date.year + 1, month=1)
            else:
                current_date = current_date.replace(month=current_date.month + 1)
        
        month_str = f"{current_date.strftime('%B')}_{current_date.year}"
        months.append(month_str)
    
    return months 