# '''

# # Developed by Abdul Aziz
# # This Streamlit app is designed for document comparison using Light00 RAG for specification and submittal documnets
# # Date: 10/25/2024




# '''

import streamlit as st
import tempfile
import asyncio
import os
from pdf_extract import extract_text_from_image_pdf  # Your custom extraction function
from lightrag_azure_openai_demo import *  # Import necessary functions
from fpdf import FPDF  # Importing from fpdf2
# from lightrag.lightrag import LightRAG, QueryParam
# from lightrag.lightrag.utils import EmbeddingFunc
# Define working directories
WORKING_DIR_SPECS = "input"
WORKING_DIR_SUBMITTAL = "sub_input"

# Function to dynamically set up model configurations for each step
def get_model_config(step):
    model_configs = {
        'specs_model': {
            'api_version': "2024-02-15-preview",
            'deployment': "gpt-4o",
            'api_key': "9101287fb67e484b9970dd8d7e31aa05",
            'endpoint': "https://diesl-eus-openai-dev.openai.azure.com/",
            'embedding_deployment': "text-embedding-ada-002",
            'embedding_api_version': "2024-02-15-preview"
        },
        'submittal_model': {
            'api_version': "2024-02-15-preview",
            'deployment': "gpt-4o",
            'api_key': "9101287fb67e484b9970dd8d7e31aa05",
            'endpoint': "https://diesl-eus-openai-dev.openai.azure.com/",
            'embedding_deployment': "text-embedding-ada-002",
            'embedding_api_version': "2024-02-15-preview"
        },


         'submittal': {
            'api_version': "2024-02-15-preview",
            'deployment': "gpt-4o",
            'api_key': "9101287fb67e484b9970dd8d7e31aa05",
            'endpoint': "https://diesl-eus-openai-dev.openai.azure.com/",
            'embedding_deployment': "text-embedding-ada-002",
            'embedding_api_version': "2024-02-15-preview"

        },
    }
    return model_configs[step]

# Async function for specification processing
async def process_specification(specs_document_path, spec_status_placeholder, tab1):
    embedding_dimension = 1536
    model_config_step1_3 = get_model_config('specs_model')
    model_config_step4 = get_model_config('specs_model')
    # comparison_model= get_model_config('step4')
    
    # Initialize RAG for specification
    spec_status_placeholder.write("**Setting up specification processing environment...**")
    setup_working_directory(WORKING_DIR_SPECS)
    rag_specs = initialize_rag(WORKING_DIR_SPECS, embedding_dimension, llm_model_func, embedding_func, model_config_step1_3, chunk_token_size=750)
    
    # Extract text and process the Specification Document
    spec_status_placeholder.write("**Extracting text from Specification Document...**")
    specs_output_txt_path = f"text_input/{os.path.basename(specs_document_path)}.txt"
    extract_text_from_image_pdf(specs_document_path, specs_output_txt_path)
    spec_status_placeholder.write("**Text extraction from Specification Document complete.**")

    # Load Specification Document text and execute query
    spec_status_placeholder.write("**Inserting text into RAG for Step 1-3 query on Specification Document...**")
    with open(specs_output_txt_path) as f:
        await rag_specs.ainsert(f.read())
    specs_product_extraction_result = await execute_query(rag_specs, specs_product_extraction)
    spec_status_placeholder.write("**Step 1-3 query on Specification Document complete.**")

    # Display Step 1-3 Results
    with tab1:
        st.write("### Step 1-3 Results for Specification Document")
        st.write(specs_product_extraction_result)

    # Step 4 for Specification
    spec_status_placeholder.write("**Executing Step 4 query on Specification Document...**")
    rag_step4 = initialize_rag(WORKING_DIR_SPECS, embedding_dimension, llm_model_func, embedding_func, model_config_step4,chunk_token_size=750)
    formatted_step4_prompt = specs_product_details.format(st1_st3=specs_product_extraction_result)
    specs_product_details_result = await execute_query(rag_step4, formatted_step4_prompt)
    spec_status_placeholder.write("**Step 4 query on Specification Document complete.**")

    # Display Step 4 Results
    with tab1:
        st.write("### Step 4 Results for Specification Document")
        st.write(specs_product_details_result)

    return specs_product_extraction_result, specs_product_details_result

