import asyncio
import shutil
# import time # Uncomment if used directly, e.g., for deliberate delays
from datetime import datetime
from pathlib import Path
import traceback # For detailed error logging

# === IMPORTS FROM YOUR MODULES ===
# Ensure these import paths correctly match your project structure.
from core.logger import Logger
from core.prompt_generator import generate_prompts_for_text
from text_generator.text_creator import generate_text, slugify
from text_to_speech.tts_generator import (generate_audio_and_srt,
                                          split_text_into_segments)
from txt_image.core.image_generator import generate_image_with_prompt

# === GLOBAL CONFIGURATIONS ===
# --- Process Control ---
MAX_WORDS_PER_SRT_LINE = 10
# Set to True to use GPT for generating image prompts (positive/negative) for each text segment.
# If True, 'gpt_api_call_function_for_image_prompts' below must be correctly implemented.
# If False, a simpler method (text_segment + base_style) will be used for image prompts.
USE_GPT_FOR_IMAGE_PROMPTS = False # CHANGE TO True TO ENABLE GPT FOR IMAGE PROMPTS

# --- Path Configurations ---
PROJECT_ROOT_DIRECTORY = Path(__file__).resolve().parent
IMAGE_PROMPT_BASE_STYLE_FILENAME = "prompt.txt" # Optional file in root for image prompt base style
FINAL_PROJECTS_OUTPUT_DIRECTORY = Path("D:/Projects") # Your main output directory for finished projects

# --- Logger Initialization & Session ID ---
SESSION_ID = datetime.now().strftime("%Y%m%d_%H%M%S")
logger = Logger(base_name=f"session_{SESSION_ID}", log_dir="logs")

# --- Session-Specific Temporary Output Directory ---
session_temp_output_dir = PROJECT_ROOT_DIRECTORY / "image_video" / "outputs" / f"session_{SESSION_ID}"
try:
    session_temp_output_dir.mkdir(parents=True, exist_ok=True)
    logger.log(f"Session directory created/confirmed: {session_temp_output_dir}")
except Exception as e_mkdir:
    logger.erro(f"CRITICAL ERROR: Failed to create session directory '{session_temp_output_dir}': {e_mkdir}")
    raise SystemExit(f"Critical error: Could not create session directory. {e_mkdir}")

# === GPT API CALL FUNCTION (FOR IMAGE PROMPTS) ===
# IMPORTANT: You need to implement the logic to call your GPT model here.
# This function will be passed to core.prompt_generator.generate_prompts_for_text.
async def gpt_api_call_function_for_image_prompts(meta_prompt_for_gpt: str) -> str | None:
    """
    Placeholder function to call your GPT API for generating image prompts.
    This function needs to be implemented with your actual API call logic.

    :param meta_prompt_for_gpt: The fully constructed prompt to send to the GPT model.
    :return: The raw text response from GPT, or None if an error occurs.
    """
    logger.log(f"  📞 Attempting to call GPT API for image prompt generation...")
    #   (Your actual GPT API call logic would go here)
    #   Example (replace with your actual implementation):
    #   from openai import OpenAI
    #   client = OpenAI(api_key="YOUR_OPENAI_API_KEY")
    #   try:
    #       response = await asyncio.to_thread(
    #           client.chat.completions.create,
    #           model="gpt-3.5-turbo", # Or your preferred model
    #           messages=[{"role": "user", "content": meta_prompt_for_gpt}],
    #           temperature=0.7,
    #           max_tokens=250
    #       )
    #       gpt_response_content = response.choices[0].message.content
    #       logger.log("    ✅ GPT API call successful.")
    #       return gpt_response_content
    #   except Exception as e_gpt_call_api:
    #       logger.erro(f"    ❌ ERROR during GPT API call for image prompts: {e_gpt_call_api}")
    #       return None

    # --- START OF PLACEHOLDER/SIMULATION ---
    # Remove or replace this simulation block with your actual GPT API call.
    logger.log("    ⚠️ SIMULATING GPT call for image prompts (actual API call not implemented in placeholder).")
    await asyncio.sleep(1) # Simulate network delay
    simulated_gpt_response = f"""
POSITIVE_PROMPT: A vibrant, detailed concept art of a futuristic cityscape at dusk, with flying vehicles and neon lights, style of Syd Mead.
NEGATIVE_PROMPT: blurry, pixelated, watermark, signature, text, day time, poorly drawn vehicles
    """
    logger.log(f"    模拟 GPT response: {simulated_gpt_response.strip()}")
    return simulated_gpt_response
    # --- END OF PLACEHOLDER/SIMULATION ---

    # If you haven't implemented the actual call yet, return None to use the fallback:
    # logger.erro("    ❌ Actual GPT API call for image prompts is not implemented in 'gpt_api_call_function_for_image_prompts'.")
    # return None


