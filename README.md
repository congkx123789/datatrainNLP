# datatrainNLP - Lexicon-Constrained Machine Translation (Chinese to Vietnamese)

This repository contains the dataset preparation and local benchmarking framework for fine-tuning a lightweight, high-performance Chinese-Vietnamese translation model with dictionary constraints.

## Project Structure

- `data/`: Contains dictionaries and processed datasets.
  - `raw/hanviet.csv`: Sino-Vietnamese dictionary mapping.
  - `processed/train_constrained.jsonl`: Formatted data with inline lexical tags (`<vi: ...>`).
- `scripts/`: Contains Python scripts for benchmarking and data conversion.
  - `hanviet_converter.py`: Converts Chinese words to their Hán Việt equivalents.
  - `prepare_constrained_data.py`: Preprocesses text and embeds Hán Việt hints into Chinese sentences.
  - `train_tiny.py`: Hugging Face Seq2Seq model training script.
  - `optimize_and_benchmark.py`: Benchmarks model speed using CTranslate2 and quantization.
- `Huong_Dan_Colab.md`: Step-by-step tutorial on how to run training on Google Colab GPU.

## Quick Start (Local Benchmark)

Ensure you have the required dependencies:
```bash
pip install transformers torch sentencepiece sacremoses ctranslate2 zhconv jieba
```

Run the translation benchmark:
```bash
python scripts/optimize_and_benchmark.py
```
