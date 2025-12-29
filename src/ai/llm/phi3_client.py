from transformers import AutoModelForCausalLM, AutoTokenizer
import torch


class Phi3Client:
    """
    Cliente para ejecutar inferencia con Phi-3 Instruct.
    Diseñado para RAG determinístico.
    """

    _instance = None
    _model = None
    _tokenizer = None

    _model_name: str = "microsoft/Phi-3-mini-4k-instruct"
    _device: str = "cuda" if torch.cuda.is_available() else "cpu"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def initialize(self) -> None:
        """
        Inicializa el modelo Phi-3.
        
        Debe llamarse una sola vez al levantar la aplicación.
        La primera carga puede ser lenta (descarga + carga en memoria),
        pero luego es rápida para inferencia.
        """
        if self._model is None or self._tokenizer is None:
            self._tokenizer = AutoTokenizer.from_pretrained(self._model_name)
            
            # Configurar el tokenizer con pad_token si no existe
            if self._tokenizer.pad_token is None:
                self._tokenizer.pad_token = self._tokenizer.eos_token
            
            self._model = AutoModelForCausalLM.from_pretrained(
                self._model_name,
                torch_dtype=torch.float16 if self._device == "cuda" else torch.float32,
                device_map="auto" if self._device == "cuda" else None,
                trust_remote_code=False,  # Cambiar a False para evitar código obsoleto
            )
            
            if self._device == "cpu":
                self._model = self._model.to(self._device)
            
            self._model.eval()  # Modo evaluación

    def is_initialized(self) -> bool:
        return self._model is not None and self._tokenizer is not None

    def generate(
        self,
        prompt: str,
        max_new_tokens: int = 256,
    ) -> str:
        if not self.is_initialized():
            raise RuntimeError(
                "Phi-3 model not initialized. Call initialize() first."
            )

        if not prompt or not prompt.strip():
            raise ValueError("Prompt cannot be empty")

        # Tokenizar el prompt
        inputs = self._tokenizer(prompt, return_tensors="pt").to(self._device)
        input_length = inputs["input_ids"].shape[1]

        # Generar respuesta
        with torch.no_grad():  # No calcular gradientes (modo inferencia)
            outputs = self._model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=False,
                temperature=0.0,
                pad_token_id=self._tokenizer.eos_token_id,
                eos_token_id=self._tokenizer.eos_token_id,
                use_cache=False,  # Deshabilitar caché para evitar problemas con DynamicCache
            )

        # Decodificar solo la parte generada (excluir el prompt original)
        generated_tokens = outputs[0][input_length:]
        generated_text = self._tokenizer.decode(
            generated_tokens, skip_special_tokens=True
        )

        return generated_text.strip()

