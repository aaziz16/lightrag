specs_product_extraction='''

Step 1: Locate and extract only the numbered items directly under the section titled "SECTION INCLUDES" in the document. The extraction should be limited strictly to the content within the "SECTION INCLUDES" part. Do not include any additional information from other sections such as regulatory requirements, performance/design criteria, installation, protection, cleaning, or warranty.
Step 2: Identify the aliases used to refer to the key products outlined within the "SECTION INCLUDES" portion of the document.
	a) Example aliases include “GYPBD-1, RF-1”. Return only a numbered list of products that have an alias.
Step 3: Using the list of products and aliases you created in step 2, verify  no product or alias is excluded from our list. If you identify a new product and alias, add this new product to the existing list. 



'''


specs_product_details='''


Task: Process and Extract Detailed Information on Construction Materials

The following is a list of construction materials:

{st1_st3}

Objective:
Review and extract all relevant information for each construction material listed above, presenting the results in a clean, structured format.

Instructions:
Locate Relevant Sections:

For each material, locate the section that contains detailed information specific to that product only.
Extract Detailed Information:

Capture all specifications, features, and attributes listed under each product.
Include any bulleted or numbered details, compliance standards, and environmental certifications.
Format the Final Output:

Structure the output for easy reference by using headings and subheadings for each material.
Avoid including these instructions or task descriptions in your output.

 
'''



submittal_product_extraction='''
You are an AI assistant that helps analyze submittal documents for detailed product information. Follow these steps carefully:

Step 1: Identify the Main Construction Material
Review the provided text document thoroughly.
Look for references to specific construction materials or product categories. Identify each material or category if multiple are present.
Note that each distinct variation within a product category (e.g., different thicknesses or profiles) should be treated as an individual product listing.
Step 2: List Each Product Listing Separately
Once the main construction material(s) is identified, locate individual product listings.
Treat each distinct variation (e.g., variations in thickness, profiles, or applications) within a product category as a separate product entry. Do not merge variations.
Extract relevant details for each product in the following structured format:
Product Listings:

Main Construction Material: [Identified Material, e.g., Thermoplastic Rubber, Vinyl]
Product Name: [e.g., BurkeBase Type TP]
Features:
Material Type: [e.g., Thermoplastic Rubber]
Profile/Design Elements: [e.g., coved or toeless, available finishes]
Specifications:
Thickness: [e.g., 1/8" (3.2 mm)]
Height Options: [e.g., 2.5", 4", 4.5", 6"]
Compliance: [e.g., ASTM F1861 Type TP, Group 1]
Additional Performance Standards: [e.g., Static Load, Radiant Panel]
Environmental & Compliance Certifications:
Certifications: [e.g., FloorScore, LEED]
Additional Compliance Details: [e.g., Buy American Act]
Additional Details: [e.g., manufacturing location, warranty]
Important:
Repeat this structured listing for each product variation under the same material category.
Do not combine different product variations (e.g., different thicknesses or profiles of the same product line) into one entry; list each with its specific features and specifications.
Here’s an example:

Main Construction Material: Thermoplastic Rubber

Product Listings:

Product Name: BurkeBase Type TP 1/8"
Features: [include features specific to this product]
Specifications: [include specifications specific to this product]
Environmental Data: [include relevant certifications]
Repeat this approach for all product variations.


Requirements:

Prioritize accuracy and ensure that no important details are missed and DO NOT MAKE UP ANY PRODUCT THAT IS NOT LISTED.
DOUBLE CHECK THE RESULT TO ENSURE ACCUACY

'''



submittal_products_detail='''

 Task: Process and Extract Detailed Information on Construction Materials

The following is a list of construction materials:

{submittal_st1_to_st3}

Objective:
Review and extract all relevant information for each construction material listed above, presenting the results in a clean, structured format.

Instructions:
Locate Relevant Sections:

For each material, locate the section that contains detailed information specific to that product only.
Extract Detailed Information:

Capture all specifications, features, and attributes listed under each product.
Include any bulleted or numbered details, compliance standards, and environmental certifications.
Format the Final Output:

Structure the output for easy reference by using headings and subheadings for each material.
Avoid including these instructions or task descriptions in your output.
'''


comparison='''

**Task**: Attribute-by-Attribute Comparison of Construction Material Data Between Specification and Submittal Documents

### Specification Document:
{specification_st4}

### Submittal Document:
{submittal_st4}

**Objective**: Compare products listed in the Specification and Submittal documents in a detailed, attribute-by-attribute table format. Use the following rules:
1. If an attribute matches exactly, mark as **MATCH**.
2. If an attribute differs, mark as **FAILURE** and include a note describing the discrepancy.
3. If an attribute is not mentioned in the Specification Document but is listed in the Submittal Document, mark as **N/A**.

---

### Instructions:

#### **Step 1: Product Matching**
- Identify corresponding products in both documents by name or alias.
  - If a product exists in the Specification Document but is missing in the Submittal Document, mark as **FAILURE** with a note: "Product not found."
  - If a product exists only in the Submittal Document but not in the Specification Document, list it and mark all Specification attributes as **N/A**.

#### **Step 2: Attribute Comparison**
- Compare attributes such as **Material Type**, **Thickness**, **Finish**, **Standards Compliance**, and others.
- For each attribute, provide a status:  
  - **MATCH**: Attributes are identical.
  - **FAILURE**: Attributes differ, with a detailed note.
  - **N/A**: Attribute is not mentioned in the Specification Document.

---

### Example Output:

#### **Comparison Table for Each Product**

| **Product Name**                  | **Attribute**          | **Specification Document**                 | **Submittal Document**                       | **Result**     | **Discrepancy Note**                           |
|-----------------------------------|------------------------|--------------------------------------------|----------------------------------------------|----------------|-----------------------------------------------|
| **GYP BD-2 – Gypsum Board**       | Material Type          | Paper-faced gypsum panels                  | ToughRock® Fireguard X™ Gypsum Board         | MATCH          |                                               |
|                                   | Thickness              | 1/2 inch (12.7 mm)                         | 1/2 inch (12.7 mm)                           | MATCH          |                                               |
|                                   | Finish                 | Smooth                                     | Smooth                                       | MATCH          |                                               |
|                                   | Standards Compliance   | ASTM C1396/C1396M                          | ASTM C1396                                   | MATCH          |                                               |
|                                   | Additional Attribute   | N/A                                        | Noncombustible core, reinforced with glass fibers | N/A          | Not specified in Specification Document.      |
| **GYP BD-3 – Moisture Resistant** | Material Type          | Moisture-resistant gypsum panels           | Not found                                   | FAILURE        | Product not found in Submittal Document.      |
|                                   | Thickness              | 1/2 inch (12.7 mm)                         | Not found                                   | FAILURE        | Product not found in Submittal Document.      |
|                                   | Finish                 | Water-resistant coating                    | Not found                                   | FAILURE        | Product not found in Submittal Document.      |

---

### **Output Requirements**
1. **Clear Table Structure**: 
   - Each product comparison is in its own table for clarity.
   - Use rows for each attribute to compare values between Specification and Submittal documents.
2. **Attribute-by-Attribute Comparison**:
   - For each attribute, compare and mark as **MATCH**, **FAILURE**, or **N/A**.
3. **Discrepancy Notes**: For any **FAILURE**, provide a detailed note explaining the difference.
4. **Complete Output**:
   - Include all attributes in the Submittal Document, even if not mentioned in the Specification Document (marking as **N/A** where necessary).

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