"""
Database Module for Thales065Maker

Stores and manages normalized cable data in JSON format.
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CableDatabase:
    """Manages cable data storage and retrieval."""
    
    def __init__(self, db_path: str = None):
        """
        Initialize the database.
        
        Args:
            db_path: Path to store the database file (default: database/cables_data.json)
        """
        if db_path is None:
            db_path = '/home/pboullet/CAP_AI/THALES/065-maker/database/cables_data.json'
        
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.data = {}
        self.metadata = {
            'created': None,
            'updated': None,
            'total_cables': 0,
            'version': '1.0'
        }
    
    def load(self) -> bool:
        """Load database from file."""
        try:
            if self.db_path.exists():
                with open(self.db_path, 'r', encoding='utf-8') as f:
                    db_content = json.load(f)
                    self.metadata = db_content.get('metadata', self.metadata)
                    self.data = db_content.get('cables', {})
                logger.info(f"Loaded database with {len(self.data)} cables")
                return True
            else:
                logger.info("Database file does not exist, creating new database")
                return True
        except Exception as e:
            logger.error(f"Failed to load database: {e}")
            return False
    
    def save(self) -> bool:
        """Save database to file."""
        try:
            self.metadata['updated'] = datetime.now().isoformat()
            self.metadata['total_cables'] = len(self.data)
            
            db_content = {
                'metadata': self.metadata,
                'cables': self.data
            }
            
            with open(self.db_path, 'w', encoding='utf-8') as f:
                json.dump(db_content, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Saved database with {len(self.data)} cables to {self.db_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to save database: {e}")
            return False
    
    def add_cable(self, cable_ref: str, cable_data: Dict[str, Any]) -> bool:
        """
        Add or update a cable in the database.
        
        Args:
            cable_ref: Cable reference number
            cable_data: Dictionary with cable data
            
        Returns:
            True if successful
        """
        try:
            if not cable_ref:
                logger.warning("Cable reference is empty, skipping")
                return False
            
            # Normalize the cable data
            normalized_data = self._normalize_cable_data(cable_data)
            
            self.data[cable_ref] = normalized_data
            logger.info(f"Added cable {cable_ref} to database")
            return True
        except Exception as e:
            logger.error(f"Failed to add cable {cable_ref}: {e}")
            return False
    
    def add_cables(self, cables: Dict[str, Dict[str, Any]]) -> int:
        """
        Add multiple cables to the database.
        
        Args:
            cables: Dictionary mapping cable references to their data
            
        Returns:
            Number of cables successfully added
        """
        count = 0
        for cable_ref, cable_data in cables.items():
            if self.add_cable(cable_ref, cable_data):
                count += 1
        
        logger.info(f"Added {count} cables to database")
        return count
    
    def get_cable(self, cable_ref: str) -> Dict[str, Any]:
        """
        Retrieve a cable from the database.
        
        Args:
            cable_ref: Cable reference number
            
        Returns:
            Cable data dictionary or None if not found
        """
        return self.data.get(cable_ref)
    
    def get_all_cables(self) -> Dict[str, Dict[str, Any]]:
        """Get all cables from the database."""
        return self.data.copy()
    
    def get_cable_list(self) -> List[str]:
        """Get list of all cable references."""
        return list(self.data.keys())
    
    def delete_cable(self, cable_ref: str) -> bool:
        """Delete a cable from the database."""
        if cable_ref in self.data:
            del self.data[cable_ref]
            logger.info(f"Deleted cable {cable_ref} from database")
            return True
        return False
    
    def _normalize_cable_data(self, cable_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize cable data for storage.
        
        Args:
            cable_data: Raw cable data from extraction
            
        Returns:
            Normalized cable data
        """
        normalized = {
            'cable_reference': cable_data.get('cable_reference', ''),
            'revision_letter': cable_data.get('revision_letter', ''),
            'created_by': cable_data.get('created_by'),
            'created_date': cable_data.get('created_date'),
            'modified_date': cable_data.get('modified_date'),
            'modified_by': cable_data.get('modified_by'),
            'first_validation_date': cable_data.get('first_validation_date'),
            'first_validator': cable_data.get('first_validator'),
            'modification_reason': cable_data.get('modification_reason'),
            'second_validation_date': cable_data.get('second_validation_date'),
            'second_validator': cable_data.get('second_validator'),
            'full_instructions': cable_data.get('full_instructions', ''),
            'special_notes': cable_data.get('special_notes', []),
            'component_references': cable_data.get('component_references', []),
            'sheet_name': cable_data.get('sheet_name', ''),
            'extracted_at': datetime.now().isoformat()
        }
        
        return normalized
    
    def export_csv(self, output_path: str = None) -> bool:
        """
        Export cable data to CSV format.
        
        Args:
            output_path: Path to save CSV file
            
        Returns:
            True if successful
        """
        try:
            if output_path is None:
                output_path = str(self.db_path.parent / 'cables_data.csv')
            
            import csv
            
            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                if not self.data:
                    logger.warning("No cables to export")
                    return False
                
                # Get headers from first cable
                first_cable = next(iter(self.data.values()))
                fieldnames = list(first_cable.keys())
                
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                
                for cable_ref, cable_data in self.data.items():
                    # Convert lists to strings for CSV
                    row = cable_data.copy()
                    row['special_notes'] = '|'.join(row.get('special_notes', []))
                    row['component_references'] = '|'.join(row.get('component_references', []))
                    writer.writerow(row)
            
            logger.info(f"Exported {len(self.data)} cables to CSV: {output_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to export CSV: {e}")
            return False
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get database statistics."""
        stats = {
            'total_cables': len(self.data),
            'cables_with_instructions': sum(1 for c in self.data.values() if c.get('full_instructions')),
            'cables_with_special_notes': sum(1 for c in self.data.values() if c.get('special_notes')),
            'cables_with_component_refs': sum(1 for c in self.data.values() if c.get('component_references')),
            'created': self.metadata.get('created'),
            'updated': self.metadata.get('updated'),
        }
        return stats


def build_database(excel_path: str, db_path: str = None) -> CableDatabase:
    """
    Build database from Excel file.
    
    Args:
        excel_path: Path to dossier_cables.xlsx
        db_path: Path to store database (optional)
        
    Returns:
        CableDatabase instance
    """
    from excel_reader import ingest_excel_file
    
    # Ingest Excel file
    logger.info("Ingesting Excel file...")
    cables = ingest_excel_file(excel_path)
    
    # Create and populate database
    db = CableDatabase(db_path)
    db.metadata['created'] = datetime.now().isoformat()
    
    logger.info("Adding cables to database...")
    db.add_cables(cables)
    
    # Save database
    db.save()
    
    # Print statistics
    stats = db.get_statistics()
    logger.info(f"Database statistics: {stats}")
    
    return db


if __name__ == '__main__':
    # Test the database
    excel_path = '/home/pboullet/CAP_AI/THALES/065-maker/inputs/dossier_cables.xlsx'
    db = build_database(excel_path)
    
    print("\nDatabase Statistics:")
    stats = db.get_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print("\nCables in database:")
    for cable_ref in db.get_cable_list()[:5]:
        cable = db.get_cable(cable_ref)
        print(f"  {cable_ref}: Rev {cable.get('revision_letter')}, Created {cable.get('created_date')}")
