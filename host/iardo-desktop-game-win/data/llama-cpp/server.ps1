llama-server `
  --model "$env:USERPROFILE\llms\models\llamacpp\qwen3.5-9B-Q4_K_S.gguf" `
  --mmproj "$env:USERPROFILE\llms\models\llamacpp\qwen3.5-9B-mmproj-f16.gguf" `
  --alias qwen3.5-9b `
  --ctx-size 24576 `
  --port 8080 `
  --host 0.0.0.0 `
  --n-gpu-layers 999 `
  --jinja `
  --flash-attn on
