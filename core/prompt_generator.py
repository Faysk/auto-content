# core/prompt_generator.py
from pathlib import Path
import re # For parsing the GPT response

# --- Configurable Constants ---
DEFAULT_NEGATIVE_PROMPT = "ugly, deformed, bad anatomy, disfigured, low quality, blurry, distorted limbs, text, watermark, signature, username, artist name, poorly drawn, extra fingers, mutated hands, fused fingers, conjoined"
# Keys to extract prompts from GPT's response (important that the GPT meta-prompt uses these)
GPT_POSITIVE_PROMPT_KEY = "POSITIVE_PROMPT:"
GPT_NEGATIVE_PROMPT_KEY = "NEGATIVE_PROMPT:"

# --- Helper Functions ---

def _load_text_content_from_file(file_path: Path, is_optional: bool = False, logger=None) -> str | None:
    """
    Robustly loads text content from a file.

    :param file_path: Path object to the file.
    :param is_optional: If True, returns None and logs a warning if the file doesn't exist or is empty.
                        If False, raises an error in those situations.
    :param logger: Optional instance of your logger.
    :return: File content as a string, or None if optional and not found/empty/error.
    :raises FileNotFoundError: If the file is not found and is_optional is False.
    :raises ValueError: If a mandatory file is empty.
    :raises IOError: If a read error occurs.
    """
    if logger:
        logger.log(f"ℹ️ Attempting to load file: {file_path}")
    if not file_path.exists():
        if is_optional:
            if logger:
                logger.log(f"⚠️ Optional file not found: {file_path}")
            return None
        else:
            if logger:
                logger.erro(f"CRITICAL ERROR: File not found: {file_path}")
            raise FileNotFoundError(f"File not found: {file_path}")
    try:
        content = file_path.read_text(encoding="utf-8").strip()
        if not content:
            if is_optional:
                if logger:
                    logger.log(f"⚠️ Optional file ({file_path}) found, but it is empty.")
                return None
            else:
                if logger:
                    logger.erro(f"CRITICAL ERROR: Mandatory file ({file_path}) is empty.")
                raise ValueError(f"Mandatory file ({file_path}) is empty.")
        
        if logger:
            logger.log(f"📄 Content successfully loaded from: {file_path}")
        return content
    except IOError as e:
        if logger:
            logger.erro(f"I/O ERROR reading file {file_path}: {e}")
        if is_optional:
            return None
        raise  # Re-raises the error if not optional


def _parse_gpt_image_prompt_response(gpt_response_text: str, logger=None) -> dict | None:
    """
    Parses the GPT response string to extract positive and negative prompts.
    Expected format in GPT response:
    POSITIVE_PROMPT: [positive prompt here]
    NEGATIVE_PROMPT: [negative prompt here]

    :param gpt_response_text: The full GPT response as a string.
    :param logger: Optional instance of your logger.
    :return: Dictionary with {"prompt": ..., "negative_prompt": ...} or None if parsing fails.
    """
    if logger:
        logger.log("ℹ️ Parsing GPT response to extract image prompts...")
    
    positive_prompt = None
    negative_prompt_from_gpt = None

    # Try to extract the positive prompt
    # Searches for "POSITIVE_PROMPT:" at the start of a line (case-insensitive, multiline)
    # and captures everything after it until the end of the line or until "NEGATIVE_PROMPT:" is found
    positive_match = re.search(
        rf"^{GPT_POSITIVE_PROMPT_KEY}(.*?)(?=\n{GPT_NEGATIVE_PROMPT_KEY}|$)",
        gpt_response_text,
        re.IGNORECASE | re.MULTILINE | re.DOTALL
    )
    if positive_match:
        positive_prompt = positive_match.group(1).strip()
        if logger:
            logger.log(f"👍 Positive prompt extracted from GPT: '{positive_prompt[:100]}...'")

    # Try to extract the negative prompt
    negative_match = re.search(
        rf"^{GPT_NEGATIVE_PROMPT_KEY}(.*)",
        gpt_response_text,
        re.IGNORECASE | re.MULTILINE | re.DOTALL
    )
    if negative_match:
        negative_prompt_from_gpt = negative_match.group(1).strip()
        if logger:
            logger.log(f"👎 Negative prompt extracted from GPT: '{negative_prompt_from_gpt[:100]}...'")

    if positive_prompt:
        return {
            "prompt": positive_prompt,
            "negative_prompt": negative_prompt_from_gpt if negative_prompt_from_gpt else DEFAULT_NEGATIVE_PROMPT
        }
    else:
        if logger:
            logger.erro(
                f"Failed to extract positive prompt from GPT response. Received response (start): '{gpt_response_text[:200]}...'"
            )
        return None


