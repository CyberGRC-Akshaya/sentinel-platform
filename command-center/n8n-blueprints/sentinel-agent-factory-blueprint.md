# Sentinel Agent Factory â€” n8n Build Blueprint

## Goal
Read tasks from Google Sheets, route tasks to the correct AI agent, create an output document, save it to Google Drive, and update the PMO log.

## Google Sheet
Name: Sentinel PMO

Tabs:
1. Agent_Input_Queue
2. Agent_Output_Log
3. Product_Backlog
4. Decision_Log
5. Risk_Log

## Google Drive
Folder:
Sentinel Command Center

Subfolders:
01_PMO
02_Agent_Outputs
03_Product_Requirements
04_Framework_Intelligence
05_Demo_Evidence
06_Client_Reports
07_Sales_Assets
08_GitHub_Assets
09_n8n_Workflows

## n8n workflow
Name: Sentinel Agent Factory v0.3

Nodes:
1. Manual Trigger
2. Google Sheets - Read rows from Agent_Input_Queue
3. Filter - Status equals New
4. Split In Batches - one task at a time
5. Switch - Agent_Name contains Agent 00/01/02/03/04/05/06
6. OpenAI Chat node for the selected agent
7. Google Docs - Create document
8. Google Drive - Move document to 02_Agent_Outputs
9. Google Sheets - Append Agent_Output_Log
10. Google Sheets - Update Agent_Input_Queue row Status to Completed

## Minimum viable automation
For the first run, do not overcomplicate routing.
Use one OpenAI node with a master router prompt that reads Agent_Name and applies the correct persona.

## Recommended model settings
Temperature: 0.2 to 0.4
Max output: high enough for detailed docs
System message: Sentinel Master Agent Router
User message: combine row fields from Google Sheet

## Output document title
{{$json["Task_ID"]}} - {{$json["Agent_Name"]}} - Sentinel Output

## Output log summary
Use first 2-3 lines of model output, or ask the model to provide a "PMO Summary" field.
