# PBP Data Extractor

PBP (Plan Benefit Package) contains the list of benefits (Medicare / Non Medicare).  This project is to build ETL process on PBP files.  The process has following steps.

- Data Analysis
- Implementation
- Validation

Check the Notebooks for more details.

## AWS Glue
This project is building ETL process like AWS Glue. https://aws.amazon.com/glue/

## PySpark
The project depends on PySpark (https://spark.apache.org/docs/latest/api/python/index.html).  PySpark allows:
- Instead of loading data file to database table and write complex query, each data file is read as table
- Write complex query language to join and filter from multiple data sources (SQL query result and data files)
- Save the result data files
- Upload the data to sql directly
- Write Code instead of writing large sql query

## PBP Flat File
PBP Flat file is downloaded from medicare.gov site(https://www.cms.gov/data-research/statistics-trends-and-reports/medicare-advantagepart-d-contract-and-enrollment-data/benefits-data).  

## Notebooks
### PBP_Benefit_Decision_Tree.ipynb
The notebook finds data pattern and find the most weighted data columns that generate the classified benefit costs.  Before implementing the benefit, we need to know whether the new benefit has existing benefit pattern or new benefit structure to write the code.

### PBP_plan_data_extractor_build_individual_benefit_tool.ipynb
After the analysis on new benefit is completed, we use the notebook to build the benefit cost text for the new benefit.  The notebook continuely verifies the benefit cost logic against the crawled data from medicare.gov.

### PBP_plan_data_extractor.ipynb 
The notebook collects all benefit costs implementation.  Any new benefit costs implementation in PBP_plan_data_extractor_build_individual_benefit_tool should be added Target Data in readme and this notebook.   

Many benefit are sharing the cost calculation logic. Any logic changes in the existing benefit cost logic should be run to this note to validate the change that share the logic. EX) Vision Benefits( 17b1, 17b2, 17b3, 17b4) and Hearing benefits (18a1, 18a2, 18b1) share Out of network Benefit logic using Non-Medicare benefit instead of Medicare benefits.  However, their In-network benefits logic are different.  If OON logic are changed on 18a1, that changes OON logic for the six other benefits. We need to make sure that the new change in 18a1 OON create the issues in the other benefits. 

###  PBP_plan_benefit_data_validator.ipynb
The notebook compare all benefits from PBP_plan_data_extractor against the medicare.gov. 

## Target Data
### Basic Plan Info
    - Plan Name
    - Plan Type
    - SNP Type
    - Drug Deductible Limit
    - WebSite
    - Health Deductible Limit
    - MAXIMUM YOU PAY FOR HEALTH SERVICES
### Benefits
|Category|Service|Benefit Code|
| :------------ |:---------------:| -----:|
|DOCTOR SERVICES|Primary doctor visit|7a|
|DOCTOR SERVICES|Specialist visit|7d|
|TESTS, LABS, & IMAGING|Diagnostic tests & procedures|8a1|
|TESTS, LABS, & IMAGING|Lab services|8a2|
|TESTS, LABS, & IMAGING|Diagnostic radiology services (like MRI)|8b1|
|TESTS, LABS, & IMAGING|Outpatient x-rays|8b3|
|TESTS, LABS, & IMAGING|Emergency care|4a|
|TESTS, LABS, & IMAGING|Urgent care|4b|
|HOSPITAL SERVICES|Inpatient hospital coverage|1a|
|HOSPITAL SERVICES|Outpatient hospital coverage|9a1|
|SKILLED NURSING FACILITY|Skilled nursing facility|2|
|PREVENTIVE SERVICES|Preventive services|14a|
|AMBULANCE|Ground ambulance|10a1|
|THERAPY SERVICES|Occupational therapy visit|7c|
|THERAPY SERVICES|Physical therapy & speech & language therapy visit|7i|
|MENTAL HEALTH SERVICES|Outpatient group therapy visit|7e2|
|MENTAL HEALTH SERVICES|Outpatient group therapy with a psychiatrist|7h2|
|MENTAL HEALTH SERVICES|Outpatient individual therapy visit|7e1|
|MENTAL HEALTH SERVICES|Outpatient individual therapy with a psychiatrist|7h1|
|PREVENTIVE DENTAL|Oral exam|16a1|
|PREVENTIVE DENTAL|Cleaning|16a2|
|PREVENTIVE DENTAL|Fluoride treatment|16a3|
|PREVENTIVE DENTAL|Dental x-rays|16a4|
|HEARING|Hearing exam|18a1|
|HEARING|Fitting/evaluation|18a2|
|HEARING|Hearing aids - all types|18b1|
|VISION|Contact lenses|17b1|
|VISION|Eyeglasses (frames & lenses)|17b2|
|VISION|Eyeglass lenses only|17b3|
|VISION|Eyeglass frames only|17b4|
|VISION|Upgrades|17b5|
|VISION|Routine eye exam|17a1|
|PART B DRUGS|Chemotherapy drugs|15-2|
|PART B DRUGS|Other Part B drugs|15-3|
|PART B DRUGS|Part B insulin|15-1-I|
|OTHER SERVICES|Durable medical equipment (like wheelchairs & oxygen)|11a|
|OTHER SERVICES|Prosthetics (like braces, artificial limbs)|11b1|
|OTHER SERVICES|Diabetes supplies|11c1|

### Findings
- 18a1, 18a2, 18b1 (under Hearing) and 17b1, 17b2, 17b3, 17b4, 17b5 (under Vision) and uses Out-of-Network for Non-Medicare OON & POS if Non-Medicare OON & POS.  If NMC OON & POS are not available, use MC OON & POS.
- Emergency care and Urgent care under 'TESTS, LABS, & IMAGING' (4a, 4b) has no in-network only service.  
- All HMO plans append 'in-network' for all benefits (under 'Hearing')  and Dialysis (under 'Other Services') benefits as long as the benefit is covered. (need to confirm)

### to-do



