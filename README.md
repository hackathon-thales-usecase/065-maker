# Thales065Maker
Build 065 document for thales cables manufacturers based on heterogenous information

Workflow description
- Inputs from client regarding cable making instructions are stored in an Excel file named dossier_cables.xlsx
- Excel file is build with one tab per type of cable, containing all retrieved information concerning that particular cable
- As an additional input we have also an example of 065 file, describing the kind of ouput we are expecting for all cables described in the excel sheet

As a list of action, we may have:
- Ingest dossier_cables.xlsx file to retrieve all usefull information
- build and store a database where all usefull information coming from excel file are stored in a reusable manner
- create the template of 065 file where all information are gathered from database
- perform as many 065 creation as we have tabs in the input excel file