# === HELPER FUNCTION: FILE ORGANIZATION ===
def move_files_to_final_organized_structure(
    source_session_dir: Path,
    project_name_slug: str,
    project_date_formatted: str
):
    """
    Moves files from the temporary session directory to a final, organized project folder.
    """
    if not project_name_slug or project_name_slug == "undefined_project":
        logger.erro("Project name is invalid or undefined. Files will not be moved to the final structure.")
        logger.log(f"Files will remain in the session directory: {source_session_dir}")
        return

    final_project_destination_root = FINAL_PROJECTS_OUTPUT_DIRECTORY / f"{project_name_slug} - {project_date_formatted}"
    logger.log(f"Target final destination directory for this project: {final_project_destination_root}")

    extension_to_folder_map = {
        ".png": "IMG", ".jpeg": "IMG", ".jpg": "IMG", ".gif": "IMG", ".webp": "IMG",
        ".mp3": "Audio", ".wav": "Audio", ".ogg": "Audio",
        ".srt": "TXT", ".txt": "TXT",
        ".log": "LOGS_PROJECT", # Renamed to avoid conflict with main logs folder
        ".json": "METADATA_PROJECT", # Renamed
        ".dbg": "DEBUG_PROJECT" # Renamed
    }

    created_final_folders = {}
    try:
        final_project_destination_root.mkdir(parents=True, exist_ok=True)
        for ext, folder_type_name in extension_to_folder_map.items():
            # Subfolder names incorporate project name and date for clarity, except for generic types
            final_subfolder_name_str = f"{folder_type_name}_{project_name_slug}-{project_date_formatted}"
            if folder_type_name in ["METADATA_PROJECT", "LOGS_PROJECT", "DEBUG_PROJECT"]:
                final_subfolder_name_str = folder_type_name # Simpler names for these
            
            full_final_subfolder_path = final_project_destination_root / final_subfolder_name_str
            full_final_subfolder_path.mkdir(parents=True, exist_ok=True)
            created_final_folders[ext] = full_final_subfolder_path
    except Exception as e_create_final_dirs:
        logger.erro(f"CRITICAL ERROR: Failed to create final destination folder structure at '{final_project_destination_root}': {e_create_final_dirs}")
        logger.log(f"Session files will not be moved. Please check permissions and path. Files remain at: {source_session_dir}")
        return

    logger.log(f"Moving files from session directory '{source_session_dir}' to final organized structure...")
    files_moved_successfully = 0
    files_ignored_or_failed = 0

    for item in source_session_dir.iterdir():
        if item.is_file():
            file_ext = item.suffix.lower()
            target_subfolder = created_final_folders.get(file_ext)
            if target_subfolder:
                destination_file_path = target_subfolder / item.name
                try:
                    item.rename(destination_file_path)
                    files_moved_successfully += 1
                except Exception as e_move_file:
                    logger.erro(f"  ✗ Error moving file '{item.name}' to '{destination_file_path}': {e_move_file}")
                    files_ignored_or_failed += 1
            else:
                logger.log(f"  ? File ignored (extension '{file_ext}' not mapped for final organization): {item.name}")
                files_ignored_or_failed += 1
    
    if files_moved_successfully > 0:
        logger.sucesso(f"File organization complete. Files successfully moved: {files_moved_successfully}.")
    else:
        logger.log("No files were moved to the final structure (either no files were generated/mapped or all moves failed).")
    if files_ignored_or_failed > 0:
        logger.log(f"Files ignored or failed to move: {files_ignored_or_failed}.")

