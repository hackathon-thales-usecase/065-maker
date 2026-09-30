# Data Extraction Requirements - dossier_cables.xlsx

## Overview

The Excel file `dossier_cables.xlsx` contains 14 sheets, one for each cable type. Each sheet follows a consistent structure with metadata in the header (rows 1-4) and detailed manufacturing instructions in the content section (rows 5+).

## Data Structure

### Section 1: Metadata (Header - Rows 1-4)

The first 4 rows of each sheet contain standardized metadata about the cable and its documentation history.

| # | Field Name | Location | Type | Required | Example |
|---|---|---|---|---|---|
| 1 | Cable Reference Number | R1:F1 | String | YES | 63076846AA |
| 2 | Revision Letter | R1:G1 | String | YES | B |
| 3 | Created By | R2:B2 | String | NO | NATHALIE |
| 4 | Created Date | R2:D2 | Date | NO | 46057 (Excel serial) |
| 5 | Modified Date | R2:F2 | Date | NO | 46182 (Excel serial) |
| 6 | Modified By | R2:H2 | String | NO | ségolène |
| 7 | First Validation Date | R3:B3 | Date | NO | 46176 (Excel serial) |
| 8 | First Validator | R3:D3 | String | NO | Heïdi |
| 9 | Modification Reason | R3:F3 | String | NO | changement de calibre |
| 10 | Second Validation Date | R4:B4 | Date | NO | (optional) |
| 11 | Second Validator | R4:D4 | String | NO | (optional) |

### Section 2: Content (Rows 5+)

Detailed cable assembly and manufacturing instructions.

| # | Field Name | Location | Type | Required | Content |
|---|---|---|---|---|---|
| 12 | Full Instructions | R5:* | Multi-line Text | YES | Step-by-step assembly instructions, technical specs, dimensions, materials, tools, QC notes, warnings |
| 13 | Special Notes | Extracted | Text | NO | Lines starting with ATTENTION, REPRENDRE, VOIR, etc. |
| 14 | Component References | Extracted | List | NO | Reference numbers (e.g., 91624771, 45351183) |

## Cable Types (14 Sheets)

1. **63076846AA** - CABLE RX VHF W1
2. **65478610AB** - LOT DE 6 CABLES W1XX
3. **SMA 01**
4. **R1**
5. **68935000BA** - W2402E
6. **61226725AA** - Lot de câble de sortie
7. **45351183**
8. **45351184**
9. **67225776AA**
10. **65221558AA - 65221562** - AEA
11. **21-33122-546**
12. **6162-233-1277**
13. **5669133A** - Lot de cordon 20160
14. **63476500BA** - CABLE IO

## Data Quality Notes

- **Dates**: Stored as Excel serial numbers (need conversion to standard date format)
- **Optional Fields**: Many metadata fields may be empty
- **Language**: Content is in French with special characters (accents, etc.)
- **Text Length**: Instructions vary from 8 rows to 32+ rows per cable
- **References**: Component references are embedded within instruction text

## Example Data

### Sheet: 63076846AA (CABLE RX VHF W1)

**Metadata:**
- Cable Reference: 63076846AA
- Revision: B
- Created By: NATHALIE
- Created Date: 46057
- Modified Date: 46182
- Modified By: ségolène
- First Validation Date: 46176
- First Validator: Heïdi
- Modification Reason: changement de calibre

**Instructions (excerpt):**
- VOIR POUR LES PREMIERS AVEC NATH
- ATTENTION le calibre a été refait a neuf (blanc) | Trait rouge coupe du semi rigide
- GOUPILLE
- Prendre le câble semi rigide 91624771
- Penser à enlever la goupille (rond blanc) pour cou...
- [32 rows total of detailed instructions]

## Next Steps

1. **Ingest**: Read all 14 sheets and extract the 14 data items per cable
2. **Store**: Build a database with normalized data
3. **Template**: Create 065 document template using extracted data
4. **Generate**: Produce 065 documents for each cable type
