import torch
import logging
from transformers import AutoModelForCausalLM, AutoTokenizer


logger = logging.getLogger("ai-llm")


class TinyLlamaClient:
    _instance = None
    _model = None
    _tokenizer = None
    _device = None

    _model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def initialize(self):
        if self._model is not None:
            return

        torch.set_num_threads(4)

        if torch.backends.mps.is_available():
            self._device = torch.device("mps")
            logger.info("Using MPS acceleration (Metal)")
        elif torch.cuda.is_available():
            self._device = torch.device("cuda")
            logger.info("Using CUDA acceleration")
        else:
            self._device = torch.device("cpu")
            logger.warning("Using CPU (without acceleration)")

        self._tokenizer = AutoTokenizer.from_pretrained(self._model_name)
        if self._tokenizer.pad_token is None:
            self._tokenizer.pad_token = self._tokenizer.eos_token

        self._model = AutoModelForCausalLM.from_pretrained(
            self._model_name,
            dtype=torch.float16,
            low_cpu_mem_usage=True,
        )

        self._model = self._model.to(self._device) # type: ignore
        self._model.eval()
        logger.info(f"Model {self._model_name} loaded on {self._device}")

    def generate(self, prompt: str, max_new_tokens: int = 64) -> str:
        if self._model is None or self._tokenizer is None:
            raise RuntimeError(
                "Model and tokenizer must be initialized. Call initialize() first."
            )

        inputs = self._tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=384,
        )

        inputs = {k: v.to(self._device) for k, v in inputs.items()}

        with torch.no_grad():
            output = self._model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=True,
                temperature=0.1,
                top_p=0.9,
                use_cache=True,
                pad_token_id=self._tokenizer.eos_token_id,
                eos_token_id=self._tokenizer.eos_token_id,
            )

        generated_tokens = output[0][inputs["input_ids"].shape[1] :]
        response = self._tokenizer.decode(
            generated_tokens,
            skip_special_tokens=True,
        ).strip()

        return response
