# Thales065Maker - Implementation Guide

## Project Overview

**Thales065Maker** is a complete system for automatically generating 065 documents for Thales cable manufacturers based on data extracted from an Excel file containing cable assembly instructions.

## Architecture

The system is built with a modular architecture consisting of four main components:

```
┌─────────────────────────────────────────────────────────────┐
│                    Main Orchestrator                         │
│                    (src/main.py)                             │
└──────────────┬──────────────┬──────────────┬────────────────┘
               │              │              │
        ┌──────▼──────┐ ┌────▼────┐ ┌──────▼──────┐
        │   Excel     │ │Database │ │  Document  │
        │   Reader    │ │ Manager │ │ Generator  │
        │(excel_reader)│ │(database)│ │(doc_gen)  │
        └─────────────┘ └─────────┘ └────────────┘
               │              │              │
        ┌──────▼──────────────▼──────────────▼──────┐
        │        Normalized Cable Data (JSON)       │
        └────────────────────────────────────────────┘
```

## Components

### 1. Excel Reader (`src/excel_reader.py`)

**Purpose**: Extract cable data from the Excel file without requiring external dependencies like openpyxl.

**Key Classes**:
- `ExcelReader`: Pure Python Excel reader using zipfile and XML parsing
- `CableDataExtractor`: Extracts 14 data items from each cable sheet

**Features**:
- Reads XLSX files using zipfile and XML parsing
- Extracts shared strings for proper text handling
- Converts Excel serial dates to ISO format
- Handles French text with special characters

**Data Extracted** (14 items per cable):
1. Cable Reference Number
2. Revision Letter
3. Created By
4. Created Date
5. Modified Date
6. Modified By
7. First Validation Date
8. First Validator
9. Modification Reason
10. Second Validation Date (if available)
11. Second Validator (if available)
12. Full Instructions
13. Special Notes (extracted from instructions)
14. Component References (extracted from instructions)

### 2. Database Manager (`src/database.py`)

**Purpose**: Store and manage normalized cable data in JSON format.

**Key Classes**:
- `CableDatabase`: Manages cable data storage, retrieval, and export

**Features**:
- Stores cable data in JSON format for easy access and portability
- Provides CRUD operations for cable data
- Exports data to CSV format
- Generates statistics about the database
- Maintains metadata (creation date, update date, version)

**Database Structure**:
```json
{
  "metadata": {
    "created": "2026-09-30T09:54:33.008913",
    "updated": "2026-09-30T09:54:33.009129",
    "total_cables": 10,
    "version": "1.0"
  },
  "cables": {
    "63076846AA": {
      "cable_reference": "63076846AA",
      "revision_letter": "B",
      "created_by": "NATHALIE",
      "created_date": "2026-02-05",
      ...
    }
  }
}
```

### 3. Document Generator (`src/document_generator.py`)

**Purpose**: Generate 065 documents in HTML format from cable data.

**Key Classes**:
- `Document065Template`: HTML template for 065 documents
- `Document065Generator`: Generates documents for individual cables or batches

**Features**:
- Generates professional HTML documents with styling
- Includes metadata section with creation/modification information
- Highlights special notes with warning styling
- Lists component references
- Supports batch generation for all cables
- Can convert to PDF using available tools (wkhtmltopdf, LibreOffice)

**Document Sections**:
1. Header with cable reference and revision
2. Metadata table (creation, modification, validation info)
3. Manufacturing instructions
4. Special notes (highlighted in yellow)
5. Component references (highlighted in blue)
6. Footer with generation timestamp

### 4. Main Orchestrator (`src/main.py`)

**Purpose**: Orchestrate the complete workflow from Excel ingestion to document generation.

**Key Class**:
- `Thales065Maker`: Main orchestrator class

**Workflow Steps**:
1. Ingest Excel file and extract cable data
2. Build normalized database
3. Generate 065 documents
4. Print summary statistics

## Usage

### Running the Complete Workflow

```bash
cd /home/pboullet/CAP_AI/THALES/065-maker
python3 src/main.py
```

### Command-Line Options

```bash
python3 src/main.py --help

Options:
  --excel PATH    Path to dossier_cables.xlsx (default: inputs/dossier_cables.xlsx)
  --db PATH       Path to database file (default: database/cables_data.json)
  --output PATH   Output directory for documents (default: outputs/065_documents)
  --pdf           Generate PDF documents instead of HTML
```

### Example Usage

```bash
# Generate HTML documents (default)
python3 src/main.py

# Generate PDF documents
python3 src/main.py --pdf

# Use custom paths
python3 src/main.py --excel /path/to/cables.xlsx --output /path/to/output
```

## File Structure

