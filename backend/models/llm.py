import logging
import queue
import threading

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from config import GENERATION_TIMEOUT_SECONDS, HF_TOKEN, LOAD_IN_8BIT, MAX_NEW_TOKENS, MODEL_NAME

logger = logging.getLogger(__name__)

_tokenizer = None
_model = None
_model_ready = False
_load_lock = threading.Lock()
_inference_lock = threading.Lock()


class ModelLoadError(RuntimeError):
    pass


def load_model():
    global _model, _tokenizer, _model_ready
    if _model_ready:
        return
    with _load_lock:
        if _model_ready:
            return
        try:
            if not HF_TOKEN:
                logger.warning(
                    "HF_TOKEN is not set. Loading from Hugging Face Hub unauthenticated; "
                    "model downloads may be slower or throttled."
                )

            auth_args = {"use_auth_token": HF_TOKEN} if HF_TOKEN else {}
            _tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, **auth_args)
            model_kwargs = {
                "low_cpu_mem_usage": True,
                "dtype": torch.float32,
            }
            if LOAD_IN_8BIT:
                model_kwargs = {
                    "load_in_8bit": True,
                    "device_map": "auto",
                }
            _model = AutoModelForCausalLM.from_pretrained(
                MODEL_NAME,
                **model_kwargs,
                **auth_args,
            )
            _model.eval()
            _model_ready = True
        except Exception as error:
            raise ModelLoadError(f"AI model failed to load: {error}") from error


def _build_prompt_text(prompt_messages):
    if hasattr(_tokenizer, "chat_template") and _tokenizer.chat_template is not None:
        return _tokenizer.apply_chat_template(
            prompt_messages, tokenize=False, add_generation_prompt=True
        )

    parts = []
    for message in prompt_messages:
        role = message.get("role", "")
        content = message.get("content", "")
        if role:
            parts.append(f"[{role.upper()}] {content}")
        else:
            parts.append(content)
    return "\n\n".join(parts)


def _run_inference(prompt_messages, result_queue):
    try:
        tokenizer = _tokenizer
        model = _model
        prompt_text = _build_prompt_text(prompt_messages)
        inputs = tokenizer(
            prompt_text,
            return_tensors="pt",
            truncation=True,
            max_length=1024,
        )
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=MAX_NEW_TOKENS,
                do_sample=True,
                temperature=0.7,
                top_p=0.9,
                repetition_penalty=1.1,
                pad_token_id=tokenizer.eos_token_id,
            )
        generated_ids = outputs[0][inputs["input_ids"].shape[1]:]
        generated_text = tokenizer.decode(generated_ids, skip_special_tokens=True)
        result_queue.put(("success", generated_text))
    except Exception as error:
        result_queue.put(("error", str(error)))


def generate_text(prompt_messages):
    with _inference_lock:
        load_model()
        result_queue = queue.Queue()
        worker = threading.Thread(
            target=_run_inference,
            args=(prompt_messages, result_queue),
            daemon=True,
        )
        worker.start()
        worker.join(timeout=GENERATION_TIMEOUT_SECONDS)
        if worker.is_alive():
            raise TimeoutError("AI generation timed out. Please try again.")
        status, payload = result_queue.get()
        if status == "error":
            raise RuntimeError(f"AI generation failed: {payload}")
        return payload
