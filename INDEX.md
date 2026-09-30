# Thales065Maker - Project Index

## Project Overview

**Thales065Maker** is a system to automatically generate 065 documents for Thales cable manufacturers based on data extracted from an Excel file containing cable assembly instructions.

## Workflow

```
dossier_cables.xlsx (14 sheets)
        ↓
    [INGEST]
        ↓
Extract 14 data items per cable
        ↓
    [STORE]
        ↓
Normalized database
        ↓
    [TEMPLATE]
        ↓
065 document template
        ↓
    [GENERATE]
        ↓
14 × 065 documents (one per cable type)
```

## Documentation Files

### 1. **README.md**
   - Project description
   - Workflow overview
   - High-level process steps

### 2. **DATA_EXTRACTION_REQUIREMENTS.md**
   - Detailed specifications for all 14 data items
   - Field locations (row/column references)
   - Data types and examples
   - Quality notes and validation rules

### 3. **EXTRACTION_CHECKLIST.txt**
   - Complete checklist of all 14 data items
   - Processing workflow (5 steps)
   - Cable types to process (14 total)
   - Data validation rules

### 4. **ANALYSIS_SUMMARY.md**
   - Executive summary of findings
   - File structure and characteristics
   - Data quality notes
   - Example data from cable 63076846AA

### 5. **INDEX.md** (this file)
   - Project overview and navigation
   - File descriptions
   - Quick reference

## Data Items to Extract (14 Total)

### Metadata (11 items from header rows 1-4)

| # | Field | Location | Type | Required |
|---|-------|----------|------|----------|
| 1 | Cable Reference Number | R1:F1 | String | YES |
| 2 | Revision Letter | R1:G1 | String | YES |
| 3 | Created By | R2:B2 | String | NO |
| 4 | Created Date | R2:D2 | Date | NO |
| 5 | Modified Date | R2:F2 | Date | NO |
| 6 | Modified By | R2:H2 | String | NO |
| 7 | First Validation Date | R3:B3 | Date | NO |
| 8 | First Validator | R3:D3 | String | NO |
| 9 | Modification Reason | R3:F3 | String | NO |
| 10 | Second Validation Date | R4:B4 | Date | NO |
| 11 | Second Validator | R4:D4 | String | NO |

### Content (3 items from rows 5+)

| # | Field | Location | Type | Required |
|---|-------|----------|------|----------|
| 12 | Full Instructions | R5:* | Text | YES |
| 13 | Special Notes | Extracted | Text | NO |
| 14 | Component References | Extracted | List | NO |

## Cable Types (14 sheets)

1. **63076846AA** - CABLE RX VHF W1
2. **65478610AB** - LOT DE 6 CABLES W1XX
3. **SMA 01** - SMA 01
4. **R1** - R1
5. **68935000BA** - W2402E
6. **61226725AA** - Lot de câble de sortie
7. **45351183** - 45351183
8. **45351184** - 45351184
9. **67225776AA** - 67225776AA
10. **65221558AA - 65221562** - AEA
11. **21-33122-546** - 21-33122-546
12. **6162-233-1277** - 6162-233-1277
13. **5669133A** - Lot de cordon 20160
14. **63476500BA** - CABLE IO

## Input Files

### Main Input
- **inputs/dossier_cables.xlsx** - Excel file with 14 sheets (one per cable type)

### Reference Files
- **inputs/example_065_template.pdf** - Example 065 document (target format)
- **inputs/[cable_type]/*.pdf** - Reference documents for each cable type

## Output Structure (To Be Created)

```
outputs/
├── database/
│   └── cables_data.json          # Normalized database
├── 065_documents/
│   ├── 63076846AA_065.pdf
│   ├── 65478610AB_065.pdf
│   ├── SMA_01_065.pdf
│   └── ... (14 total)
└── logs/
    └── generation_report.txt
```

## Processing Steps

### Step 1: Data Ingestion
- Read dossier_cables.xlsx
- Extract all 14 sheets
- Parse metadata (rows 1-4) and content (rows 5+)

### Step 2: Data Normalization
- Convert Excel dates to standard format
- Clean and validate text content
- Extract special notes and component references

### Step 3: Database Building
- Store normalized data in reusable format
- Create structured database (JSON/SQLite)
- Ensure data integrity

### Step 4: Template Creation
- Create 065 document template
- Map database fields to template placeholders
- Define output format (PDF/XML)

### Step 5: Document Generation
- Generate 065 document for each cable
- Populate with extracted data
- Save to outputs directory

## Key Characteristics

### Data Format
- **Language**: French with special characters (accents: é, è, ê, ç)
- **Dates**: Excel serial format (need conversion)
- **Text**: Multi-line instructions with technical terminology

### Data Quality
- **Required Fields**: Cable Reference, Revision Letter, Full Instructions
- **Optional Fields**: 8 metadata fields may be empty
- **Validation**: Dates must be valid Excel serial numbers

## Quick Reference

### File Locations
```
Repository: /home/pboullet/CAP_AI/THALES/Thales065Maker/
Excel File: inputs/dossier_cables.xlsx
Example 065: inputs/example_065_template.pdf
```

### Documentation
```
DATA_EXTRACTION_REQUIREMENTS.md  - Detailed specifications
EXTRACTION_CHECKLIST.txt         - Checklist and workflow
ANALYSIS_SUMMARY.md              - Executive summary
INDEX.md                         - This file
```

## Next Steps

1. Review **DATA_EXTRACTION_REQUIREMENTS.md** for detailed field specifications
2. Check **EXTRACTION_CHECKLIST.txt** for processing workflow
3. Implement data ingestion pipeline
4. Build normalized database
5. Create 065 document template
6. Generate 065 documents for all 14 cables

---

**Project Status**: Analysis Complete ✓  
**Date**: 2026-09-29  
**Ready for**: Implementation Phase