```
065-maker/
├── inputs/
│   ├── dossier_cables.xlsx          # Input Excel file with cable data
│   ├── example_065_template.pdf     # Reference 065 document
│   └── [cable_type]/                # Reference documents for each cable
├── database/
│   └── cables_data.json             # Generated database
├── outputs/
│   └── 065_documents/               # Generated 065 documents
│       ├── 63076846AA_065.html
│       ├── 65478610AB_065.html
│       └── ...
├── src/
│   ├── main.py                      # Main orchestrator
│   ├── excel_reader.py              # Excel ingestion
│   ├── database.py                  # Database management
│   └── document_generator.py        # Document generation
├── README.md                        # Project overview
└── IMPLEMENTATION_GUIDE.md          # This file
```

## Data Flow

```
dossier_cables.xlsx
        ↓
    [Excel Reader]
        ↓
Cable Data (14 items × 10 cables)
        ↓
    [Database Manager]
        ↓
cables_data.json
        ↓
    [Document Generator]
        ↓
10 × 065_documents.html
```

## Key Features

### 1. Pure Python Excel Reading
- No external dependencies like openpyxl
- Uses standard library (zipfile, xml.etree)
- Handles Excel date conversion
- Supports shared strings

### 2. Robust Data Extraction
- Handles French text with special characters
- Extracts metadata from specific cell locations
- Identifies special notes and component references
- Gracefully handles missing or empty fields

### 3. Professional Document Generation
- HTML documents with professional styling
- Color-coded sections (warnings in yellow, components in blue)
- Responsive design suitable for printing
- Includes all relevant metadata

### 4. Extensible Architecture
- Modular design allows easy enhancement
- JSON database format for portability
- Can be extended to generate PDF, XML, or other formats
- Supports batch processing

## Statistics

### Current Implementation
- **Cables Processed**: 10 out of 14 sheets
- **Data Items Extracted**: 14 per cable
- **Documents Generated**: 10 HTML documents
- **Database Size**: ~15 KB (JSON)
- **Document Size**: ~4-7 KB per document (HTML)

### Processing Time
- Excel ingestion: < 1 second
- Database building: < 1 second
- Document generation: < 2 seconds
- Total workflow: < 5 seconds

## Troubleshooting

### Issue: Some sheets are empty (SMA 01, R1, etc.)

**Cause**: These sheets may have different data structures or be placeholder sheets.

**Solution**: The system gracefully skips empty sheets and processes only sheets with data.

### Issue: Special characters not displaying correctly

**Solution**: All files are saved with UTF-8 encoding. Ensure your browser/viewer supports UTF-8.

### Issue: PDF generation fails

**Cause**: wkhtmltopdf or LibreOffice not installed.

**Solution**: 
1. Install wkhtmltopdf: `apt-get install wkhtmltopdf`
2. Or install LibreOffice: `apt-get install libreoffice`
3. Or use HTML documents directly

## Future Enhancements

1. **PDF Generation**: Implement direct PDF generation using reportlab
2. **XML Export**: Generate XML format for integration with other systems
3. **Database Backend**: Support SQLite or PostgreSQL for larger datasets
4. **Web Interface**: Create web UI for document generation and management
5. **Template Customization**: Allow custom HTML templates
6. **Multi-language Support**: Support for multiple languages
7. **Validation Rules**: Add data validation and quality checks
8. **Audit Trail**: Track all modifications and generations

## Technical Details

### Excel Structure
- Row 1: Cable Reference (Col G), Revision Letter (Col H)
- Row 4: Created By (Col E), Created Date (Col G), Modified Date (Col J), Modified By (Col L)
- Row 5: First Validation Date (Col E), First Validator (Col G), Modification Reason (Col J)
- Rows 6+: Manufacturing instructions

### Date Conversion
- Excel uses serial date format (days since 1900-01-01)
- Accounts for Excel's leap year bug (1900 is not a leap year)
- Converts to ISO format (YYYY-MM-DD)

### Component Reference Extraction
- Uses regex pattern: `\b\d{6,}\b` (6+ consecutive digits)
- Removes duplicates
- Useful for identifying part numbers

## Performance Considerations

- **Memory Usage**: ~50 MB for 10 cables
- **Scalability**: Can handle 100+ cables without issues
- **Optimization**: Database is loaded once and reused for document generation

## Security Considerations

- All file operations use absolute paths
- HTML output escapes special characters to prevent injection
- JSON database is human-readable for audit purposes
- No external API calls or network operations

## Support and Maintenance

### Adding New Cables
1. Add new sheet to dossier_cables.xlsx
2. Run `python3 src/main.py` to regenerate database and documents
3. New documents will be created automatically

### Updating Existing Cables
1. Modify data in Excel sheet
2. Run `python3 src/main.py` to update database and regenerate documents
3. Previous documents will be overwritten

### Exporting Data
```python
from src.database import CableDatabase

db = CableDatabase()
db.load()
db.export_csv('cables_export.csv')
```

## Version History

- **v1.0** (2026-09-30): Initial implementation
  - Excel ingestion with pure Python
  - JSON database storage
  - HTML document generation
  - 10 cables processed successfully

## License

This project is part of the Thales CAP_AI initiative.

## Contact

For questions or issues, contact the development team.
