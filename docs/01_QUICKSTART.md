# Quick Start Guide - Thales065Maker

## Installation

No additional dependencies required! The system uses only Python standard library.

```bash
cd /home/pboullet/CAP_AI/THALES/065-maker
```

## Running the Workflow

### Option 1: Generate HTML Documents (Recommended)

```bash
python3 src/main.py
```

This will:
1. Read the Excel file (`inputs/dossier_cables.xlsx`)
2. Extract cable data
3. Build a database (`database/cables_data.json`)
4. Generate HTML documents (`outputs/065_documents/`)

### Option 2: Generate PDF Documents

```bash
python3 src/main.py --pdf
```

Note: Requires wkhtmltopdf or LibreOffice to be installed.

## Output Files

After running the workflow, you'll find:

- **Database**: `database/cables_data.json` - All extracted cable data in JSON format
- **Documents**: `outputs/065_documents/*.html` - Generated 065 documents

## Viewing Documents

### HTML Documents
Open any HTML file in a web browser:
```bash
firefox outputs/065_documents/63076846AA_065.html
```

Or convert to PDF using your browser's print function (Ctrl+P → Save as PDF).

## Understanding the Output

Each generated document contains:

1. **Header**: Cable reference and revision number
2. **Metadata**: Creation, modification, and validation information
3. **Instructions**: Step-by-step manufacturing instructions
4. **Special Notes**: Important warnings and special handling (yellow background)
5. **Component References**: Part numbers and component IDs (blue background)

## Troubleshooting

### Issue: "No module named 'excel_reader'"
**Solution**: Make sure you're running from the project root directory:
```bash
cd /home/pboullet/CAP_AI/THALES/065-maker
python3 src/main.py
```

### Issue: Excel file not found
**Solution**: Verify the Excel file exists:
```bash
ls -l inputs/dossier_cables.xlsx
```

### Issue: Permission denied
**Solution**: Ensure write permissions for output directories:
```bash
chmod -R 755 database outputs
```

## Next Steps

1. **Review Generated Documents**: Open HTML files in a browser
2. **Check Database**: View `database/cables_data.json` for extracted data
3. **Customize**: Modify `src/document_generator.py` to change document styling
4. **Integrate**: Use the database JSON for integration with other systems

## Advanced Usage

### Using the Modules Directly

```python
from src.excel_reader import ingest_excel_file
from src.database import CableDatabase
from src.document_generator import Document065Generator

# Ingest Excel
cables = ingest_excel_file('inputs/dossier_cables.xlsx')

# Build database
db = CableDatabase()
db.add_cables(cables)
db.save()

# Generate documents
gen = Document065Generator()
results = gen.generate_all(cables, format='html')
```

### Exporting to CSV

```python
from src.database import CableDatabase

db = CableDatabase()
db.load()
db.export_csv('cables_export.csv')
```

## Performance

- **Total Processing Time**: ~5 seconds
- **Database Size**: ~15 KB
- **Document Size**: ~4-7 KB each
- **Memory Usage**: ~50 MB

## Support

For detailed information, see:
- `README.md` - Project overview
- `IMPLEMENTATION_GUIDE.md` - Technical details
- `INDEX.md` - Project structure and navigation

---

**Ready to generate your 065 documents?**

```bash
python3 src/main.py
```

Enjoy! 🚀
