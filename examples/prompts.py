st1_to_st3_prompt='''

Step 1: Locate and extract only the numbered items directly under the section titled "SECTION INCLUDES" in the document. The extraction should be limited strictly to the content within the "SECTION INCLUDES" part. Do not include any additional information from other sections such as regulatory requirements, performance/design criteria, installation, protection, cleaning, or warranty.
Step 2: Identify the aliases used to refer to the key products outlined within the "SECTION INCLUDES" portion of the document.
	a) Example aliases include “GYPBD-1, RF-1”. Return only a numbered list of products that have an alias.
Step 3: Using the list of products and aliases you created in step 2, verify  no product or alias is excluded from our list. If you identify a new product and alias, add this new product to the existing list. 



'''


stp4_prompt='''

 Task: Process and Extract Detailed Information on Construction Materials

The following is a list of construction materials:

#########  

{st1_st3}

#########
Your objective is to thoroughly review this list and complete the following steps for each material, following the order of the items:

Locate Relevant Sections:
For each construction material, identify the corresponding section in the provided text document that pertains specifically to that material. Ensure that you focus only on the section directly related to the product.

Extract Detailed Information:
From the identified section, extract all numbered and bulleted data related to the construction material, including any specifications, attributes, or key details.

Ensure Completeness:
Before moving on to the next item, verify that all relevant data for the current construction material has been extracted. Be sure that the information captured is comprehensive and includes any necessary specifications or descriptions.

Final Output:
Your final output should be a well-organized list of construction materials, each accompanied by the extracted data. Ensure that the output is structured clearly, allowing for easy reference to the materials and their associated information.

Requirements:

Prioritize accuracy and ensure that no important details are missed.
If there are any ambiguities or missing data in the text, clearly note them.
Present the final output in a clean, numbered format, ensuring that each construction material is paired with its detailed data.

'''



submittal_st1_to_st3_prompt='''

Step 1: Locate and extract only the numbered items directly under the section titled "SECTION INCLUDES" in the document. The extraction should be limited strictly to the content within the "SECTION INCLUDES" part. Do not include any additional information from other sections such as regulatory requirements, performance/design criteria, installation, protection, cleaning, or warranty.
Step 2: Identify the aliases used to refer to the key products outlined within the "SECTION INCLUDES" portion of the document.
	a) Example aliases include “GYPBD-1, RF-1”. Return only a numbered list of products that have an alias.
Step 3: Using the list of products and aliases you created in step 2, verify  no product or alias is excluded from our list. If you identify a new product and alias, add this new product to the existing list. 



'''



submittal_stp4_prompt='''

 Task: Process and Extract Detailed Information on Construction Materials

The following is a list of construction materials:

#########  

{submittal_st1_to_st3}

#########
Your objective is to thoroughly review this list and complete the following steps for each material, following the order of the items:

Locate Relevant Sections:
For each construction material, identify the corresponding section in the provided text document that pertains specifically to that material. Ensure that you focus only on the section directly related to the product.

Extract Detailed Information:
From the identified section, extract all numbered and bulleted data related to the construction material, including any specifications, attributes, or key details.

Ensure Completeness:
Before moving on to the next item, verify that all relevant data for the current construction material has been extracted. Be sure that the information captured is comprehensive and includes any necessary specifications or descriptions.

Final Output:
Your final output should be a well-organized list of construction materials, each accompanied by the extracted data. Ensure that the output is structured clearly, allowing for easy reference to the materials and their associated information.

Requirements:

Prioritize accuracy and ensure that no important details are missed.
If there are any ambiguities or missing data in the text, clearly note them.
Present the final output in a clean, numbered format, ensuring that each construction material is paired with its detailed data.

'''


