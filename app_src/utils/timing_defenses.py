from datetime import datetime

# Used to prevent time-based attacks on user authentication (more on calc_remaining_time_for_report_error function)
MINIMUM_TIME_FOR_REPORT_ERROR = 3 # In seconds

def calc_remaining_time_for_report_error(request_started_at: datetime) -> int:
    """
        Calculates a time before returning response to client. This is used with MINIMUM_TIME_FOR_REPORT_ERROR to 
        prevent time-based attacks.

        To learn more about time-based attacks, refer to:
        https://ropesec.com/articles/timing-attacks/#:~:text=A%20timing%20attack%20is%20a,the%20password%20of%20a%20user
    """
    now = datetime.now()
    elapsed_time = now - request_started_at

    # If the maximum time was already reached for any reason, do not delay
    if elapsed_time.total_seconds() > MINIMUM_TIME_FOR_REPORT_ERROR:
        return 0

    time_to_sleep = MINIMUM_TIME_FOR_REPORT_ERROR - elapsed_time.total_seconds()
    return time_to_sleep