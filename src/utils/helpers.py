"""
Helper utilities for Policy Navigator Agent
"""
import logging
from typing import Optional, Any, Dict
import requests
from functools import wraps
import time

def setup_logger(name: str, log_file: str = None, level: str = "INFO") -> logging.Logger:
    """
    Setup logger with file and console handlers
    
    Args:
        name: Logger name
        log_file: Path to log file (optional)
        level: Logging level
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level))
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, level))
    console_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)
    
    # File handler
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(getattr(logging, level))
        file_handler.setFormatter(console_format)
        logger.addHandler(file_handler)
    
    return logger


def safe_api_call(api_function):
    """
    Decorator for API calls with error handling and retry logic
    
    Args:
        api_function: Function to wrap
    
    Returns:
        Wrapped function with error handling
    """
    @wraps(api_function)
    def wrapper(*args, **kwargs) -> Optional[Dict[str, Any]]:
        max_retries = kwargs.pop('max_retries', 3)
        retry_delay = kwargs.pop('retry_delay', 1)
        
        logger = logging.getLogger(api_function.__module__)
        
        for attempt in range(max_retries):
            try:
                result = api_function(*args, **kwargs)
                logger.info(f"API call successful: {api_function.__name__}")
                return result
            except requests.exceptions.Timeout as e:
                logger.warning(f"Timeout on attempt {attempt + 1}/{max_retries}: {e}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay * (attempt + 1))
                else:
                    return {"error": "Timeout", "details": str(e)}
            except requests.exceptions.RequestException as e:
                logger.error(f"API request failed: {e}")
                return {"error": "API unavailable", "details": str(e)}
            except Exception as e:
                logger.error(f"Unexpected error in {api_function.__name__}: {e}")
                return {"error": "Internal error", "details": str(e)}
        
        return {"error": "Max retries exceeded"}
    
    return wrapper


def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 100) -> list[str]:
    """
    Split text into overlapping chunks
    
    Args:
        text: Text to chunk
        chunk_size: Maximum chunk size in characters
        overlap: Overlap between chunks
    
    Returns:
        List of text chunks
    """
    if len(text) <= chunk_size:
        return [text]
    
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        
        # Try to break at sentence boundary
        if end < len(text):
            # Look for period, question mark, or exclamation
            for punct in ['. ', '? ', '! ', '\n\n']:
                punct_pos = text.rfind(punct, start, end)
                if punct_pos != -1:
                    end = punct_pos + len(punct)
                    break
        
        chunks.append(text[start:end].strip())
        start = end - overlap if end < len(text) else end
    
    return chunks


def format_policy_response(data: Dict[str, Any]) -> str:
    """
    Format policy data into readable response
    
    Args:
        data: Policy data dictionary
    
    Returns:
        Formatted string
    """
    if 'error' in data:
        return f"Error: {data['error']}\nDetails: {data.get('details', 'N/A')}"
    
    formatted = []
    
    if 'title' in data:
        formatted.append(f"**{data['title']}**\n")
    
    if 'status' in data:
        formatted.append(f"Status: {data['status']}")
    
    if 'publication_date' in data:
        formatted.append(f"Publication Date: {data['publication_date']}")
    
    if 'summary' in data:
        formatted.append(f"\nSummary:\n{data['summary']}")
    
    if 'source' in data:
        formatted.append(f"\nSource: {data['source']}")
    
    if 'url' in data:
        formatted.append(f"Link: {data['url']}")
    
    return '\n'.join(formatted)


def validate_env_vars(*required_vars: str) -> tuple[bool, list[str]]:
    """
    Validate that required environment variables are set
    
    Args:
        *required_vars: Variable names to check
    
    Returns:
        Tuple of (all_valid, missing_vars)
    """
    import os
    missing = [var for var in required_vars if not os.getenv(var)]
    return len(missing) == 0, missing
