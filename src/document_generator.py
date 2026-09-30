"""
065 Document Generator for Thales Cable Manufacturers

Generates 065 documents from cable data using HTML templates.
"""

import logging
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime
import html

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Document065Template:
    """Template for 065 documents."""
    
    @staticmethod
    def generate_html(cable_data: Dict[str, Any]) -> str:
        """
        Generate HTML content for a 065 document.
        
        Args:
            cable_data: Cable data from database
            
        Returns:
            HTML string
        """
        # Escape HTML special characters
        def esc(text):
            if text is None:
                return ''
            return html.escape(str(text))
        
        # Format instructions with line breaks
        instructions = cable_data.get('full_instructions', '')
        instructions_html = '<br>'.join(
            f'<p>{esc(line)}</p>' 
            for line in instructions.split('\n') 
            if line.strip()
        )
        
        # Format special notes
        special_notes = cable_data.get('special_notes', [])
        special_notes_html = ''
        if special_notes:
            special_notes_html = '<div class="special-notes"><h3>Notes Spéciales</h3><ul>'
            for note in special_notes:
                special_notes_html += f'<li>{esc(note)}</li>'
            special_notes_html += '</ul></div>'
        
        # Format component references
        component_refs = cable_data.get('component_references', [])
        component_refs_html = ''
        if component_refs:
            component_refs_html = '<div class="component-refs"><h3>Références de Composants</h3><ul>'
            for ref in component_refs:
                component_refs_html += f'<li>{esc(ref)}</li>'
            component_refs_html += '</ul></div>'
        
        # Build metadata section
        metadata_html = '<div class="metadata"><table>'
        
        if cable_data.get('created_by'):
            metadata_html += f'<tr><td>Créé par:</td><td>{esc(cable_data.get("created_by"))}</td></tr>'
        
        if cable_data.get('created_date'):
            metadata_html += f'<tr><td>Date de création:</td><td>{esc(cable_data.get("created_date"))}</td></tr>'
        
        if cable_data.get('modified_by'):
            metadata_html += f'<tr><td>Modifié par:</td><td>{esc(cable_data.get("modified_by"))}</td></tr>'
        
        if cable_data.get('modified_date'):
            metadata_html += f'<tr><td>Date de modification:</td><td>{esc(cable_data.get("modified_date"))}</td></tr>'
        
        if cable_data.get('first_validator'):
            metadata_html += f'<tr><td>Validateur:</td><td>{esc(cable_data.get("first_validator"))}</td></tr>'
        
        if cable_data.get('first_validation_date'):
            metadata_html += f'<tr><td>Date de validation:</td><td>{esc(cable_data.get("first_validation_date"))}</td></tr>'
        
        if cable_data.get('modification_reason'):
            metadata_html += f'<tr><td>Motif de modification:</td><td>{esc(cable_data.get("modification_reason"))}</td></tr>'
        
        metadata_html += '</table></div>'
        
        # Build complete HTML document
        html_content = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document 065 - {esc(cable_data.get('cable_reference', 'Unknown'))}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            line-height: 1.6;
            color: #333;
        }}
        .header {{
            border-bottom: 3px solid #003366;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }}
        .header h1 {{
            margin: 0;
            color: #003366;
            font-size: 24px;
        }}
        .header .subtitle {{
            color: #666;
            font-size: 14px;
            margin-top: 5px;
        }}
        .metadata {{
            background-color: #f5f5f5;
            border: 1px solid #ddd;
            padding: 15px;
            margin-bottom: 20px;
            border-radius: 4px;
        }}
        .metadata table {{
            width: 100%;
            border-collapse: collapse;
        }}
        .metadata td {{
            padding: 8px;
            border-bottom: 1px solid #ddd;
        }}
        .metadata td:first-child {{
            font-weight: bold;
            width: 200px;
            background-color: #e8e8e8;
        }}
        .instructions {{
            background-color: #fff;
            border: 1px solid #ddd;
            padding: 15px;
            margin-bottom: 20px;
            border-radius: 4px;
        }}
        .instructions h2 {{
            color: #003366;
            border-bottom: 2px solid #003366;
            padding-bottom: 10px;
            margin-top: 0;
        }}
        .instructions p {{
            margin: 10px 0;
            padding: 8px;
            background-color: #fafafa;
            border-left: 3px solid #ddd;
            padding-left: 12px;
        }}
        .special-notes {{
            background-color: #fff3cd;
            border: 1px solid #ffc107;
            padding: 15px;
            margin-bottom: 20px;
            border-radius: 4px;
        }}
        .special-notes h3 {{
            color: #856404;
            margin-top: 0;
        }}
        .special-notes ul {{
            margin: 10px 0;
            padding-left: 20px;
        }}
        .special-notes li {{
            margin: 8px 0;
            color: #856404;
        }}
        .component-refs {{
            background-color: #d1ecf1;
            border: 1px solid #17a2b8;
            padding: 15px;
            margin-bottom: 20px;
            border-radius: 4px;
        }}
        .component-refs h3 {{
            color: #0c5460;
            margin-top: 0;
        }}
        .component-refs ul {{
            margin: 10px 0;
            padding-left: 20px;
        }}
        .component-refs li {{
            margin: 8px 0;
            color: #0c5460;
            font-family: monospace;
            font-weight: bold;
        }}
        .footer {{
            border-top: 1px solid #ddd;
            padding-top: 10px;
            margin-top: 30px;
            font-size: 12px;
            color: #666;
            text-align: center;
        }}
        @media print {{
            body {{
                margin: 0;
            }}
            .page-break {{
                page-break-after: always;
            }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Document 065 - Fabrication de Câbles</h1>
        <div class="subtitle">
            Référence: {esc(cable_data.get('cable_reference', 'N/A'))} | 
            Révision: {esc(cable_data.get('revision_letter', 'N/A'))}
        </div>
    </div>
    
    {metadata_html}
    
    <div class="instructions">
        <h2>Instructions de Fabrication</h2>
        {instructions_html}
    </div>
    
    {special_notes_html}
    
    {component_refs_html}
    
    <div class="footer">
        <p>Document généré automatiquement par Thales065Maker</p>
        <p>Généré le: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
</body>
</html>"""
        
        return html_content


class Document065Generator:
    """Generate 065 documents from cable data."""
    
    def __init__(self, output_dir: str = None):
        """
        Initialize the generator.
        
        Args:
            output_dir: Directory to save generated documents
        """
        if output_dir is None:
            output_dir = '/home/pboullet/CAP_AI/THALES/065-maker/outputs/065_documents'
        
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_html(self, cable_ref: str, cable_data: Dict[str, Any]) -> str:
        """
        Generate HTML document for a cable.
        
        Args:
            cable_ref: Cable reference number
            cable_data: Cable data from database
            
        Returns:
            Path to generated HTML file
        """
        try:
            # Generate HTML content
            html_content = Document065Template.generate_html(cable_data)
            
            # Save HTML file
            output_file = self.output_dir / f'{cable_ref}_065.html'
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            logger.info(f"Generated HTML document: {output_file}")
            return str(output_file)
        except Exception as e:
            logger.error(f"Failed to generate HTML for {cable_ref}: {e}")
            return None
    
    def generate_pdf(self, cable_ref: str, cable_data: Dict[str, Any]) -> Optional[str]:
        """
        Generate PDF document for a cable.
        
        Args:
            cable_ref: Cable reference number
            cable_data: Cable data from database
            
        Returns:
            Path to generated PDF file or None if failed
        """
        try:
            # First generate HTML
            html_file = self.generate_html(cable_ref, cable_data)
            if not html_file:
                return None
            
            # Try to convert HTML to PDF using available tools
            pdf_file = str(self.output_dir / f'{cable_ref}_065.pdf')
            
            # Try using wkhtmltopdf if available
            import subprocess
            try:
                result = subprocess.run(
                    ['wkhtmltopdf', html_file, pdf_file],
                    capture_output=True,
                    timeout=30
                )
                if result.returncode == 0:
                    logger.info(f"Generated PDF document: {pdf_file}")
                    return pdf_file
            except FileNotFoundError:
                logger.warning("wkhtmltopdf not found, trying alternative methods")
            
            # Try using libreoffice if available
            try:
                result = subprocess.run(
                    ['libreoffice', '--headless', '--convert-to', 'pdf', '--outdir', str(self.output_dir), html_file],
                    capture_output=True,
                    timeout=30
                )
                if result.returncode == 0:
                    logger.info(f"Generated PDF document: {pdf_file}")
                    return pdf_file
            except FileNotFoundError:
                logger.warning("libreoffice not found")
            
            # If PDF conversion fails, return HTML file path
            logger.warning(f"Could not convert to PDF, HTML file available at: {html_file}")
            return html_file
        except Exception as e:
            logger.error(f"Failed to generate PDF for {cable_ref}: {e}")
            return None
    
    def generate_all(self, cables: Dict[str, Dict[str, Any]], format: str = 'html') -> Dict[str, str]:
        """
        Generate documents for all cables.
        
        Args:
            cables: Dictionary of cable data
            format: Output format ('html' or 'pdf')
            
        Returns:
            Dictionary mapping cable references to output file paths
        """
        results = {}
        
        for cable_ref, cable_data in cables.items():
            logger.info(f"Generating {format.upper()} for {cable_ref}...")
            
            if format.lower() == 'pdf':
                output_file = self.generate_pdf(cable_ref, cable_data)
            else:
                output_file = self.generate_html(cable_ref, cable_data)
            
            if output_file:
                results[cable_ref] = output_file
        
        logger.info(f"Generated {len(results)} documents")
        return results
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get generation statistics."""
        html_files = list(self.output_dir.glob('*_065.html'))
        pdf_files = list(self.output_dir.glob('*_065.pdf'))
        
        return {
            'html_documents': len(html_files),
            'pdf_documents': len(pdf_files),
            'total_documents': len(html_files) + len(pdf_files),
            'output_directory': str(self.output_dir)
        }


def generate_065_documents(cables: Dict[str, Dict[str, Any]], output_dir: str = None, format: str = 'html') -> Dict[str, str]:
    """
    Generate 065 documents from cable data.
    
    Args:
        cables: Dictionary of cable data
        output_dir: Output directory (optional)
        format: Output format ('html' or 'pdf')
        
    Returns:
        Dictionary mapping cable references to output file paths
    """
    generator = Document065Generator(output_dir)
    results = generator.generate_all(cables, format)
    
    # Print statistics
    stats = generator.get_statistics()
    logger.info(f"Generation statistics: {stats}")
    
    return results


if __name__ == '__main__':
    # Test the generator
    from database import CableDatabase
    
    db = CableDatabase()
    db.load()
    
    cables = db.get_all_cables()
    
    print(f"\nGenerating 065 documents for {len(cables)} cables...")
    results = generate_065_documents(cables, format='html')
    
    print("\nGenerated documents:")
    for cable_ref, output_file in list(results.items())[:5]:
        print(f"  {cable_ref}: {output_file}")
