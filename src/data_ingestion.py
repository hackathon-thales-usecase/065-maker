"""
Data Ingestion Module for Thales065Maker

Extracts cable data from dossier_cables.xlsx and normalizes it for storage.
"""

import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ExcelDateConverter:
    """Convert Excel serial dates to standard date format."""
    
    # Excel's epoch: January 1, 1900
    EXCEL_EPOCH = datetime(1900, 1, 1)
    
    @staticmethod
    def excel_to_date(excel_serial: float) -> Optional[str]:
        """
        Convert Excel serial number to ISO date string (YYYY-MM-DD).
        
        Args:
            excel_serial: Excel serial date number
            
        Returns:
            ISO format date string or None if invalid
        """
        if pd.isna(excel_serial) or excel_serial is None:
            return None
        
        try:
            # Excel has a leap year bug for 1900, so we need to adjust
            if excel_serial > 59:
                excel_serial -= 1
            
            date_obj = ExcelDateConverter.EXCEL_EPOCH + timedelta(days=excel_serial)
            return date_obj.strftime('%Y-%m-%d')
        except (ValueError, TypeError):
            logger.warning(f"Could not convert Excel date: {excel_serial}")
            return None


class CableDataExtractor:
    """Extract and normalize cable data from Excel sheets."""
    
    # Define the 14 data items to extract
    METADATA_FIELDS = {
        'cable_reference': ('F', 1),      # Row 1, Column F
        'revision_letter': ('G', 1),      # Row 1, Column G
        'created_by': ('B', 2),           # Row 2, Column B
        'created_date': ('D', 2),         # Row 2, Column D
        'modified_date': ('F', 2),        # Row 2, Column F
        'modified_by': ('H', 2),          # Row 2, Column H
        'first_validation_date': ('B', 3),  # Row 3, Column B
        'first_validator': ('D', 3),      # Row 3, Column D
        'modification_reason': ('F', 3),  # Row 3, Column F
        'second_validation_date': ('B', 4),  # Row 4, Column B
        'second_validator': ('D', 4),     # Row 4, Column D
    }
    
    def __init__(self, excel_path: str):
        """
        Initialize the extractor with an Excel file path.
        
        Args:
            excel_path: Path to dossier_cables.xlsx
        """
        self.excel_path = excel_path
        self.excel_file = None
        self.sheet_names = []
        
    def load_workbook(self) -> bool:
        """Load the Excel workbook and get sheet names."""
        try:
            self.excel_file = pd.ExcelFile(self.excel_path)
            self.sheet_names = self.excel_file.sheet_names
            logger.info(f"Loaded workbook with {len(self.sheet_names)} sheets")
            return True
        except Exception as e:
            logger.error(f"Failed to load workbook: {e}")
            return False
    
    def extract_metadata(self, sheet_name: str, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Extract metadata from rows 1-4 of a sheet.
        
        Args:
            sheet_name: Name of the sheet
            df: DataFrame of the sheet
            
        Returns:
            Dictionary with extracted metadata
        """
        metadata = {}
        
        for field_name, (col, row) in self.METADATA_FIELDS.items():
            try:
                # Convert column letter to index (A=0, B=1, etc.)
                col_idx = ord(col.upper()) - ord('A')
                row_idx = row - 1  # Convert to 0-based index
                
                if row_idx < len(df) and col_idx < len(df.columns):
                    value = df.iloc[row_idx, col_idx]
                    
                    # Handle date fields
                    if 'date' in field_name:
                        value = ExcelDateConverter.excel_to_date(value)
                    elif pd.isna(value):
                        value = None
                    else:
                        value = str(value).strip() if value is not None else None
                    
                    metadata[field_name] = value
                else:
                    metadata[field_name] = None
            except Exception as e:
                logger.warning(f"Error extracting {field_name}: {e}")
                metadata[field_name] = None
        
        return metadata
    
    def extract_instructions(self, df: pd.DataFrame) -> tuple[str, List[str], List[str]]:
        """
        Extract full instructions, special notes, and component references from rows 5+.
        
        Args:
            df: DataFrame of the sheet
            
        Returns:
            Tuple of (full_instructions, special_notes, component_references)
        """
        # Get all rows from row 5 onwards (index 4+)
        instruction_rows = []
        special_notes = []
        component_refs = []
        
        for idx in range(4, len(df)):
            row_data = df.iloc[idx]
            
            # Concatenate all non-empty cells in the row
            row_text = ' | '.join(
                str(cell).strip() 
                for cell in row_data 
                if pd.notna(cell) and str(cell).strip()
            )
            
            if row_text:
                instruction_rows.append(row_text)
                
                # Extract special notes (look for keywords like ATTENTION, WARNING, etc.)
                row_str = str(row_text).upper()
                if any(keyword in row_str for keyword in ['ATTENTION', 'WARNING', 'IMPORTANT', 'DANGER']):
                    special_notes.append(row_text)
                
                # Extract component references (look for patterns like numbers with letters)
                # Simple heuristic: look for patterns like "91624771" or similar
                import re
                refs = re.findall(r'\b\d{6,}\b', row_text)
                component_refs.extend(refs)
        
        full_instructions = '\n'.join(instruction_rows)
        component_refs = list(set(component_refs))  # Remove duplicates
        
        return full_instructions, special_notes, component_refs
    
    def extract_cable_data(self, sheet_name: str) -> Dict[str, Any]:
        """
        Extract all 14 data items from a cable sheet.
        
        Args:
            sheet_name: Name of the sheet to extract
            
        Returns:
            Dictionary with all extracted data
        """
        try:
            # Read the sheet
            df = pd.read_excel(self.excel_path, sheet_name=sheet_name, header=None)
            
            # Extract metadata (11 items)
            metadata = self.extract_metadata(sheet_name, df)
            
            # Extract content (3 items)
            full_instructions, special_notes, component_refs = self.extract_instructions(df)
            
            # Combine all data
            cable_data = {
                **metadata,
                'full_instructions': full_instructions,
                'special_notes': special_notes,
                'component_references': component_refs,
                'sheet_name': sheet_name,
            }
            
            return cable_data
        except Exception as e:
            logger.error(f"Error extracting data from sheet {sheet_name}: {e}")
            return None
    
    def extract_all_cables(self) -> Dict[str, Dict[str, Any]]:
        """
        Extract data from all cable sheets.
        
        Returns:
            Dictionary mapping cable references to their data
        """
        if not self.excel_file:
            self.load_workbook()
        
        all_cables = {}
        
        for sheet_name in self.sheet_names:
            logger.info(f"Extracting data from sheet: {sheet_name}")
            cable_data = self.extract_cable_data(sheet_name)
            
            if cable_data:
                # Use cable reference as key if available
                cable_ref = cable_data.get('cable_reference')
                if cable_ref:
                    all_cables[cable_ref] = cable_data
                else:
                    all_cables[sheet_name] = cable_data
        
        logger.info(f"Successfully extracted data from {len(all_cables)} cables")
        return all_cables


def ingest_excel_file(excel_path: str) -> Dict[str, Dict[str, Any]]:
    """
    Main function to ingest Excel file and extract all cable data.
    
    Args:
        excel_path: Path to dossier_cables.xlsx
        
    Returns:
        Dictionary with all extracted cable data
    """
    extractor = CableDataExtractor(excel_path)
    
    if not extractor.load_workbook():
        logger.error("Failed to load workbook")
        return {}
    
    all_cables = extractor.extract_all_cables()
    return all_cables


if __name__ == '__main__':
    # Test the ingestion
    excel_path = '/home/pboullet/CAP_AI/THALES/065-maker/inputs/dossier_cables.xlsx'
    cables = ingest_excel_file(excel_path)
    
    print(f"\nExtracted {len(cables)} cables")
    for cable_ref, data in list(cables.items())[:2]:
        print(f"\n{cable_ref}:")
        print(f"  Revision: {data.get('revision_letter')}")
        print(f"  Created: {data.get('created_date')} by {data.get('created_by')}")
        print(f"  Instructions length: {len(data.get('full_instructions', ''))}")
        print(f"  Special notes: {len(data.get('special_notes', []))}")
        print(f"  Component refs: {data.get('component_references', [])[:3]}")
