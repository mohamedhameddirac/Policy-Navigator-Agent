"""
Dataset loader for policy documents
Loads data from CSV, JSON, or Excel files
"""
import pandas as pd
from pathlib import Path
from typing import List, Dict, Any
import logging
from ..utils.helpers import setup_logger

logger = setup_logger(__name__)


class DatasetLoader:
    """Load and process policy datasets"""
    
    def __init__(self, data_dir: Path):
        """
        Initialize dataset loader
        
        Args:
            data_dir: Directory containing datasets
        """
        self.data_dir = Path(data_dir)
        logger.info(f"DatasetLoader initialized with directory: {self.data_dir}")
    
    def load_csv(self, filename: str, encoding: str = 'utf-8') -> pd.DataFrame:
        """
        Load CSV file
        
        Args:
            filename: CSV filename
            encoding: File encoding
        
        Returns:
            DataFrame with loaded data
        """
        file_path = self.data_dir / filename
        logger.info(f"Loading CSV file: {file_path}")
        
        try:
            df = pd.read_csv(file_path, encoding=encoding)
            logger.info(f"Loaded {len(df)} records from {filename}")
            return df
        except Exception as e:
            logger.error(f"Error loading CSV {filename}: {e}")
            raise
    
    def load_json(self, filename: str) -> pd.DataFrame:
        """
        Load JSON file
        
        Args:
            filename: JSON filename
        
        Returns:
            DataFrame with loaded data
        """
        file_path = self.data_dir / filename
        logger.info(f"Loading JSON file: {file_path}")
        
        try:
            df = pd.read_json(file_path)
            logger.info(f"Loaded {len(df)} records from {filename}")
            return df
        except Exception as e:
            logger.error(f"Error loading JSON {filename}: {e}")
            raise
    
    def load_excel(self, filename: str, sheet_name: str = 0) -> pd.DataFrame:
        """
        Load Excel file
        
        Args:
            filename: Excel filename
            sheet_name: Sheet name or index
        
        Returns:
            DataFrame with loaded data
        """
        file_path = self.data_dir / filename
        logger.info(f"Loading Excel file: {file_path}")
        
        try:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            logger.info(f"Loaded {len(df)} records from {filename}")
            return df
        except Exception as e:
            logger.error(f"Error loading Excel {filename}: {e}")
            raise
    
    def prepare_policy_records(
        self, 
        df: pd.DataFrame,
        text_column: str = 'text',
        id_column: str = 'id',
        metadata_columns: List[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Prepare policy records for vector indexing
        
        Args:
            df: DataFrame with policy data
            text_column: Column containing policy text
            id_column: Column containing unique IDs
            metadata_columns: Columns to include as metadata
        
        Returns:
            List of policy records ready for indexing
        """
        if metadata_columns is None:
            metadata_columns = ['category', 'agency', 'date', 'type']
        
        records = []
        
        for idx, row in df.iterrows():
            # Generate ID if not present
            if id_column not in df.columns:
                record_id = f"doc_{idx}"
            else:
                record_id = str(row[id_column])
            
            # Extract text
            if text_column not in df.columns:
                logger.warning(f"Text column '{text_column}' not found. Skipping row {idx}")
                continue
            
            text = str(row[text_column])
            
            # Extract metadata
            attributes = {}
            for col in metadata_columns:
                if col in df.columns and pd.notna(row[col]):
                    attributes[col] = str(row[col])
            
            records.append({
                'id': record_id,
                'text': text,
                'attributes': attributes
            })
        
        logger.info(f"Prepared {len(records)} policy records")
        return records
    
    def create_sample_dataset(self, output_file: str = "sample_policies.csv"):
        """
        Create a sample policy dataset for testing
        
        Args:
            output_file: Output filename
        """
        sample_data = {
            'id': [f'policy_{i}' for i in range(1, 11)],
            'title': [
                'Clean Air Act Amendments',
                'Occupational Safety Standards',
                'Data Privacy Regulation',
                'Environmental Protection Guidelines',
                'Healthcare Compliance Requirements',
                'Financial Reporting Standards',
                'Food Safety Regulations',
                'Transportation Safety Rules',
                'Energy Efficiency Standards',
                'Consumer Protection Laws'
            ],
            'text': [
                'The Clean Air Act requires the EPA to regulate air pollution emissions. Facilities must monitor and report emissions quarterly. Non-compliance may result in fines up to $50,000 per violation.',
                'OSHA requires employers to provide a safe workplace. This includes proper training, protective equipment, and hazard communication. Annual safety audits are mandatory.',
                'Organizations must protect personal data and notify individuals of breaches within 72 hours. Data retention policies must be documented and enforced.',
                'The EPA establishes guidelines for environmental impact assessments. Projects affecting wetlands require federal permits and ongoing monitoring.',
                'Healthcare providers must comply with HIPAA regulations for patient data protection. Regular staff training and security audits are required.',
                'Public companies must file quarterly and annual reports following GAAP standards. Independent audits are required annually.',
                'Food manufacturers must follow FDA guidelines for safety and labeling. Regular inspections ensure compliance with sanitation standards.',
                'Commercial vehicles must meet DOT safety requirements including regular inspections, driver qualifications, and hours of service limits.',
                'The Energy Star program sets efficiency standards for appliances and buildings. Compliance can qualify for tax incentives.',
                'Consumer protection laws prohibit unfair or deceptive practices. Companies must provide clear terms and honor warranties.'
            ],
            'category': [
                'Environmental', 'Workplace Safety', 'Data Privacy', 'Environmental',
                'Healthcare', 'Financial', 'Food Safety', 'Transportation',
                'Energy', 'Consumer Protection'
            ],
            'agency': [
                'EPA', 'OSHA', 'FTC', 'EPA', 'HHS', 'SEC', 'FDA', 'DOT', 'DOE', 'FTC'
            ],
            'date': [
                '2020-01-15', '2019-06-20', '2021-03-10', '2018-11-05',
                '2020-08-30', '2019-12-15', '2021-05-20', '2020-02-28',
                '2019-09-10', '2021-07-15'
            ],
            'type': [
                'Regulation', 'Standard', 'Law', 'Guideline', 'Rule',
                'Standard', 'Regulation', 'Rule', 'Standard', 'Law'
            ]
        }
        
        df = pd.DataFrame(sample_data)
        output_path = self.data_dir / output_file
        df.to_csv(output_path, index=False)
        logger.info(f"Sample dataset created: {output_path}")
        
        return df


# Example usage
if __name__ == "__main__":
    from ..config import RAW_DATA_DIR
    
    loader = DatasetLoader(RAW_DATA_DIR)
    
    # Create sample dataset
    sample_df = loader.create_sample_dataset()
    print(f"Created sample dataset with {len(sample_df)} policies")
    
    # Prepare records for indexing
    records = loader.prepare_policy_records(sample_df)
    print(f"Prepared {len(records)} records for indexing")
