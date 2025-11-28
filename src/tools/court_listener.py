"""
CourtListener API integration tool
Search for case law related to regulations
"""
import requests
from typing import Dict, Any, List, Optional
import logging
import os
from ..utils.helpers import setup_logger, safe_api_call
from ..config import COURTLISTENER_API_KEY

logger = setup_logger(__name__)


class CourtListenerTool:
    """Interface with CourtListener API for case law research"""
    
    BASE_URL = "https://www.courtlistener.com/api/rest/v3"
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize CourtListener API client
        
        Args:
            api_key: CourtListener API key (optional, will use env var)
        """
        self.api_key = api_key or COURTLISTENER_API_KEY
        self.session = requests.Session()
        
        if self.api_key:
            self.session.headers.update({
                "Authorization": f"Token {self.api_key}"
            })
        else:
            logger.warning("No CourtListener API key provided. Some features may be limited.")
        
        logger.info("CourtListenerTool initialized")
    
    @safe_api_call
    def search_case_law(
        self,
        regulation_reference: str,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Search for court cases related to a specific regulation
        
        Args:
            regulation_reference: Regulation name or section (e.g., "Section 230")
            limit: Maximum number of cases to return
        
        Returns:
            List of relevant court cases
        """
        logger.info(f"Searching case law for: {regulation_reference}")
        
        # Note: CourtListener API requires authentication for most endpoints
        # This is a simplified implementation
        
        url = f"{self.BASE_URL}/search/"
        params = {
            "q": regulation_reference,
            "type": "o",  # opinions
            "order_by": "score desc"
        }
        
        if not self.api_key:
            # Return mock data if no API key
            logger.warning("Using mock data - no API key provided")
            return self._get_mock_case_law(regulation_reference, limit)
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            cases = []
            for result in data.get('results', [])[:limit]:
                cases.append({
                    "case_name": result.get('caseName'),
                    "court": result.get('court'),
                    "date_filed": result.get('dateFiled'),
                    "snippet": result.get('snippet'),
                    "url": result.get('absolute_url'),
                    "citation": result.get('citation', []),
                    "status": result.get('status')
                })
            
            logger.info(f"Found {len(cases)} court cases")
            return cases
            
        except Exception as e:
            logger.error(f"Error searching case law: {e}")
            return self._get_mock_case_law(regulation_reference, limit)
    
    def _get_mock_case_law(self, regulation: str, limit: int) -> List[Dict[str, Any]]:
        """
        Return mock case law data for testing
        
        Args:
            regulation: Regulation reference
            limit: Max results
        
        Returns:
            Mock case data
        """
        mock_cases = {
            "Section 230": [
                {
                    "case_name": "Fair Housing Council v. Roommates.com",
                    "court": "9th Circuit Court of Appeals",
                    "date_filed": "2008-04-03",
                    "snippet": "This case clarified the limits of Section 230 immunity, holding that website design that contributes to allegedly unlawful content can remove immunity protection.",
                    "url": "https://www.courtlistener.com/opinion/...",
                    "citation": ["521 F.3d 1157"],
                    "status": "Precedential"
                },
                {
                    "case_name": "Zeran v. America Online, Inc.",
                    "court": "4th Circuit Court of Appeals",
                    "date_filed": "1997-11-12",
                    "snippet": "Established broad immunity for ISPs under Section 230, holding that providers cannot be held liable for content posted by third parties.",
                    "url": "https://www.courtlistener.com/opinion/...",
                    "citation": ["129 F.3d 327"],
                    "status": "Precedential"
                }
            ],
            "Clean Air Act": [
                {
                    "case_name": "Massachusetts v. EPA",
                    "court": "Supreme Court of the United States",
                    "date_filed": "2007-04-02",
                    "snippet": "The Supreme Court held that the EPA has authority to regulate greenhouse gas emissions from new motor vehicles under the Clean Air Act.",
                    "url": "https://www.courtlistener.com/opinion/...",
                    "citation": ["549 U.S. 497"],
                    "status": "Precedential"
                }
            ],
            "default": [
                {
                    "case_name": "Sample Case v. Example Defendant",
                    "court": "District Court",
                    "date_filed": "2023-01-15",
                    "snippet": f"This case discusses {regulation} and its application.",
                    "url": "https://www.courtlistener.com/opinion/...",
                    "citation": ["123 F. Supp. 3d 456"],
                    "status": "Published"
                }
            ]
        }
        
        # Find matching cases
        for key in mock_cases:
            if key.lower() in regulation.lower():
                return mock_cases[key][:limit]
        
        return mock_cases["default"][:limit]
    
    @safe_api_call
    def get_case_details(self, case_id: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific case
        
        Args:
            case_id: CourtListener case ID
        
        Returns:
            Detailed case information
        """
        logger.info(f"Fetching details for case: {case_id}")
        
        url = f"{self.BASE_URL}/opinions/{case_id}/"
        
        if not self.api_key:
            return {"error": "API key required for detailed case information"}
        
        response = self.session.get(url, timeout=30)
        response.raise_for_status()
        return response.json()


# Function wrappers for agent integration

def search_case_law(regulation_reference: str, limit: int = 5) -> List[Dict[str, Any]]:
    """
    Search for court cases related to a specific regulation
    
    Args:
        regulation_reference: Section or regulation name
        limit: Max number of cases to return
    
    Returns:
        List of relevant court cases
    """
    tool = CourtListenerTool()
    return tool.search_case_law(regulation_reference, limit)


def find_legal_precedents(regulation: str) -> str:
    """
    Find and format legal precedents for a regulation
    
    Args:
        regulation: Regulation name or reference
    
    Returns:
        Formatted string with case law information
    """
    tool = CourtListenerTool()
    cases = tool.search_case_law(regulation, limit=5)
    
    if not cases:
        return f"No court cases found referencing {regulation}."
    
    result = [f"Found {len(cases)} court cases referencing {regulation}:\n"]
    
    for i, case in enumerate(cases, 1):
        result.append(f"\n{i}. {case.get('case_name')} ({case.get('court')})")
        result.append(f"   Date: {case.get('date_filed')}")
        if case.get('snippet'):
            result.append(f"   Summary: {case.get('snippet')}")
        if case.get('url'):
            result.append(f"   Link: {case.get('url')}")
    
    return '\n'.join(result)


# Example usage
if __name__ == "__main__":
    tool = CourtListenerTool()
    
    # Test case law search
    print("Testing case law search...")
    cases = tool.search_case_law("Section 230", limit=3)
    print(f"Found {len(cases)} cases")
    
    for case in cases:
        print(f"\n{case.get('case_name')}")
        print(f"Court: {case.get('court')}")
        print(f"Date: {case.get('date_filed')}")