# Async function for submittal processing
async def process_submittal(submittal_document_path, submittal_status_placeholder, tab2):
    embedding_dimension = 1536
    # model_config_step1_3 = get_model_config('step1_3')
    model_config_submittal = get_model_config('submittal_model')
    
    # Initialize RAG for Submittal
    submittal_status_placeholder.write("**Setting up submittal processing environment...**")
    setup_working_directory(WORKING_DIR_SUBMITTAL)
    rag_submittal = initialize_rag(WORKING_DIR_SUBMITTAL, embedding_dimension, llm_model_func, embedding_func, model_config_submittal, chunk_token_size=750)
    # rag_submittal2 = initialize_rag(WORKING_DIR_SUBMITTAL, embedding_dimension, llm_model_func, embedding_func, model_config_step1_3, chunk_token_size=1300)

    # Extract text and process the Submittal Document
    submittal_status_placeholder.write("**Extracting text from Submittal Document...**")
    submittal_output_txt_path = f"text_input/{os.path.basename(submittal_document_path)}.txt"
    extract_text_from_image_pdf(submittal_document_path, submittal_output_txt_path)
    submittal_status_placeholder.write("**Text extraction from Submittal Document complete.**")

    # Load Submittal Document text and execute query
    submittal_status_placeholder.write("**Inserting text into RAG for Step 1-3 query on Submittal Document...**")
    with open(submittal_output_txt_path) as f:
        await rag_submittal.ainsert(f.read())
    submittal_product_extraction_result = await execute_query(rag_submittal, submittal_product_extraction)
    submittal_status_placeholder.write("**Step 1-3 query on Submittal Document complete.**")

    # Display Step 1-3 Results
    with tab2:
        st.write("### Step 1-3 Results for Submittal Document")
        st.write(submittal_product_extraction_result)

    # Step 4 for Submittal
    submittal_status_placeholder.write("**Executing Step 4 query on Submittal Document...**")
    formatted_submittal_prompts4 = submittal_products_detail.format(submittal_st1_to_st3=submittal_product_extraction_result)
    submittal_products_detail_result = await execute_query(rag_submittal, formatted_submittal_prompts4)
    submittal_status_placeholder.write("**Step 4 query on Submittal Document complete.**")

    # Display Step 4 Results
    with tab2:
        st.write("### Step 4 Results for Submittal Document")
        st.write(submittal_products_detail_result)

    return submittal_product_extraction_result, submittal_products_detail_result

# Main pipeline to handle parallel execution
async def main_pipeline(specs_document_path, submittal_document_path, spec_status_placeholder, submittal_status_placeholder, tab1, tab2, tab3):
    # Run specification and submittal processing in parallel
    spec_results, submittal_results = await asyncio.gather(
        process_specification(specs_document_path, spec_status_placeholder, tab1),
        process_submittal(submittal_document_path, submittal_status_placeholder, tab2)
    )
    
    # Unpack results
    specs_product_extraction_result, specs_product_details_result = spec_results
    submittal_product_extraction_result, submittal_products_detail_result = submittal_results

    # Final Comparison Report
    status_placeholder = st.empty()
    status_placeholder.write("**Generating Final Comparison Report...**")
    formatted_comparison = comparison.format(specification_st4=specs_product_details_result, submittal_st4=submittal_products_detail_result)
    llm_result = await llm_model_func(formatted_comparison, get_model_config('specs_model'))
    status_placeholder.write("**Final Comparison Report generated.**")
    
    # Display Final Comparison Report
    with tab3:
        st.write("### Final Comparison Report")
        st.write(llm_result)

    return specs_product_extraction_result, specs_product_details_result, submittal_product_extraction_result, submittal_products_detail_result, llm_result

# Streamlit Interface
st.title("DIESL AI INTL")

# File Uploads
specs_document = st.file_uploader("Upload Specification Document", type=["pdf"])
submittal_document = st.file_uploader("Upload Submittal Document", type=["pdf"])

# Process Button
if st.button("Run Comparison") and specs_document and submittal_document:
    # Save files temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as specs_temp, tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as submittal_temp:
        specs_temp.write(specs_document.read())
        submittal_temp.write(submittal_document.read())
        specs_path = specs_temp.name
        submittal_path = submittal_temp.name

    # Tabs for displaying results
    tab1, tab2, tab3 = st.tabs(["Specification", "Submittal", "Final Report"])
    
    # Placeholders for status updates
    spec_status_placeholder = tab1.empty()
    submittal_status_placeholder = tab2.empty()
    
    # Run async processing and collect results
    with st.spinner("Processing..."):
        specs_product_extraction_result, specs_product_details_result, submittal_product_extraction_result, submittal_products_detail_result, llm_result = asyncio.run(
            main_pipeline(specs_path, submittal_path, spec_status_placeholder, submittal_status_placeholder, tab1, tab2, tab3)
        )

    # Save Final Report to PDF with UTF-8 support
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, llm_result.encode('utf-8', 'ignore').decode('latin-1'))
    
    pdf_output = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf_file_path = pdf_output.name
    pdf.output(pdf_file_path, dest='F')

    # Final Report Tab with PDF Download
    with open(pdf_file_path, "rb") as pdf_file:
        st.download_button("Download Final Report as PDF", data=pdf_file, file_name="Final_Comparison_Report.pdf", mime="application/pdf")




