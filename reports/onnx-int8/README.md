# ONNX FP32 and INT8 against PyTorch: the trained DeBERTa (dev)

The exported runtimes were checked on the run-3 DeBERTa candidate
(`deberta-3-base-bio_weightingsqrt-learning_rate5e-05-seed2`). The checks are:
- **The declared gate** in [`docs/targets.md`](../../docs/targets.md): typed-condition F1 on the
  hand-labelled dev documents may drop by at most 1.0 point against PyTorch.
- **Agreement on dev:** typed F1 against the 172 model-drafted dev records.
- **Identity:** whether each document keeps exactly the same conditions as PyTorch.

Until now this had only been measured on pretrained backbones with untrained heads, where
INT8 predictions mean nothing.

The PyTorch predictions are the committed ones (run 3 for the pilot, batch-03 and batch-06;
CPU for batch-07). Both ONNX runtimes ran on CPU with 2 threads, using
`triggermap export onnx` (dynamic INT8 quantization from ONNX Runtime). Dev only: nothing was
tuned, and the test split was not touched. Reproduce with
`bash scripts/experiments/onnx_int8_parity.sh BUNDLE_DIR [WORK_DIR]`.

## Result: FP32 is exact, INT8 fails the gate

| Runtime | Documents | Identical to PyTorch | Conditions (PyTorch → runtime) | Conditions shared |
|---|---:|---:|---:|---:|
| ONNX FP32 | 372 | 372 | 1,824 → 1,824 | 1,824 |
| ONNX INT8 | 372 | 51 | 1,824 → 810 | 244 |

| Typed-condition F1 | PyTorch | ONNX INT8 | INT8 − PyTorch (95% paired CI) | Verdict |
|---|---:|---:|---:|---|
| Hand-labelled dev, 10 documents, 17 conditions (**declared gate**) | 0.346 | 0.326 | −0.021 [−0.135, +0.079] | **fails**: drop of 2.1 points > 1.0 |
| Agreement with 172 model-drafted dev records | 0.185 | 0.111 | −0.074 [−0.121, −0.039] | clearly worse |

On the 172 agreement records INT8 also has a lower false-prerequisite rate (0.370 against
0.490, clearly lower). It gets there only by predicting fewer than half as many conditions.
Its typed agreement (0.111) falls below the CRF's (0.145 on the same records).

FP32 ONNX gives the same scores as PyTorch on every check (difference +0.000), as it did on
the untrained backbones.

Full tables: [`fp32_gate_manual.md`](fp32_gate_manual.md),
[`int8_gate_manual.md`](int8_gate_manual.md), [`fp32_agreement.md`](fp32_agreement.md),
[`int8_agreement.md`](int8_agreement.md), [`identity.md`](identity.md).

## Reading

- **Dynamic INT8 breaks this DeBERTa.** Only 51 of 372 documents keep their conditions, and
  13% of PyTorch's conditions survive (244 of 1,824). That fits the earlier backbone check:
  INT8 moved DeBERTa's logits far more than DistilBERT's (max difference 1.54 against 0.36).
  The span tagger's decisions sit close to their thresholds, so quantization noise flips them.
- **The 2.1-point gate failure on 10 documents understates the damage.** One condition moves
  typed F1 by several points there, so that slice can barely resolve a 1-point gate. The
  agreement slice and the identity check show the real size of the change.
- **If DeBERTa is ever served, it would run as PyTorch or FP32 ONNX, not INT8.** FP32 ONNX
  is exact, and ONNX Runtime needs no PyTorch in the image. Making INT8 usable would need a
  different method (for example, leaving the attention and embedding layers unquantized, or
  quantization-aware training). Any such variant has to pass the same gate on dev.
- The CRF stays the default model ([`../calibration/`](../calibration/README.md),
  [`../batch-07-comparison/`](../batch-07-comparison/README.md)), so this does not change the
  current release.

The ONNX latency figures in [`docs/benchmarks.md`](../../docs/benchmarks.md) come from the
pretrained backbones on a Mac. INT8 latency matters only for a variant that passes the gate.