comparison='''
Task: Strict Comparison of Construction Material Data Between Specification and Submittal Documents

**Specification Document**:
{specification_st4}

**Submittal Document**:
{submittal_st4}

Objective: Conduct a detailed, item-by-item comparison between the Specification and Submittal documents. For each construction material:
1. Mark "SUCCESS" if all details match exactly.
2. Mark "FAILURE" if there is any discrepancy, and provide a specific note detailing the missing, incorrect, or differing information.

### Step-by-Step Instructions:

**Step 1: Material Matching and Verification**
- For each material listed in the Specification Document, locate the corresponding entry in the Submittal Document based on material name or alias.
- **FAILURE**: If a material or alias is not found in the Submittal Document, mark as “FAILURE” and note it as missing.

**Step 2: Attribute Comparison**
For each matched material entry:
- **Exact Match Check**: Compare all attributes (e.g., descriptions, thickness, certifications, specific standards compliance) between the Specification and Submittal documents:
  - **SUCCESS**: If all details match exactly.
  - **FAILURE**: If any attributes differ or are missing, mark the entry as "FAILURE" with a brief explanation (e.g., missing specification, incorrect measurement).
  - **Note**: For implied or non-explicit specifications in the submittal, annotate as "Implied, not explicitly stated."

**Step 3: Structured Output**
- Each material should have its details from both Specification and Submittal Documents listed side-by-side for easy comparison.
- Annotate each material with **SUCCESS** or **FAILURE**.
- For each FAILURE, include a **Discrepancy Note** that specifies the exact difference or missing information.

### Example Output:

**1. GYP BD-1 Impact Resistant Board**
- **Specification Document Details**:
  - **Description**: [Specification data]
  - **Specifications**: [List specifications]
- **Submittal Document Details**:
  - **Description**: [Submittal data]
  - **Specifications**: [List specifications]
- **Annotation**: SUCCESS / FAILURE
- **Discrepancy Note**: [Specific missing/incorrect information for FAILURE]

### Final Output Requirements
- Ensure each material entry is marked as **SUCCESS** or **FAILURE**.
- Any missing, incorrect, or differing information must be noted in a **Discrepancy Note** for each FAILURE.
- Arrange the output in a structured, item-by-item format for easy reference.




'''

submittal_prompt='''



Task: Comprehensive Verification of Construction Material Data

The following is a numbered list of construction materials, each accompanied by its corresponding product data: {st4}.

Your objective is to meticulously review each item in the list and verify its accuracy based on the provided document. Follow these steps for each numbered item to ensure a thorough and complete verification:

Examine the Construction Material Data:
For each material in the list, carefully review the associated bulleted product data to ensure accuracy.

Cross-Check Against the Document:
Compare the product data against the corresponding section within the provided text document. For each piece of data:

Verify the exact match between the data in the list and the data in the text document.
Annotate the Results:
Based on your verification, annotate each item according to the following criteria:

If all product data matches exactly, return the original numbered item with its data and mark it as "SUCCESS".
If any product data is missing or incorrect, return the original numbered item with its data and mark it as "FAILURE". Additionally, provide a brief note explaining what is missing or incorrect.
Proceed Sequentially:
After completing the verification for one construction material, move on to the next item in the list. Ensure that the same level of scrutiny is applied consistently to all materials.

Final Output Requirements:

The output must include the full list of construction materials with their respective data and annotations ("SUCCESS" or "FAILURE").
For items marked as "FAILURE", clearly explain which elements of the data were incorrect or missing.
Ensure that the final output is well-organized and presented in a structured format for easy review and reference.



'''


submittal_prompt2='''

1) Provide the main theme of the document. Reduce the main theme to a construction material. Return only the name of the identified construction object and material"
 


'''


submittal_prompt3='''


Go step by step.
    Step 1: Identify all of the {sub_q}.
    Step 2: Go through every {sub_q} in your list and produce bullet points summarizing the {sub_q} materials of the information retrieved. 
    Don't skip any {sub_q}.
 
 
Expected output:
 
    A nicely formatted report of the different materials and product data for all {sub_q}.

has context menu



'''