# import streamlit as st
# import tempfile
# import asyncio
# import os
# from pdf_extract import extract_text_from_image_pdf  # Your custom extraction function
# from lightrag_azure_openai_demo import *  # Import necessary functions
# from fpdf import FPDF  # Importing from fpdf2
# from feedback import save_feedback_to_postgres  # Importing the feedback service

# # Define working directories
# WORKING_DIR_SPECS = "input"
# WORKING_DIR_SUBMITTAL = "sub_input"

# # Function to dynamically set up model configurations for each step
# def get_model_config(step):
#     model_configs = {
#         'specs_model': {
#             'api_version': "2024-02-15-preview",
#             'deployment': "gpt-4o",
#             'api_key': "9101287fb67e484b9970dd8d7e31aa05",
#             'endpoint': "https://diesl-eus-openai-dev.openai.azure.com/",
#             'embedding_deployment': "text-embedding-ada-002",
#             'embedding_api_version': "2024-02-15-preview"
#         },
#         'submittal_model': {
#             'api_version': "2024-02-15-preview",
#             'deployment': "gpt-4o",
#             'api_key': "9101287fb67e484b9970dd8d7e31aa05",
#             'endpoint': "https://diesl-eus-openai-dev.openai.azure.com/",
#             'embedding_deployment': "text-embedding-ada-002",
#             'embedding_api_version': "2024-02-15-preview"
#         },
#         'submittal': {
#             'api_version': "2024-02-15-preview",
#             'deployment': "gpt-4o",
#             'api_key': "9101287fb67e484b9970dd8d7e31aa05",
#             'endpoint': "https://diesl-eus-openai-dev.openai.azure.com/",
#             'embedding_deployment': "text-embedding-ada-002",
#             'embedding_api_version': "2024-02-15-preview"
#         },
#     }
#     return model_configs[step]


# # Initialize session state
# if "st1_to_st3_results" not in st.session_state:
#     st.session_state.st1_to_st3_results = None
# if "step4_results" not in st.session_state:
#     st.session_state.step4_results = None
# if "submittal_st1_to_st3" not in st.session_state:
#     st.session_state.submittal_st1_to_st3 = None
# if "submittal_st4" not in st.session_state:
#     st.session_state.submittal_st4 = None
# if "llm_result" not in st.session_state:
#     st.session_state.llm_result = None

# # Async function for specification processing
# async def process_specification(specs_document_path, spec_status_placeholder, tab1):
#     embedding_dimension = 1536
#     model_config_step1_3 = get_model_config('specs_model')
#     model_config_step4 = get_model_config('specs_model')

#     # Initialize RAG for specification
#     spec_status_placeholder.write("**Setting up specification processing environment...**")
#     setup_working_directory(WORKING_DIR_SPECS)
#     rag_specs = initialize_rag(WORKING_DIR_SPECS, embedding_dimension, llm_model_func, embedding_func, model_config_step1_3, chunk_token_size=1200)
    
#     # Extract text and process the Specification Document
#     spec_status_placeholder.write("**Extracting text from Specification Document...**")
#     specs_output_txt_path = f"text_input/{os.path.basename(specs_document_path)}.txt"
#     extract_text_from_image_pdf(specs_document_path, specs_output_txt_path)
#     spec_status_placeholder.write("**Text extraction from Specification Document complete.**")

#     # Load Specification Document text and execute query
#     spec_status_placeholder.write("**Inserting text into RAG for Step 1-3 query on Specification Document...**")
#     with open(specs_output_txt_path) as f:
#         await rag_specs.ainsert(f.read())
#     st1_to_st3_results = await execute_query(rag_specs, st1_to_st3_prompt)
#     spec_status_placeholder.write("**Step 1-3 query on Specification Document complete.**")

#     # Display Step 1-3 Results with Markdown formatting
#     with tab1:
#         st.markdown("### Step 1-3 Results for Specification Document")
#         st.markdown(f"**Results:**\n\n{st1_to_st3_results}", unsafe_allow_html=True)

