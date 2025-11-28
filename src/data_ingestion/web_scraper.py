"""
Web scraper for policy documents from government websites
"""
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any, Optional
import time
import logging
from pathlib import Path
import json
from ..utils.helpers import setup_logger, safe_api_call

logger = setup_logger(__name__)


class PolicyWebScraper:
    """Scrape policy documents from government websites"""
    
    def __init__(self, output_dir: Path, delay: float = 1.0):
        """
        Initialize web scraper
        
        Args:
            output_dir: Directory to save scraped content
            delay: Delay between requests in seconds
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (PolicyNavigatorAgent/1.0; Research Bot)'
        })
        logger.info(f"PolicyWebScraper initialized with output dir: {self.output_dir}")
    
    @safe_api_call
    def fetch_page(self, url: str) -> Optional[str]:
        """
        Fetch webpage content
        
        Args:
            url: URL to fetch
        
        Returns:
            HTML content or None if failed
        """
        logger.info(f"Fetching: {url}")
        response = self.session.get(url, timeout=30)
        response.raise_for_status()
        time.sleep(self.delay)
        return response.text
    
    def scrape_federal_register(self, search_term: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """
        Scrape documents from Federal Register API
        
        Args:
            search_term: Search query
            max_results: Maximum number of results
        
        Returns:
            List of policy documents
        """
        logger.info(f"Scraping Federal Register for: {search_term}")
        
        api_url = "https://www.federalregister.gov/api/v1/documents.json"
        params = {
            "conditions[term]": search_term,
            "per_page": min(max_results, 100),
            "fields[]": ["title", "abstract", "body_html_url", "publication_date", 
                        "document_number", "type", "agencies"]
        }
        
        try:
            response = requests.get(api_url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            documents = []
            for result in data.get('results', [])[:max_results]:
                doc = {
                    'id': result.get('document_number', ''),
                    'title': result.get('title', ''),
                    'text': result.get('abstract', ''),
                    'url': result.get('body_html_url', ''),
                    'date': result.get('publication_date', ''),
                    'type': result.get('type', ''),
                    'agencies': ', '.join(result.get('agencies', [])),
                    'category': 'Federal Register',
                    'agency': result.get('agencies', [''])[0] if result.get('agencies') else 'Unknown'
                }
                documents.append(doc)
            
            logger.info(f"Scraped {len(documents)} documents from Federal Register")
            return documents
            
        except Exception as e:
            logger.error(f"Error scraping Federal Register: {e}")
            return []
    
    def scrape_epa_regulations(self, max_pages: int = 3) -> List[Dict[str, Any]]:
        """
        Scrape EPA regulations (simplified example)
        
        Args:
            max_pages: Maximum number of pages to scrape
        
        Returns:
            List of regulation documents
        """
        logger.info("Scraping EPA regulations")
        
        # Note: This is a simplified example. Real implementation would need
        # to adapt to the actual structure of EPA website
        documents = [
            {
                'id': 'epa_001',
                'title': 'Clean Water Act Section 404 Permits',
                'text': 'The Clean Water Act Section 404 permit program regulates the discharge of dredged or fill material into waters of the United States, including wetlands.',
                'category': 'Environmental',
                'agency': 'EPA',
                'date': '2024-01-15',
                'type': 'Regulation',
                'url': 'https://www.epa.gov/cwa-404'
            },
            {
                'id': 'epa_002',
                'title': 'National Ambient Air Quality Standards',
                'text': 'The EPA has established National Ambient Air Quality Standards for six principal pollutants, which are called criteria pollutants.',
                'category': 'Environmental',
                'agency': 'EPA',
                'date': '2023-12-10',
                'type': 'Standard',
                'url': 'https://www.epa.gov/criteria-air-pollutants'
            },
            {
                'id': 'epa_003',
                'title': 'Hazardous Waste Management',
                'text': 'RCRA gives EPA the authority to control hazardous waste from cradle to grave including generation, transportation, treatment, storage, and disposal.',
                'category': 'Environmental',
                'agency': 'EPA',
                'date': '2024-03-20',
                'type': 'Regulation',
                'url': 'https://www.epa.gov/hw'
            }
        ]
        
        logger.info(f"Retrieved {len(documents)} EPA regulation documents")
        return documents
    
    def save_documents(self, documents: List[Dict[str, Any]], filename: str):
        """
        Save scraped documents to JSON file
        
        Args:
            documents: List of document dictionaries
            filename: Output filename
        """
        output_path = self.output_dir / filename
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(documents, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved {len(documents)} documents to {output_path}")
        except Exception as e:
            logger.error(f"Error saving documents: {e}")
            raise
    
    def load_documents(self, filename: str) -> List[Dict[str, Any]]:
        """
        Load scraped documents from JSON file
        
        Args:
            filename: Input filename
        
        Returns:
            List of document dictionaries
        """
        input_path = self.output_dir / filename
        
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                documents = json.load(f)
            logger.info(f"Loaded {len(documents)} documents from {input_path}")
            return documents
        except Exception as e:
            logger.error(f"Error loading documents: {e}")
            raise
    
    def scrape_all_sources(self, search_terms: List[str] = None) -> List[Dict[str, Any]]:
        """
        Scrape all configured sources
        
        Args:
            search_terms: List of search terms for Federal Register
        
        Returns:
            Combined list of all documents
        """
        if search_terms is None:
            search_terms = ["executive order", "environmental regulation", "compliance"]
        
        all_documents = []
        
        # Scrape Federal Register
        for term in search_terms:
            docs = self.scrape_federal_register(term, max_results=5)
            all_documents.extend(docs)
            time.sleep(self.delay)
        
        # Scrape EPA
        epa_docs = self.scrape_epa_regulations()
        all_documents.extend(epa_docs)
        
        logger.info(f"Total scraped documents: {len(all_documents)}")
        return all_documents


# Example usage
if __name__ == "__main__":
    from ..config import RAW_DATA_DIR
    
    scraper = PolicyWebScraper(RAW_DATA_DIR / "scraped_policies")
    
    # Scrape documents
    documents = scraper.scrape_all_sources(
        search_terms=["environmental protection", "clean air act"]
    )
    
    # Save to file
    scraper.save_documents(documents, "scraped_policies.json")
    
    print(f"Scraped and saved {len(documents)} policy documents")
