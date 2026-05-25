# Sentinel Agent Factory — n8n Blueprint

Workflow objective:
Read agent tasks from Google Sheets, route each task to the correct AI Agent prompt, generate output, create a Google Doc, save it in Google Drive, and update the PMO log.

Nodes:
1. Manual Trigger
2. Google Sheets - Read Agent_Input_Queue
3. IF node - Status equals New
4. Switch node - Agent_Name
5. OpenAI Chat / AI Agent node
6. Google Docs - Create Document
7. Google Drive - Move/Store Document
8. Google Sheets - Append Agent_Output_Log
9. Google Sheets - Update Task Status to Completed

Google Sheet tabs required:
- Agent_Input_Queue
- Agent_Output_Log
- Product_Backlog
- Sprint_Board
- Framework_Mapping
- Launch_Assets

Folder structure in Google Drive:
- Sentinel Command Center
  - 01_PMO
  - 02_Agent_Outputs
  - 03_Product_Requirements
  - 04_Framework_Intelligence
  - 05_Demo_Evidence
  - 06_Client_Reports
  - 07_Sales_Assets
  - 08_GitHub_Assets

First automation goal:
Run T001 through T007 and generate one Google Doc per agent output.