#     # Step 4 for Specification
#     spec_status_placeholder.write("**Executing Step 4 query on Specification Document...**")
#     rag_step4 = initialize_rag(WORKING_DIR_SPECS, embedding_dimension, llm_model_func, embedding_func, model_config_step4)
#     formatted_step4_prompt = stp4_prompt.format(st1_st3=st1_to_st3_results)
#     step4_results = await execute_query(rag_step4, formatted_step4_prompt)
#     spec_status_placeholder.write("**Step 4 query on Specification Document complete.**")

#     # Display Step 4 Results with Markdown formatting
#     with tab1:
#         st.markdown("### Step 4 Results for Specification Document")
#         st.markdown(f"**Results:**\n\n{step4_results}", unsafe_allow_html=True)

#     return st1_to_st3_results, step4_results

# # Async function for submittal processing
# async def process_submittal(submittal_document_path, submittal_status_placeholder, tab2):
#     embedding_dimension = 1536
#     model_config_submittal = get_model_config('submittal_model')

#     # Initialize RAG for Submittal
#     submittal_status_placeholder.write("**Setting up submittal processing environment...**")
#     setup_working_directory(WORKING_DIR_SUBMITTAL)
#     rag_submittal = initialize_rag(WORKING_DIR_SUBMITTAL, embedding_dimension, llm_model_func, embedding_func, model_config_submittal, chunk_token_size=1300)

#     # Extract text and process the Submittal Document
#     submittal_status_placeholder.write("**Extracting text from Submittal Document...**")
#     submittal_output_txt_path = f"text_input/{os.path.basename(submittal_document_path)}.txt"
#     extract_text_from_image_pdf(submittal_document_path, submittal_output_txt_path)
#     submittal_status_placeholder.write("**Text extraction from Submittal Document complete.**")

#     # Load Submittal Document text and execute query
#     submittal_status_placeholder.write("**Inserting text into RAG for Step 1-3 query on Submittal Document...**")
#     with open(submittal_output_txt_path) as f:
#         await rag_submittal.ainsert(f.read())
#     submittal_st1_to_st3 = await execute_query(rag_submittal, submittal_st1_to_st3_prompt)
#     submittal_status_placeholder.write("**Step 1-3 query on Submittal Document complete.**")

#     # Display Step 1-3 Results with Markdown formatting
#     with tab2:
#         st.markdown("### Step 1-3 Results for Submittal Document")
#         st.markdown(f"**Results:**\n\n{submittal_st1_to_st3}", unsafe_allow_html=True)

#     # Step 4 for Submittal
#     submittal_status_placeholder.write("**Executing Step 4 query on Submittal Document...**")
#     formatted_submittal_prompts4 = submittal_stp4_prompt.format(submittal_st1_to_st3=submittal_st1_to_st3)
#     submittal_st4 = await execute_query(rag_submittal, formatted_submittal_prompts4)
#     submittal_status_placeholder.write("**Step 4 query on Submittal Document complete.**")

#     # Display Step 4 Results with Markdown formatting
#     with tab2:
#         st.markdown("### Step 4 Results for Submittal Document")
#         st.markdown(f"**Results:**\n\n{submittal_st4}", unsafe_allow_html=True)

#     return submittal_st1_to_st3, submittal_st4

# # Main pipeline to handle parallel execution
# async def main_pipeline(specs_document_path, submittal_document_path, spec_status_placeholder, submittal_status_placeholder, tab1, tab2, tab3):
#     # Run specification and submittal processing in parallel
#     spec_results, submittal_results = await asyncio.gather(
#         process_specification(specs_document_path, spec_status_placeholder, tab1),
#         process_submittal(submittal_document_path, submittal_status_placeholder, tab2)
#     )

#     # Unpack results
#     st1_to_st3_results, step4_results = spec_results
#     submittal_st1_to_st3, submittal_st4 = submittal_results

#     # Final Comparison Report
#     status_placeholder = st.empty()
#     status_placeholder.write("**Generating Final Comparison Report...**")
#     formatted_comparison = comparison.format(specification_st4=step4_results, submittal_st4=submittal_st4)
#     llm_result = await llm_model_func(formatted_comparison, get_model_config('specs_model'))
#     status_placeholder.write("**Final Comparison Report generated.**")

#     # Display Final Comparison Report with Markdown formatting
#     with tab3:
#         st.markdown("### Final Comparison Report")
#         st.markdown(f"**Results:**\n\n{llm_result}", unsafe_allow_html=True)