# === MAIN ASYNCHRONOUS EXECUTION FLOW ===
async def execute_automated_content_pipeline():
    """
    Orchestrates the entire automated content creation pipeline.
    """
    logger.destaque("🚀 STARTING AUTOMATED CONTENT GENERATION PIPELINE 🚀")

    # --- Load Optional Base Style Prompt for Images ---
    image_prompt_style_base_path = PROJECT_ROOT_DIRECTORY / IMAGE_PROMPT_BASE_STYLE_FILENAME
    image_prompt_style_base_content = None
    try:
        if image_prompt_style_base_path.exists():
            content_read = image_prompt_style_base_path.read_text(encoding="utf-8").strip()
            if content_read:
                image_prompt_style_base_content = content_read
                logger.log(f"📄 Image prompt style base loaded from: {image_prompt_style_base_path}")
            else:
                logger.log(f"⚠️  Image prompt style base file ({image_prompt_style_base_path}) is empty. Proceeding without it.")
        else:
            logger.log(f"⚠️  Image prompt style base file ({image_prompt_style_base_path}) not found. Image prompts will be generated without this style base.")
    except Exception as e_load_img_prompt_base:
        logger.erro(f"❌ Error loading image prompt style base file ({image_prompt_style_base_path}): {e_load_img_prompt_base}")
        logger.log("Continuing without image prompt style base.")

    # --- STEP 1: MAIN TEXT GENERATION (GPT) ---
    logger.bloco("🧠 STEP 1: GENERATING MAIN SCRIPT TEXT")
    full_generated_text_script = None
    project_name_slug = "untitled_project"
    session_files_base_name = f"{project_name_slug}_{SESSION_ID}"
    try:
        # generate_text() is assumed to handle its own prompt.txt for GPT input
        full_generated_text_script = await asyncio.to_thread(generate_text) # Use .to_thread if generate_text is synchronous
        if not full_generated_text_script or not full_generated_text_script.strip():
            raise ValueError("Main text generation (GPT) returned an empty or invalid result.")
        
        first_valid_line_for_title = next((line for line in full_generated_text_script.splitlines() if line.strip()), project_name_slug)
        project_name_slug = slugify(first_valid_line_for_title)
        session_files_base_name = f"{project_name_slug}_{SESSION_ID}"
        logger.sucesso(f"📝 Main script text generated successfully. Project identifier for this session: '{project_name_slug}'")
    except Exception as e_main_text_gen:
        logger.erro(f"❌ CRITICAL FAILURE at Step 1 - Main Text Generation: {e_main_text_gen}")
        raise SystemExit("Aborting: Unrecoverable error during main text generation.")

    # --- STEP 1.B: TEXT SEGMENTATION ---
    script_text_segments = []
    try:
        script_text_segments = split_text_into_segments(full_generated_text_script, max_words=MAX_WORDS_PER_SRT_LINE)
        if not script_text_segments:
            logger.log("⚠️  The generated main text did not result in any processable segments.")
        else:
            logger.sucesso(f"✅ Main text successfully segmented into {len(script_text_segments)} parts.")
    except Exception as e_text_segmentation:
        logger.erro(f"❌ CRITICAL FAILURE at Step 1.B - Text Segmentation: {e_text_segmentation}")
        raise SystemExit("Aborting: Unrecoverable error during text segmentation.")

    # --- STEP 2: AUDIO AND SRT FILE GENERATION (for the full script) ---
    logger.bloco("🔊 STEP 2: GENERATING AUDIO & SRT SUBTITLES (for full script)")
    try:
        # generate_audio_and_srt expects (text, base_name)
        # It should ideally save files into session_temp_output_dir or allow specifying it.
        await generate_audio_and_srt(full_generated_text_script, session_files_base_name)
        logger.sucesso(f"🎧 Audio and SRT subtitles for the full script generated (base name: {session_files_base_name}).")
    except Exception as e_audio_gen:
        logger.erro(f"❌ Error during Step 2 - Audio/SRT Generation: {e_audio_gen}")
        logger.log("Continuing process. Full script audio/SRT might be unavailable.")

    # --- STEP 3 & 4: IMAGE PROMPT GENERATION AND IMAGE GENERATION (per segment) ---
    logger.bloco("🖼️ STEPS 3 & 4: GENERATING IMAGE PROMPTS AND IMAGES (per segment)")
    if not script_text_segments:
        logger.log("⚠️  No text segments available; skipping image prompt and image generation.")
    else:
        num_total_segments = len(script_text_segments)
        logger.log(f"Starting image generation process for {num_total_segments} text segments...")

        for i, current_segment_text in enumerate(script_text_segments):
            image_file_prefix = f"{session_files_base_name}_img_{i:03d}"
            logger.log(f"  🖼️ Processing Segment {i + 1}/{num_total_segments} for image: \"{current_segment_text[:70].strip()}...\"")

            comfyui_prompts = None
            try:
                # This call now includes parameters for GPT-based image prompt generation
                comfyui_prompts = generate_prompts_for_text(
                    text_segment=current_segment_text,
                    base_prompt_content=image_prompt_style_base_content,
                    use_gpt_for_image_prompts=USE_GPT_FOR_IMAGE_PROMPTS,
                    gpt_api_function=gpt_api_call_function_for_image_prompts if USE_GPT_FOR_IMAGE_PROMPTS else None,
                    logger=logger # Pass logger if generate_prompts_for_text is adapted to use it
                )
                logger.log(f"    👍 Positive Image Prompt: {comfyui_prompts['prompt'][:100]}...")
                logger.log(f"    👎 Negative Image Prompt: {comfyui_prompts['negative_prompt'][:100]}...")
            except Exception as e_gen_img_prompts:
                logger.erro(f"    ✗ Error generating image prompts for segment {i + 1}: {e_gen_img_prompts}")
                logger.log(f"    ⚠️  Skipping image generation for this segment.")
                continue # Move to the next segment

            try:
                # generate_image_with_prompt must ensure images are saved to session_temp_output_dir
                await asyncio.to_thread( # Use if generate_image_with_prompt is synchronous
                    generate_image_with_prompt,
                    prompt_positivo=comfyui_prompts["prompt"],
                    prompt_negativo=comfyui_prompts["negative_prompt"],
                    output_path=session_temp_output_dir, # Crucial for SaveImage node
                    nome_base=image_file_prefix
                )
                logger.sucesso(f"    ✅ Image request for segment {i + 1} sent (file prefix: {image_file_prefix}).")
            except Exception as e_send_to_comfy:
                logger.erro(f"    ✗ Error sending image request to ComfyUI for segment {i + 1}: {e_send_to_comfy}")
                logger.log(f"    ⚠️  Failed attempt to generate image for this segment. Ensure ComfyUI is running and accessible via network.")

    # --- FINALIZATION AND FILE ORGANIZATION ---
    logger.destaque("🏁 CONTENT GENERATION PIPELINE COMPLETED (MAIN PROCESSING) 🏁")
    logger.log(f"📁 Intermediate files (if any were successfully generated) are in: {session_temp_output_dir}")
    
    log_file_path_str = "Not specified (check 'logs' folder)"
    if hasattr(logger, 'caminho') and callable(logger.caminho):
         log_file_path_str = str(logger.caminho())
    elif hasattr(logger, 'log_file_path'):
         log_file_path_str = str(logger.log_file_path)
    logger.log(f"📄 Full session log saved at: {log_file_path_str}")

    logger.bloco("📦 FINAL STEP: ORGANIZING GENERATED FILES INTO FINAL STRUCTURE")
    todays_formatted_date = datetime.now().strftime("%d-%m-%Y")
    move_files_to_final_organized_structure(
        session_temp_output_dir,
        project_name_slug,
        todays_formatted_date
    )

# === SCRIPT ENTRY POINT ===
if __name__ == "__main__":
    try:
        asyncio.run(execute_automated_content_pipeline())
    except SystemExit as e_sys_exit:
        logger.erro(f"🛑 Process terminated prematurely due to a critical error: {e_sys_exit}")
    except KeyboardInterrupt:
        logger.log("⌨️ Execution interrupted by user (Ctrl+C).")
    except Exception as e_unhandled_main:
        logger.erro(f"💥 FATAL UNHANDLED ERROR at script's main level: {e_unhandled_main}")
        logger.erro("Error Details (Traceback):\n" + traceback.format_exc())
    finally:
        logger.log("✨ Automated content script 'main.py' execution finished. ✨")