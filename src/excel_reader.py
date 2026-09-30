"""
Pure Python Excel Reader for XLSX files

Reads Excel files without requiring openpyxl by using zipfile and XML parsing.
"""

import zipfile
import xml.etree.ElementTree as ET
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
import re
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ExcelReader:
    """Read XLSX files using zipfile and XML parsing."""
    
    # Excel's epoch: January 1, 1900
    EXCEL_EPOCH = datetime(1900, 1, 1)
    
    # XML namespace
    NS = {'': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
    
    def __init__(self, excel_path: str):
        """Initialize the Excel reader."""
        self.excel_path = excel_path
        self.zip_file = None
        self.shared_strings = []
        self.sheet_names = []
        self.sheet_ids = {}
        
    def load(self) -> bool:
        """Load the Excel file and extract metadata."""
        try:
            self.zip_file = zipfile.ZipFile(self.excel_path, 'r')
            
            # Load shared strings
            self._load_shared_strings()
            
            # Load sheet names
            self._load_sheet_names()
            
            logger.info(f"Loaded Excel file with {len(self.sheet_names)} sheets")
            return True
        except Exception as e:
            logger.error(f"Failed to load Excel file: {e}")
            return False
    
    def _load_shared_strings(self):
        """Load the shared strings table."""
        try:
            with self.zip_file.open('xl/sharedStrings.xml') as f:
                tree = ET.parse(f)
                root = tree.getroot()
                
                # Find all string items
                for si in root.findall('.//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}si'):
                    text_parts = []
                    for t in si.findall('.//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t'):
                        if t.text:
                            text_parts.append(t.text)
                    self.shared_strings.append(''.join(text_parts))
                
                logger.info(f"Loaded {len(self.shared_strings)} shared strings")
        except Exception as e:
            logger.warning(f"Could not load shared strings: {e}")
    
    def _load_sheet_names(self):
        """Load sheet names from workbook.xml."""
        try:
            with self.zip_file.open('xl/workbook.xml') as f:
                tree = ET.parse(f)
                root = tree.getroot()
                
                # Find all sheets
                for sheet in root.findall('.//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}sheet'):
                    name = sheet.get('name')
                    sheet_id = sheet.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')
                    if name:
                        self.sheet_names.append(name)
                        self.sheet_ids[name] = sheet_id
                
                logger.info(f"Found sheets: {self.sheet_names}")
        except Exception as e:
            logger.error(f"Could not load sheet names: {e}")
    
    def _get_sheet_filename(self, sheet_name: str) -> Optional[str]:
        """Get the XML filename for a sheet."""
        try:
            sheet_id = self.sheet_ids.get(sheet_name)
            if not sheet_id:
                return None
            
            # Read the workbook relationships
            with self.zip_file.open('xl/_rels/workbook.xml.rels') as f:
                tree = ET.parse(f)
                root = tree.getroot()
                
                # Find the relationship with matching ID
                for rel in root.findall('.//{http://schemas.openxmlformats.org/package/2006/relationships}Relationship'):
                    if rel.get('Id') == sheet_id:
                        target = rel.get('Target')
                        return f'xl/{target}'
            
            return None
        except Exception as e:
            logger.warning(f"Could not get sheet filename for {sheet_name}: {e}")
            return None
    
    def _parse_cell_value(self, cell_elem) -> Any:
        """Parse the value from a cell element."""
        try:
            # Get cell type
            cell_type = cell_elem.get('t', 'n')  # Default to number
            
            # Get the value
            value_elem = cell_elem.find('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}v')
            if value_elem is None or value_elem.text is None:
                return None
            
            value = value_elem.text
            
            # Handle different cell types
            if cell_type == 's':  # Shared string
                try:
                    idx = int(value)
                    return self.shared_strings[idx] if idx < len(self.shared_strings) else value
                except (ValueError, IndexError):
                    return value
            elif cell_type == 'n':  # Number
                try:
                    if '.' in value:
                        return float(value)
                    else:
                        return int(value)
                except ValueError:
                    return value
            elif cell_type == 'd':  # Date
                return value
            else:
                return value
        except Exception as e:
            logger.warning(f"Error parsing cell value: {e}")
            return None
    
    def _excel_to_date(self, excel_serial: float) -> Optional[str]:
        """Convert Excel serial number to ISO date string."""
        if excel_serial is None:
            return None
        
        try:
            excel_serial = float(excel_serial)
            # Excel has a leap year bug for 1900
            if excel_serial > 59:
                excel_serial -= 1
            
            date_obj = self.EXCEL_EPOCH + timedelta(days=excel_serial)
            return date_obj.strftime('%Y-%m-%d')
        except (ValueError, TypeError):
            return None
    
    def read_sheet(self, sheet_name: str) -> List[List[Any]]:
        """
        Read a sheet and return data as a 2D list.
        
        Args:
            sheet_name: Name of the sheet to read
            
        Returns:
            List of rows, where each row is a list of cell values
        """
        try:
            sheet_filename = self._get_sheet_filename(sheet_name)
            if not sheet_filename:
                logger.error(f"Could not find sheet file for {sheet_name}")
                return []
            
            with self.zip_file.open(sheet_filename) as f:
                tree = ET.parse(f)
                root = tree.getroot()
                
                # Find the sheet data
                sheet_data = root.find('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}sheetData')
                if sheet_data is None:
                    return []
                
                # Parse rows
                rows = []
                for row_elem in sheet_data.findall('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}row'):
                    row_num = int(row_elem.get('r', 0))
                    
                    # Ensure we have enough rows
                    while len(rows) < row_num:
                        rows.append([])
                    
                    # Parse cells in this row
                    row_data = []
                    max_col = 0
                    
                    for cell_elem in row_elem.findall('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}c'):
                        cell_ref = cell_elem.get('r', '')
                        
                        # Extract column number from cell reference (e.g., "A1" -> 0, "B1" -> 1)
                        col_letter = ''.join(c for c in cell_ref if c.isalpha())
                        col_num = 0
                        for c in col_letter:
                            col_num = col_num * 26 + (ord(c) - ord('A') + 1)
                        col_num -= 1  # Convert to 0-based
                        
                        # Ensure we have enough columns
                        while len(row_data) <= col_num:
                            row_data.append(None)
                        
                        # Parse cell value
                        value = self._parse_cell_value(cell_elem)
                        row_data[col_num] = value
                        max_col = max(max_col, col_num)
                    
                    # Trim row to actual data
                    row_data = row_data[:max_col + 1]
                    rows[row_num - 1] = row_data
                
                logger.info(f"Read sheet {sheet_name}: {len(rows)} rows")
                return rows
        except Exception as e:
            logger.error(f"Error reading sheet {sheet_name}: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def close(self):
        """Close the Excel file."""
        if self.zip_file:
            self.zip_file.close()


class CableDataExtractor:
    """Extract cable data from Excel sheets."""
    
    # Define the 14 data items to extract
    # Based on actual Excel structure:
    # Row 1: Cable Reference (G), Revision Letter (H)
    # Row 4: Created By (E), Created Date (G), Modified Date (J), Modified By (L)
    # Row 5: First Validation Date (E), First Validator (G), Modification Reason (J)
    METADATA_FIELDS = {
        'cable_reference': ('G', 1),      # Row 1, Column G (index 6)
        'revision_letter': ('H', 1),      # Row 1, Column H (index 7)
        'created_by': ('E', 4),           # Row 4, Column E (index 4)
        'created_date': ('G', 4),         # Row 4, Column G (index 6)
        'modified_date': ('J', 4),        # Row 4, Column J (index 9)
        'modified_by': ('L', 4),          # Row 4, Column L (index 11)
        'first_validation_date': ('E', 5),  # Row 5, Column E (index 4)
        'first_validator': ('G', 5),      # Row 5, Column G (index 6)
        'modification_reason': ('J', 5),  # Row 5, Column J (index 9)
        'second_validation_date': None,   # Not found in current structure
        'second_validator': None,         # Not found in current structure
    }
    
    def __init__(self, excel_reader: ExcelReader):
        """Initialize the extractor."""
        self.reader = excel_reader
    
    def _col_letter_to_index(self, col_letter: str) -> int:
        """Convert column letter to 0-based index."""
        col_num = 0
        for c in col_letter:
            col_num = col_num * 26 + (ord(c) - ord('A') + 1)
        return col_num - 1
    
    def extract_metadata(self, sheet_data: List[List[Any]]) -> Dict[str, Any]:
        """Extract metadata from rows 1, 4, and 5."""
        metadata = {}
        
        for field_name, field_info in self.METADATA_FIELDS.items():
            try:
                if field_info is None:
                    metadata[field_name] = None
                    continue
                
                col_letter, row_num = field_info
                col_idx = self._col_letter_to_index(col_letter)
                row_idx = row_num - 1  # Convert to 0-based
                
                if row_idx < len(sheet_data) and col_idx < len(sheet_data[row_idx]):
                    value = sheet_data[row_idx][col_idx]
                    
                    # Handle date fields
                    if 'date' in field_name and isinstance(value, (int, float)):
                        value = self.reader._excel_to_date(value)
                    elif value is not None:
                        value = str(value).strip()
                    
                    metadata[field_name] = value
                else:
                    metadata[field_name] = None
            except Exception as e:
                logger.warning(f"Error extracting {field_name}: {e}")
                metadata[field_name] = None
        
        return metadata
    
    def extract_instructions(self, sheet_data: List[List[Any]]) -> Tuple[str, List[str], List[str]]:
        """Extract instructions, special notes, and component references from rows 6+."""
        instruction_rows = []
        special_notes = []
        component_refs = []
        
        for idx in range(5, len(sheet_data)):  # Start from row 6 (index 5)
            row_data = sheet_data[idx]
            
            # Concatenate all non-empty cells in the row
            row_text = ' | '.join(
                str(cell).strip() 
                for cell in row_data 
                if cell is not None and str(cell).strip()
            )
            
            if row_text:
                instruction_rows.append(row_text)
                
                # Extract special notes
                row_str = str(row_text).upper()
                if any(keyword in row_str for keyword in ['ATTENTION', 'WARNING', 'IMPORTANT', 'DANGER']):
                    special_notes.append(row_text)
                
                # Extract component references (numbers with 6+ digits)
                refs = re.findall(r'\b\d{6,}\b', row_text)
                component_refs.extend(refs)
        
        full_instructions = '\n'.join(instruction_rows)
        component_refs = list(set(component_refs))  # Remove duplicates
        
        return full_instructions, special_notes, component_refs
    
    def extract_cable_data(self, sheet_name: str) -> Dict[str, Any]:
        """Extract all 14 data items from a cable sheet."""
        try:
            # Read the sheet
            sheet_data = self.reader.read_sheet(sheet_name)
            
            if not sheet_data:
                logger.error(f"No data found in sheet {sheet_name}")
                return None
            
            # Extract metadata
            metadata = self.extract_metadata(sheet_data)
            
            # Extract content
            full_instructions, special_notes, component_refs = self.extract_instructions(sheet_data)
            
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
            import traceback
            traceback.print_exc()
            return None


def ingest_excel_file(excel_path: str) -> Dict[str, Dict[str, Any]]:
    """
    Main function to ingest Excel file and extract all cable data.
    
    Args:
        excel_path: Path to dossier_cables.xlsx
        
    Returns:
        Dictionary with all extracted cable data
    """
    reader = ExcelReader(excel_path)
    
    if not reader.load():
        logger.error("Failed to load Excel file")
        return {}
    
    extractor = CableDataExtractor(reader)
    all_cables = {}
    
    for sheet_name in reader.sheet_names:
        logger.info(f"Extracting data from sheet: {sheet_name}")
        cable_data = extractor.extract_cable_data(sheet_name)
        
        if cable_data:
            # Use cable reference as key if available
            cable_ref = cable_data.get('cable_reference')
            if cable_ref:
                all_cables[cable_ref] = cable_data
            else:
                all_cables[sheet_name] = cable_data
    
    reader.close()
    logger.info(f"Successfully extracted data from {len(all_cables)} cables")
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