def _generate_prompts_simple_method(
    text_segment: str,
    base_style_content: str | None = None,
    logger=None
) -> dict:
    """
    Simple fallback method: Generates a positive prompt by combining the text segment
    with optional base style content. Uses a default negative prompt.
    """
    if logger:
        logger.log(f"⚙️ Generating image prompt using simple method for: '{text_segment[:70]}...'")
    
    final_positive_prompt = text_segment.strip()
    if base_style_content:
        final_positive_prompt = f"{base_style_content.strip()}, {text_segment.strip()}"
    # else: # The "no additional base" warning can be given by the main calling function
        # print("⚠️  Generating positive prompt using only the text segment (no additional style base).")

    # The default negative prompt is defined as a module-level constant.
    # It could be made more configurable in the future (e.g., read from base_style_content).
    final_negative_prompt = DEFAULT_NEGATIVE_PROMPT
    
    return {
        "prompt": final_positive_prompt,
        "negative_prompt": final_negative_prompt
    }

# --- MAIN EXPORTED FUNCTION (used by main.py) ---
# This is the function your main.py attempts to import.
def generate_prompts_for_text(
    text_segment: str,
    base_prompt_content: str | None = None, # Optional content from prompt.txt for style/guidance
    use_gpt_for_image_prompts: bool = False, # CONTROLS WHETHER GPT IS USED!
    gpt_api_function = None, # Reference to your function that calls the GPT API
    logger = None # Your logger instance (optional, for internal logging)
) -> dict:
    """
    Main entry point to generate image prompts (positive and negative) for a text segment.

    Can utilize a GPT API call to generate more creative and contextual prompts,
    or a simpler string combination method as a fallback or option.

    :param text_segment: The piece of text for which to generate prompts.
    :param base_prompt_content: Optional string (e.g., content from prompt.txt) to:
                                 - Add style/prefix to the prompt (simple method).
                                 - Guide GPT in prompt generation (GPT method).
    :param use_gpt_for_image_prompts: Boolean. If True, attempts to use GPT. If False or if gpt_api_function
                                     is not provided, uses the simple method.
    :param gpt_api_function: A Python function you must provide to call the GPT API.
                             This function should accept a single argument (string: the meta-prompt for GPT)
                             and return the GPT's response as a string.
                             Example signature: def my_gpt_function(prompt_for_api: str) -> str: ...
    :param logger: Optional instance of your logger for internal messages.
    :return: Dictionary with keys "prompt" (positive prompt) and "negative_prompt".
    """
    # Replace 'print' with logger calls if logger is passed
    # Ex: if logger: logger.log("...") else: print("...")

    if not text_segment or not text_segment.strip():
        if logger:
            logger.erro("ERROR: Text segment provided to 'generate_prompts_for_text' is empty or whitespace.")
        # Return defaults to avoid breaking the main flow, but clearly indicate failure.
        return {"prompt": "Text segment was empty.", "negative_prompt": DEFAULT_NEGATIVE_PROMPT}

    cleaned_text_segment = text_segment.strip()

    if use_gpt_for_image_prompts:
        if not gpt_api_function:
            if logger:
                logger.log("⚠️ WARNING: GPT image prompt generation was requested, but no 'gpt_api_function' was provided.")
                logger.log("Falling back to the simple prompt generation method.")
            return _generate_prompts_simple_method(cleaned_text_segment, base_prompt_content, logger)

        if logger:
            logger.log(f"🧠 Attempting to generate image prompts with GPT for segment: '{cleaned_text_segment[:70]}...'")
        
        # ---- CONSTRUCTION OF THE META-PROMPT FOR GPT ----
        # This is an example. You can refine this meta-prompt extensively!
        meta_prompt_instructions = f"""
You are an expert assistant specialized in creating highly effective prompts for AI image generation models (like Stable Diffusion, DALL-E, Midjourney).
Your task is, from the provided "Text Segment," to generate a vivid and descriptive "Positive Prompt" for an image, and a concise "Negative Prompt" listing elements to avoid.

Provided Text Segment:
"{cleaned_text_segment}"
"""
        if base_prompt_content: # If a base style/context was loaded from prompt.txt
            meta_prompt_instructions += f"""
Additional Style/Context Guide (use this to influence the tone, artistic style, or key elements of your prompts):
"{base_prompt_content}"
"""
        meta_prompt_instructions += f"""
Detailed Instructions for Your Response:
1.  **Positive Prompt**:
    * Should be rich in visual details, describing the scene, subjects, environment, lighting, colors, emotion, and, if applicable, artistic style (e.g., 'cinematic photography', 'digital watercolor painting', 'sci-fi concept art').
    * Translate the essence of the "Text Segment" into a description an image model can visually interpret.
    * Avoid phrases like "an image of..." or "draw a...". Get straight to the description.
    * Maximum of 150 words.

2.  **Negative Prompt**:
    * Should be a list of terms or short phrases, separated by commas, describing what should be AVOIDED in the image.
    * Include generic low-quality terms (e.g., blurry, pixelated, deformed, bad anatomy), as well as specific elements to avoid based on the context of the positive prompt, if applicable.
    * Maximum of 50 words.

Please format your response EXACTLY as follows, with no additional introductory or concluding text:
{GPT_POSITIVE_PROMPT_KEY} [Your generated positive prompt here]
{GPT_NEGATIVE_PROMPT_KEY} [Your generated negative prompt here]
"""
        # ---- END OF META-PROMPT CONSTRUCTION ----

        try:
            if logger:
                logger.log("✉️ Sending request to GPT API (to generate image prompts)...")
            # This is the call to your function that interacts with the GPT API
            raw_gpt_response = gpt_api_function(meta_prompt_instructions)
            
            if not raw_gpt_response or not raw_gpt_response.strip():
                if logger:
                    logger.erro("ERROR: GPT API returned an empty or invalid response when trying to generate image prompts.")
                raise ValueError("Empty response from GPT API for image prompts.")

            parsed_prompts = _parse_gpt_image_prompt_response(raw_gpt_response, logger)

            if parsed_prompts and "prompt" in parsed_prompts:
                if logger:
                    logger.sucesso("Image prompts (positive and negative) successfully generated via GPT.")
                return parsed_prompts
            else:
                if logger:
                    logger.erro("Failed to parse prompts from GPT response. The response might not be in the expected format.")
                    logger.log("⚠️  Falling back to the simple prompt generation method due to GPT parsing error.")
                return _generate_prompts_simple_method(cleaned_text_segment, base_prompt_content, logger)

        except Exception as e_gpt_call:
            if logger:
                logger.erro(f"ERROR during GPT API call for image prompts or response processing: {e_gpt_call}")
                logger.log("⚠️  Falling back to the simple prompt generation method due to GPT failure.")
            return _generate_prompts_simple_method(cleaned_text_segment, base_prompt_content, logger)
    else:
        # GPT not requested, use the simple method
        if logger:
            logger.log("⚙️  GPT prompt generation disabled. Using simple method.")
        return _generate_prompts_simple_method(cleaned_text_segment, base_prompt_content, logger)

# The old function `carregar_arquivo_prompt` has been replaced by `_load_text_content_from_file`
# and is more robust. If your main.py was directly calling the old one, it would need to be updated,
# but it seems main.py was already loading its primary prompt.txt itself.
# This new `_load_text_content_from_file` is more of an internal utility or for loading
# other potential config files for this module in the future.