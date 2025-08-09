import numpy as np
import pandas as pd

def levenshtein(a, b):
    """
    Compute Levenshtein (edit) distance between two sequences (string or list of tokens).
    """
    len_a, len_b = len(a), len(b)
    dp = np.zeros((len_a + 1, len_b + 1), dtype=int)

    for i in range(len_a + 1):
        dp[i][0] = i
    for j in range(len_b + 1):
        dp[0][j] = j

    for i in range(1, len_a + 1):
        for j in range(1, len_b + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,        # deletion
                dp[i][j - 1] + 1,        # insertion
                dp[i - 1][j - 1] + cost  # substitution
            )

    return dp[len_a][len_b]

def compute_metrics(clean_texts, references):
    """
    Compute CER (Character Error Rate) and WER (Word Error Rate) for multiple pages.

    Returns:
        per_page_df (pd.DataFrame)
        overall_metrics (dict)
    """
    per_page_data = []
    total_chars_ref = 0
    total_char_err = 0
    total_words_ref = 0
    total_word_err = 0

    for idx, (hyp, ref) in enumerate(zip(clean_texts, references), start=1):
        # --- CER ---
        char_err = levenshtein(hyp, ref)
        char_ref_len = max(len(ref), 1)
        cer = char_err / char_ref_len
        char_acc = 1 - cer

        # --- WER ---
        hyp_words = hyp.split()
        ref_words = ref.split()
        word_err = levenshtein(hyp_words, ref_words)
        word_ref_len = max(len(ref_words), 1)
        wer = word_err / word_ref_len
        word_acc = 1 - wer

        per_page_data.append({
            "Page": idx,
            "CER": cer,
            "Char Accuracy (%)": round(char_acc * 100, 2),
            "WER": wer,
            "Word Accuracy (%)": round(word_acc * 100, 2)
        })

        total_chars_ref += char_ref_len
        total_char_err += char_err
        total_words_ref += word_ref_len
        total_word_err += word_err

    # Overall metrics
    overall_cer = total_char_err / total_chars_ref if total_chars_ref else 0
    overall_wer = total_word_err / total_words_ref if total_words_ref else 0
    overall_metrics = {
        "CER": overall_cer,
        "Char Accuracy (%)": round((1 - overall_cer) * 100, 2),
        "WER": overall_wer,
        "Word Accuracy (%)": round((1 - overall_wer) * 100, 2)
    }

    per_page_df = pd.DataFrame(per_page_data)

    return per_page_df, overall_metrics
