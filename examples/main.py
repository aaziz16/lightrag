

'''

# Developed by Abdul Aziz
#Contains main function to run light rag on terminal
# Date: 10/25/2024



'''


from pdf_extract import extract_text_from_image_pdf
from lightrag_azure_openai_demo import *


# Define working directories
WORKING_DIR_SPECS = "input"
WORKING_DIR_SUBMITTAL = "sub_input"

# File paths for specification and submittal documents
specs_document_path = r"specification_documents/092116-Gypsum-Board-Assemblies-Rev 01-230310.pdf"
specs_output_txt_path = f"text_input/{specs_document_path.split('/')[-1]}.txt"

submittal_document_path = r"submittal_documents/revised_gupsum.pdf"
submittal_output_txt_path = f"text_input/{submittal_document_path.split('/')[-1]}.txt"

# Function to dynamically set up model configurations for each step
def get_model_config(step):
    """Returns model configuration based on the step."""
    model_configs = {
        'step1_3': {
            'api_version': "2024-02-15-preview",
            'deployment': "gpt-4o-2",
            'api_key': "9101287fb67e484b9970dd8d7e31aa05",
            'endpoint': "https://diesl-eus-openai-dev.openai.azure.com/",
            'embedding_deployment': "text-embedding-ada-002",
            'embedding_api_version': "2024-02-15-preview"
        },
        'step4': {
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
            'api_key': "53b705775b4c4eb4845a179433dab2a2",
            'endpoint': "https://aaziz-m2mfpibj-westus.openai.azure.com/",
            'embedding_deployment': "text-embedding-ada-002",
            'embedding_api_version': "2024-02-15-preview"
        },
    }
    return model_configs[step]


async def main_pipeline():
    """Main pipeline that extracts text from PDFs, inserts into RAG, and runs queries."""
    
    # Set up working directory for specs
    setup_working_directory(WORKING_DIR_SPECS)

    # Initialize RAG for step 1-3 using a specific model
    embedding_dimension = 1536
    model_config_step1_3 = get_model_config('step1_3')
    rag_specs = initialize_rag(WORKING_DIR_SPECS, embedding_dimension, llm_model_func, embedding_func, model_config_step1_3,chunk_token_size=1200)

    # Extract text from the specification document and log
    print("######## PROCESSING SPECIFICATION PDF TO TEXT ########")
    specs_document = extract_text_from_image_pdf(specs_document_path, specs_output_txt_path)
    print("######## PDF TO TEXT CONVERSION COMPLETE ########", f"Text saved at: {specs_output_txt_path}")

    # Load text from specs document into RAG asynchronously
    with open(specs_output_txt_path) as f:
        await rag_specs.ainsert(f.read())

    # Query RAG for step 1-3 results and log
    print("######## RUNNING QUERY FOR STEP 1-3 ########")
    st1_to_st3_results = await execute_query(rag_specs, st1_to_st3_prompt)
    print("######## STEP 1-3 QUERY RESULTS ########")
    print(st1_to_st3_results)

    # Initialize RAG for step 4 using a different model
    model_config_step4 = get_model_config('step4')
    rag_step4 = initialize_rag(WORKING_DIR_SPECS, embedding_dimension, llm_model_func, embedding_func, model_config_step4)

    # Query RAG for step 4 results using results from step 1-3
    formatted_step4_prompt = stp4_prompt.format(st1_st3=st1_to_st3_results)
    print("######## RUNNING QUERY FOR STEP 4 ########")
    print("Step 4 Prompt:", formatted_step4_prompt)
    step4_results = await execute_query(rag_step4, formatted_step4_prompt)
    print("######## STEP 4 QUERY RESULTS ########")
    print(step4_results)

    ########### Submittal Processing ###########

    # Set up working directory for submittal verification
    setup_working_directory(WORKING_DIR_SUBMITTAL)
    
    # Initialize RAG for submittal using model config
    model_config_submittal = get_model_config('step1_3')
    rag_submittal = initialize_rag(WORKING_DIR_SUBMITTAL, embedding_dimension, llm_model_func, embedding_func, model_config_step1_3,chunk_token_size=1300)

    # Extract text from the submittal document and log
    print("######## PROCESSING SUBMITTAL PDF TO TEXT ########")
    submittal_document = extract_text_from_image_pdf(submittal_document_path, submittal_output_txt_path)
    print("######## PDF TO TEXT CONVERSION COMPLETE ########", f"Text saved at: {submittal_output_txt_path}")

    # Load text from submittal document into RAG asynchronously
    with open(submittal_output_txt_path) as f:
        await rag_submittal.ainsert(f.read())

    print("######## RUNNING submittal for stp1 to step 3########")

    submittal_st1_to_st3 = await execute_query(rag_submittal, submittal_st1_to_st3_prompt)

    print(submittal_st1_to_st3)


    print("######## RUNNING submittal for step4########")
    formatted_submittal_prompts4 = submittal_stp4_prompt.format(submittal_st1_to_st3=submittal_st1_to_st3)


    submittal_st4 = await execute_query(rag_submittal, formatted_submittal_prompts4)
    print(submittal_st4)


    print("######## RUNNING Comparison########")
    formatted_comparison = comparison.format(specification_st4=step4_results,submittal_st4=submittal_st4)

    print("###########Comparison POMPT########")
    print(formatted_comparison)
    print("###########Comparison REPORT########")




    # comparison_report = await execute_query(rag_submittal, formatted_submittal_prompts4)
    llm_result = await llm_model_func(formatted_comparison, model_config_submittal)
    print(llm_result)




    # # Query RAG for submittal verification using results from step 4
    # formatted_submittal_prompt1 = submittal_prompt.format(st4=step4_results)
    # print("######## RUNNING QUERY FOR SUBMITTAL VERIFICATION ########")
    # print("Submittal Prompt:", formatted_submittal_prompt)
    # submittal_results = await execute_query(rag_submittal, formatted_submittal_prompt)
    # print("######## SUBMITTAL QUERY RESULTS ########")
    # print(submittal_results)


# Run the pipeline
if __name__ == "__main__":
    asyncio.run(main_pipeline())
