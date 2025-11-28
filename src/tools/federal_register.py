"""
Federal Register API integration tool
Check policy status, search regulations, and retrieve executive orders
"""
import requests
from typing import Dict, Any, Optional, List
import logging
from ..utils.helpers import setup_logger, safe_api_call

logger = setup_logger(__name__)


class FederalRegisterTool:
    """Interface with Federal Register API"""
    
    BASE_URL = "https://www.federalregister.gov/api/v1"
    
    def __init__(self):
        """Initialize Federal Register API client"""
        self.session = requests.Session()
        logger.info("FederalRegisterTool initialized")
    
    @safe_api_call
    def check_executive_order_status(self, order_number: str) -> Dict[str, Any]:
        """
        Check if an executive order is active or repealed
        
        Args:
            order_number: Executive order number (e.g., "14067")
        
        Returns:
            Status information dictionary
        """
        logger.info(f"Checking status of Executive Order {order_number}")
        
        url = f"{self.BASE_URL}/documents.json"
        params = {
            "conditions[term]": f"Executive Order {order_number}",
            "fields[]": ["title", "publication_date", "type", "html_url", 
                        "executive_order_number", "signing_date"],
            "per_page": 5
        }
        
        response = self.session.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        if data.get('results'):
            result = data['results'][0]
            return {
                "status": "active",
                "executive_order": order_number,
                "title": result.get('title'),
                "publication_date": result.get('publication_date'),
                "signing_date": result.get('signing_date'),
                "url": result.get('html_url'),
                "source": "Federal Register API",
                "details": result
            }
        else:
            return {
                "status": "not_found",
                "executive_order": order_number,
                "message": f"No records found for Executive Order {order_number}",
                "source": "Federal Register API"
            }
    
    @safe_api_call
    def search_regulations(
        self, 
        search_term: str, 
        agency: Optional[str] = None,
        document_type: Optional[str] = None,
        max_results: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Search regulations by term
        
        Args:
            search_term: Search query
            agency: Filter by agency (optional)
            document_type: Filter by type (optional)
            max_results: Maximum results to return
        
        Returns:
            List of matching regulations
        """
        logger.info(f"Searching regulations for: {search_term}")
        
        url = f"{self.BASE_URL}/documents.json"
        params = {
            "conditions[term]": search_term,
            "per_page": min(max_results, 100),
            "fields[]": ["title", "abstract", "publication_date", "type", 
                        "agencies", "html_url", "document_number"]
        }
        
        if agency:
            params["conditions[agencies][]"] = agency
        
        if document_type:
            params["conditions[type]"] = document_type
        
        response = self.session.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        results = []
        for item in data.get('results', []):
            results.append({
                "document_number": item.get('document_number'),
                "title": item.get('title'),
                "abstract": item.get('abstract'),
                "publication_date": item.get('publication_date'),
                "type": item.get('type'),
                "agencies": item.get('agencies', []),
                "url": item.get('html_url')
            })
        
        logger.info(f"Found {len(results)} regulations")
        return results
    
    @safe_api_call
    def get_recent_documents(
        self, 
        days: int = 7,
        document_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get recent documents from Federal Register
        
        Args:
            days: Number of days to look back
            document_type: Filter by document type
        
        Returns:
            List of recent documents
        """
        from datetime import datetime, timedelta
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        logger.info(f"Fetching documents from {start_date.date()} to {end_date.date()}")
        
        url = f"{self.BASE_URL}/documents.json"
        params = {
            "conditions[publication_date][gte]": start_date.strftime("%Y-%m-%d"),
            "conditions[publication_date][lte]": end_date.strftime("%Y-%m-%d"),
            "per_page": 20,
            "fields[]": ["title", "publication_date", "type", "agencies", "html_url"]
        }
        
        if document_type:
            params["conditions[type]"] = document_type
        
        response = self.session.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        return data.get('results', [])


# Function wrappers for agent integration

def check_policy_status(executive_order_number: str) -> Dict[str, Any]:
    """
    Check if an executive order is active or repealed
    
    Args:
        executive_order_number: EO number (e.g., "14067")
    
    Returns:
        Status information from Federal Register API
    """
    tool = FederalRegisterTool()
    return tool.check_executive_order_status(executive_order_number)


def search_federal_regulations(
    search_term: str,
    agency: str = None,
    max_results: int = 10
) -> List[Dict[str, Any]]:
    """
    Search federal regulations
    
    Args:
        search_term: What to search for
        agency: Filter by specific agency
        max_results: Maximum number of results
    
    Returns:
        List of matching regulations
    """
    tool = FederalRegisterTool()
    return tool.search_regulations(search_term, agency=agency, max_results=max_results)


# Example usage
if __name__ == "__main__":
    tool = FederalRegisterTool()
    
    # Test executive order check
    print("Testing Executive Order status check...")
    result = tool.check_executive_order_status("14067")
    print(f"Status: {result.get('status')}")
    print(f"Title: {result.get('title')}")
    
    # Test regulation search
    print("\nTesting regulation search...")
    regulations = tool.search_regulations("environmental protection", max_results=3)
    print(f"Found {len(regulations)} regulations")
    for reg in regulations[:2]:
        print(f"- {reg.get('title')}")
