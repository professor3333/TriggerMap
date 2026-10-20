"""A tiny BERT-style encoder and WordPiece tokenizer built locally (no downloads)."""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

from tokenizers import Tokenizer, models, normalizers, pre_tokenizers, processors, trainers
from transformers import AutoModel, BertConfig, PreTrainedTokenizerFast

SPECIAL = ["[PAD]", "[UNK]", "[CLS]", "[SEP]", "[MASK]"]


def build_tiny_base(directory: Path, corpus: Iterable[str], seed: int = 0) -> Path:
    tokenizer = Tokenizer(models.WordPiece(unk_token="[UNK]"))
    tokenizer.normalizer = normalizers.BertNormalizer(lowercase=False)
    tokenizer.pre_tokenizer = pre_tokenizers.BertPreTokenizer()
    trainer = trainers.WordPieceTrainer(vocab_size=400, special_tokens=SPECIAL)
    tokenizer.train_from_iterator(list(corpus), trainer)
    cls_id, sep_id = tokenizer.token_to_id("[CLS]"), tokenizer.token_to_id("[SEP]")
    tokenizer.post_processor = processors.TemplateProcessing(
        single="[CLS] $A [SEP]",
        pair="[CLS] $A [SEP] $B:1 [SEP]:1",
        special_tokens=[("[CLS]", cls_id), ("[SEP]", sep_id)],
    )
    fast = PreTrainedTokenizerFast(
        tokenizer_object=tokenizer,
        unk_token="[UNK]",
        pad_token="[PAD]",
        cls_token="[CLS]",
        sep_token="[SEP]",
        mask_token="[MASK]",
    )
    fast.save_pretrained(directory)
    import torch

    torch.manual_seed(seed)
    config = BertConfig(
        vocab_size=fast.vocab_size,
        hidden_size=32,
        num_hidden_layers=2,
        num_attention_heads=2,
        intermediate_size=64,
        max_position_embeddings=256,
    )
    AutoModel.from_config(config).save_pretrained(directory)
    return directory
