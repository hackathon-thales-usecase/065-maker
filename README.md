# Thales065Maker

Automated system for generating 065 documents for Thales cable manufacturers from Excel data.

## Quick Start

```bash
python3 src/main.py
```

This will:
1. Read `inputs/dossier_cables.xlsx`
2. Extract cable data
3. Build `database/cables_data.json`
4. Generate 10 HTML documents in `outputs/065_documents/`

## Documentation

All documentation is organized in the `docs/` directory:

| File | Purpose |
|------|---------|
| [01_QUICKSTART.md](docs/01_QUICKSTART.md) | Get started in 5 minutes |
| [02_IMPLEMENTATION_GUIDE.md](docs/02_IMPLEMENTATION_GUIDE.md) | Technical architecture and design |
| [03_PROJECT_SUMMARY.md](docs/03_PROJECT_SUMMARY.md) | Project completion status and results |
| [04_COMPLETE_README.md](docs/04_COMPLETE_README.md) | Comprehensive overview |
| [05_PROJECT_INDEX.md](docs/05_PROJECT_INDEX.md) | Project structure and navigation |
| [06_ANALYSIS_SUMMARY.md](docs/06_ANALYSIS_SUMMARY.md) | Data analysis findings |
| [07_DATA_EXTRACTION_REQUIREMENTS.md](docs/07_DATA_EXTRACTION_REQUIREMENTS.md) | Data extraction specifications |
| [08_EXTRACTION_CHECKLIST.txt](docs/08_EXTRACTION_CHECKLIST.txt) | Processing checklist |

## Project Structure

```
065-maker/
├── inputs/                          # Input data
│   ├── dossier_cables.xlsx         # Excel file with cable data
│   ├── example_065_template.pdf    # Reference document
│   └── [cable_types]/              # Reference documents
├── database/                        # Generated database
│   └── cables_data.json            # Normalized cable data
├── outputs/                         # Generated documents
│   └── 065_documents/              # 065 HTML documents
├── src/                             # Source code
│   ├── main.py                     # Main orchestrator
│   ├── excel_reader.py             # Excel ingestion
│   ├── database.py                 # Database management
│   └── document_generator.py       # Document generation
├── docs/                            # Documentation
│   ├── 01_QUICKSTART.md
│   ├── 02_IMPLEMENTATION_GUIDE.md
│   ├── 03_PROJECT_SUMMARY.md
│   ├── 04_COMPLETE_README.md
│   ├── 05_PROJECT_INDEX.md
│   ├── 06_ANALYSIS_SUMMARY.md
│   ├── 07_DATA_EXTRACTION_REQUIREMENTS.md
│   └── 08_EXTRACTION_CHECKLIST.txt
└── README.md                        # This file
```

## Features

✅ **No External Dependencies** - Uses only Python standard library  
✅ **Robust Data Extraction** - Handles French text and Excel dates  
✅ **Professional Documents** - Color-coded HTML with styling  
✅ **Extensible Architecture** - Modular, well-documented code  

## Results

- **Cables Processed**: 10 out of 14 sheets
- **Documents Generated**: 10 HTML documents
- **Database Size**: 15 KB (JSON)
- **Processing Time**: < 5 seconds

## Usage

### Generate HTML Documents (Default)
```bash
python3 src/main.py
```

### Generate PDF Documents
```bash
python3 src/main.py --pdf
```

### Use Custom Paths
```bash
python3 src/main.py --excel /path/to/cables.xlsx --output /path/to/output
```

### View Help
```bash
python3 src/main.py --help
```

## System Requirements

- Python 3.6 or higher
- 50 MB RAM
- 100 MB disk space

## Getting Started

1. **Read the Quick Start**: [docs/01_QUICKSTART.md](docs/01_QUICKSTART.md)
2. **Run the workflow**: `python3 src/main.py`
3. **View generated documents**: Open `outputs/065_documents/*.html` in a browser
4. **Check the database**: View `database/cables_data.json`

## Documentation Guide

- **New to the project?** Start with [01_QUICKSTART.md](docs/01_QUICKSTART.md)
- **Need technical details?** See [02_IMPLEMENTATION_GUIDE.md](docs/02_IMPLEMENTATION_GUIDE.md)
- **Want project status?** Check [03_PROJECT_SUMMARY.md](docs/03_PROJECT_SUMMARY.md)
- **Need complete overview?** Read [04_COMPLETE_README.md](docs/04_COMPLETE_README.md)
- **Looking for structure?** See [05_PROJECT_INDEX.md](docs/05_PROJECT_INDEX.md)

## Support

For questions or issues, refer to the appropriate documentation file or check the inline code comments.

## Version

**v1.0** - Initial implementation (2026-09-30)

---

**Status**: ✅ Production Ready