#     return st1_to_st3_results, step4_results, submittal_st1_to_st3, submittal_st4, llm_result


# # Streamlit Interface
# st.title("DIESL AI INTL")

# # File Uploads
# specs_document = st.file_uploader("Upload Specification Document", type=["pdf"])
# submittal_document = st.file_uploader("Upload Submittal Document", type=["pdf"])

# # Tabs for displaying results
# tab1, tab2, tab3 = st.tabs(["Specification", "Submittal", "Final Report"])

# # Process Button
# if st.button("Run Comparison") and specs_document and submittal_document:
#     # Save files temporarily
#     with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as specs_temp, tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as submittal_temp:
#         specs_temp.write(specs_document.read())
#         submittal_temp.write(submittal_document.read())
#         specs_path = specs_temp.name
#         submittal_path = submittal_temp.name

#     # Placeholders for status updates
#     spec_status_placeholder = tab1.empty()
#     submittal_status_placeholder = tab2.empty()

#     # Run async processing and collect results
#     with st.spinner("Processing..."):
#         st.session_state.st1_to_st3_results, st.session_state.step4_results, st.session_state.submittal_st1_to_st3, st.session_state.submittal_st4, st.session_state.llm_result = asyncio.run(
#             main_pipeline(specs_path, submittal_path, spec_status_placeholder, submittal_status_placeholder, tab1, tab2, tab3)
#         )

#     # Save Final Report to PDF with UTF-8 support
#     pdf = FPDF()
#     pdf.add_page()
#     pdf.set_auto_page_break(auto=True, margin=15)
#     pdf.set_font("Arial", size=12)
#     pdf.multi_cell(0, 10, st.session_state.llm_result.encode('utf-8', 'ignore').decode('latin-1'))

#     pdf_output = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
#     pdf_file_path = pdf_output.name
#     pdf.output(pdf_file_path, dest='F')

#     # Add the download button in the Final Report tab
#     with tab3:
#         with open(pdf_file_path, "rb") as pdf_file:
#             st.download_button("Download Final Report as PDF", data=pdf_file, file_name="Final_Comparison_Report.pdf", mime="application/pdf")

# # Display results in their respective sections
# with tab1:
#     if st.session_state.st1_to_st3_results or st.session_state.step4_results:
#         st.markdown("### Specification Results")
#         if st.session_state.st1_to_st3_results:
#             st.markdown(f"**Step 1-3 Results:**\n\n{st.session_state.st1_to_st3_results}", unsafe_allow_html=True)
#         if st.session_state.step4_results:
#             st.markdown(f"**Step 4 Results:**\n\n{st.session_state.step4_results}", unsafe_allow_html=True)

# with tab2:
#     if st.session_state.submittal_st1_to_st3 or st.session_state.submittal_st4:
#         st.markdown("### Submittal Results")
#         if st.session_state.submittal_st1_to_st3:
#             st.markdown(f"**Step 1-3 Results:**\n\n{st.session_state.submittal_st1_to_st3}", unsafe_allow_html=True)
#         if st.session_state.submittal_st4:
#             st.markdown(f"**Step 4 Results:**\n\n{st.session_state.submittal_st4}", unsafe_allow_html=True)

# with tab3:
#     if st.session_state.llm_result:
#         st.markdown("### Final Report")
#         st.markdown(f"{st.session_state.llm_result}", unsafe_allow_html=True)

# # User Feedback
# st.write("### Your Feedback")
# feedback = st.radio("Was the report helpful?", ("Thumbs Up", "Thumbs Down"))
# comments = ""
# if feedback == "Thumbs Down":
#     comments = st.text_area("Please share your feedback or suggestions for improvement")

# if st.button("Submit Feedback"):
#     # Save feedback and report data to PostgreSQL
#     save_feedback_to_postgres(
#         st.session_state.st1_to_st3_results,
#         st.session_state.submittal_st1_to_st3,
#         st.session_state.llm_result,
#         feedback,
#         comments
#     )
#     st.success("Thank you for your feedback!")

# # Clear Output Button
# if st.button("Clear Output"):
#     # Clear session state variables
#     st.session_state.st1_to_st3_results = None
#     st.session_state.step4_results = None
#     st.session_state.submittal_st1_to_st3 = None
#     st.session_state.submittal_st4 = None
#     st.session_state.llm_result = None
#     # Use query params to refresh the app
#     st.experimental_set_query_params()
