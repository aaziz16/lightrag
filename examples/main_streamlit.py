'''

# Developed by Abdul Aziz
# This Streamlit app is designed for document comparison using Light00 RAG for specification and submittal documnets
# Date: 10/25/2024




'''

import streamlit as st
import tempfile
import asyncio
import os
from pdf_extract import extract_text_from_image_pdf  # Your custom extraction function
from lightrag_azure_openai_demo import *  # Import necessary functions
from fpdf import FPDF  # Importing from fpdf2

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
    rag_specs = initialize_rag(WORKING_DIR_SPECS, embedding_dimension, llm_model_func, embedding_func, model_config_step1_3, chunk_token_size=1200)
    
    # Extract text and process the Specification Document
    spec_status_placeholder.write("**Extracting text from Specification Document...**")
    specs_output_txt_path = f"text_input/{os.path.basename(specs_document_path)}.txt"
    extract_text_from_image_pdf(specs_document_path, specs_output_txt_path)
    spec_status_placeholder.write("**Text extraction from Specification Document complete.**")

    # Load Specification Document text and execute query
    spec_status_placeholder.write("**Inserting text into RAG for Step 1-3 query on Specification Document...**")
    with open(specs_output_txt_path) as f:
        await rag_specs.ainsert(f.read())
    st1_to_st3_results = await execute_query(rag_specs, st1_to_st3_prompt)
    spec_status_placeholder.write("**Step 1-3 query on Specification Document complete.**")

    # Display Step 1-3 Results
    with tab1:
        st.write("### Step 1-3 Results for Specification Document")
        st.write(st1_to_st3_results)

    # Step 4 for Specification
    spec_status_placeholder.write("**Executing Step 4 query on Specification Document...**")
    rag_step4 = initialize_rag(WORKING_DIR_SPECS, embedding_dimension, llm_model_func, embedding_func, model_config_step4)
    formatted_step4_prompt = stp4_prompt.format(st1_st3=st1_to_st3_results)
    step4_results = await execute_query(rag_step4, formatted_step4_prompt)
    spec_status_placeholder.write("**Step 4 query on Specification Document complete.**")

    # Display Step 4 Results
    with tab1:
        st.write("### Step 4 Results for Specification Document")
        st.write(step4_results)

    return st1_to_st3_results, step4_results

# Async function for submittal processing
async def process_submittal(submittal_document_path, submittal_status_placeholder, tab2):
    embedding_dimension = 1536
    # model_config_step1_3 = get_model_config('step1_3')
    model_config_submittal = get_model_config('submittal_model')
    
    # Initialize RAG for Submittal
    submittal_status_placeholder.write("**Setting up submittal processing environment...**")
    setup_working_directory(WORKING_DIR_SUBMITTAL)
    rag_submittal = initialize_rag(WORKING_DIR_SUBMITTAL, embedding_dimension, llm_model_func, embedding_func, model_config_submittal, chunk_token_size=1300)
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
    submittal_st1_to_st3 = await execute_query(rag_submittal, submittal_st1_to_st3_prompt)
    submittal_status_placeholder.write("**Step 1-3 query on Submittal Document complete.**")

    # Display Step 1-3 Results
    with tab2:
        st.write("### Step 1-3 Results for Submittal Document")
        st.write(submittal_st1_to_st3)

    # Step 4 for Submittal
    submittal_status_placeholder.write("**Executing Step 4 query on Submittal Document...**")
    formatted_submittal_prompts4 = submittal_stp4_prompt.format(submittal_st1_to_st3=submittal_st1_to_st3)
    submittal_st4 = await execute_query(rag_submittal, formatted_submittal_prompts4)
    submittal_status_placeholder.write("**Step 4 query on Submittal Document complete.**")

    # Display Step 4 Results
    with tab2:
        st.write("### Step 4 Results for Submittal Document")
        st.write(submittal_st4)

    return submittal_st1_to_st3, submittal_st4

# Main pipeline to handle parallel execution
async def main_pipeline(specs_document_path, submittal_document_path, spec_status_placeholder, submittal_status_placeholder, tab1, tab2, tab3):
    # Run specification and submittal processing in parallel
    spec_results, submittal_results = await asyncio.gather(
        process_specification(specs_document_path, spec_status_placeholder, tab1),
        process_submittal(submittal_document_path, submittal_status_placeholder, tab2)
    )
    
    # Unpack results
    st1_to_st3_results, step4_results = spec_results
    submittal_st1_to_st3, submittal_st4 = submittal_results

    # Final Comparison Report
    status_placeholder = st.empty()
    status_placeholder.write("**Generating Final Comparison Report...**")
    formatted_comparison = comparison.format(specification_st4=step4_results, submittal_st4=submittal_st4)
    llm_result = await llm_model_func(formatted_comparison, get_model_config('specs_model'))
    status_placeholder.write("**Final Comparison Report generated.**")
    
    # Display Final Comparison Report
    with tab3:
        st.write("### Final Comparison Report")
        st.write(llm_result)

    return st1_to_st3_results, step4_results, submittal_st1_to_st3, submittal_st4, llm_result

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
        st1_to_st3_results, step4_results, submittal_st1_to_st3, submittal_st4, llm_result = asyncio.run(
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



# def clear_cache_and_restart():
#     """Clears all cached data and restarts the Streamlit app by resetting a session variable."""
#     st.cache_data.clear()       # Clears all @st.cache_data caches
#     st.cache_resource.clear()   # Clears all @st.cache_resource caches
    
#     # Trigger a rerun by modifying a session state variable
#     st.session_state["restart"] = not st.session_state.get("restart", False)

# # Add a button to the app to trigger the cache clear and restart
# if st.button("Clear Cache and Restart"):
#     clear_cache_and_restart()
