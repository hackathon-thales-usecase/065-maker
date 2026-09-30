#!/usr/bin/env python3
"""
Thales065Maker - Main Orchestration Script

Orchestrates the complete workflow:
1. Ingest Excel file
2. Build database
3. Generate 065 documents
"""

import sys
import logging
from pathlib import Path
from datetime import datetime

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from excel_reader import ingest_excel_file
from database import CableDatabase
from document_generator import Document065Generator

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class Thales065Maker:
    """Main orchestrator for the 065 document generation workflow."""
    
    def __init__(self, excel_path: str, db_path: str = None, output_dir: str = None):
        """
        Initialize the maker.
        
        Args:
            excel_path: Path to dossier_cables.xlsx
            db_path: Path to database file (optional)
            output_dir: Output directory for documents (optional)
        """
        self.excel_path = excel_path
        self.db_path = db_path or '/home/pboullet/CAP_AI/THALES/065-maker/database/cables_data.json'
        self.output_dir = output_dir or '/home/pboullet/CAP_AI/THALES/065-maker/outputs/065_documents'
        
        self.database = None
        self.generator = None
        self.results = {}
    
    def run(self, generate_pdf: bool = False) -> bool:
        """
        Run the complete workflow.
        
        Args:
            generate_pdf: Whether to generate PDF documents (default: False)
            
        Returns:
            True if successful
        """
        try:
            logger.info("=" * 60)
            logger.info("Thales065Maker - Starting workflow")
            logger.info("=" * 60)
            
            # Step 1: Ingest Excel file
            logger.info("\n[Step 1/4] Ingesting Excel file...")
            cables = self._ingest_excel()
            if not cables:
                logger.error("Failed to ingest Excel file")
                return False
            
            # Step 2: Build database
            logger.info("\n[Step 2/4] Building database...")
            self._build_database(cables)
            if not self.database:
                logger.error("Failed to build database")
                return False
            
            # Step 3: Generate documents
            logger.info("\n[Step 3/4] Generating 065 documents...")
            doc_format = 'pdf' if generate_pdf else 'html'
            self._generate_documents(doc_format)
            
            # Step 4: Print summary
            logger.info("\n[Step 4/4] Generating summary...")
            self._print_summary()
            
            logger.info("\n" + "=" * 60)
            logger.info("Workflow completed successfully!")
            logger.info("=" * 60)
            
            return True
        except Exception as e:
            logger.error(f"Workflow failed: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _ingest_excel(self) -> dict:
        """Ingest Excel file and return cable data."""
        try:
            logger.info(f"Reading Excel file: {self.excel_path}")
            cables = ingest_excel_file(self.excel_path)
            logger.info(f"Successfully ingested {len(cables)} cables")
            return cables
        except Exception as e:
            logger.error(f"Failed to ingest Excel file: {e}")
            return {}
    
    def _build_database(self, cables: dict) -> bool:
        """Build database from cable data."""
        try:
            logger.info(f"Creating database at: {self.db_path}")
            self.database = CableDatabase(self.db_path)
            self.database.metadata['created'] = datetime.now().isoformat()
            
            logger.info(f"Adding {len(cables)} cables to database...")
            count = self.database.add_cables(cables)
            
            logger.info(f"Saving database...")
            self.database.save()
            
            # Print statistics
            stats = self.database.get_statistics()
            logger.info(f"Database statistics:")
            for key, value in stats.items():
                logger.info(f"  {key}: {value}")
            
            return True
        except Exception as e:
            logger.error(f"Failed to build database: {e}")
            return False
    
    def _generate_documents(self, format: str = 'html') -> bool:
        """Generate 065 documents."""
        try:
            logger.info(f"Creating document generator...")
            self.generator = Document065Generator(self.output_dir)
            
            cables = self.database.get_all_cables()
            logger.info(f"Generating {len(cables)} {format.upper()} documents...")
            
            self.results = self.generator.generate_all(cables, format)
            
            # Print statistics
            stats = self.generator.get_statistics()
            logger.info(f"Generation statistics:")
            for key, value in stats.items():
                logger.info(f"  {key}: {value}")
            
            return True
        except Exception as e:
            logger.error(f"Failed to generate documents: {e}")
            return False
    
    def _print_summary(self) -> None:
        """Print workflow summary."""
        logger.info("\n" + "=" * 60)
        logger.info("WORKFLOW SUMMARY")
        logger.info("=" * 60)
        
        if self.database:
            stats = self.database.get_statistics()
            logger.info(f"\nDatabase:")
            logger.info(f"  Total cables: {stats['total_cables']}")
            logger.info(f"  Cables with instructions: {stats['cables_with_instructions']}")
            logger.info(f"  Cables with special notes: {stats['cables_with_special_notes']}")
            logger.info(f"  Cables with component refs: {stats['cables_with_component_refs']}")
        
        if self.generator:
            stats = self.generator.get_statistics()
            logger.info(f"\nDocuments Generated:")
            logger.info(f"  HTML documents: {stats['html_documents']}")
            logger.info(f"  PDF documents: {stats['pdf_documents']}")
            logger.info(f"  Total documents: {stats['total_documents']}")
            logger.info(f"  Output directory: {stats['output_directory']}")
        
        logger.info(f"\nDatabase file: {self.db_path}")
        logger.info(f"Output directory: {self.output_dir}")
        logger.info("=" * 60)


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Thales065Maker - Generate 065 documents for cable manufacturers'
    )
    parser.add_argument(
        '--excel',
        default='/home/pboullet/CAP_AI/THALES/065-maker/inputs/dossier_cables.xlsx',
        help='Path to dossier_cables.xlsx'
    )
    parser.add_argument(
        '--db',
        default='/home/pboullet/CAP_AI/THALES/065-maker/database/cables_data.json',
        help='Path to database file'
    )
    parser.add_argument(
        '--output',
        default='/home/pboullet/CAP_AI/THALES/065-maker/outputs/065_documents',
        help='Output directory for documents'
    )
    parser.add_argument(
        '--pdf',
        action='store_true',
        help='Generate PDF documents (default: HTML)'
    )
    
    args = parser.parse_args()
    
    # Create and run maker
    maker = Thales065Maker(
        excel_path=args.excel,
        db_path=args.db,
        output_dir=args.output
    )
    
    success = maker.run(generate_pdf=args.pdf)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
