import os
import random
import logging
import torch
import numpy as np
from seqeval.metrics import precision_score, recall_score, f1_score
from transformers import BertConfig, DistilBertConfig, AlbertConfig
from transformers import BertTokenizer, DistilBertTokenizer, AlbertTokenizer
# 导入自己写的
from model import ClsBERT


MODEL_CLASSES = {
    'albert': (AlbertConfig, ClsBERT, BertTokenizer),
    'bert': (BertConfig, ClsBERT, BertTokenizer),
}

# 预训练模型路径
MODEL_PATH_MAP = {
    'albert': 'resources/albert_base_zh',
    'bert': 'resources/uncased_L-2_H-128_A-2',
}


# 后面标签就分别通过简单的读取函数就可以读取出来了
def get_intent_labels(args):
    return [label.strip() for label in open(os.path.join(args.data_dir, args.task, args.intent_label_file), 'r', encoding='utf-8')]


def load_tokenizer(args):
    return MODEL_CLASSES[args.model_type][2].from_pretrained(args.model_name_or_path)


def init_logger():
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s -   %(message)s',
                        datefmt='%m/%d/%Y %H:%M:%S',
                        level=logging.INFO)


def set_seed(args):
    random.seed(args.seed)
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)
    if not args.no_cuda and torch.cuda.is_available():
        torch.cuda.manual_seed_all(args.seed)


# 计算评价指标
def compute_metrics(intent_preds, intent_labels):
    """
    计算metrics
    """
    assert len(intent_preds) == len(intent_labels)
    results = {}
    intent_result = get_intent_acc(intent_preds, intent_labels)

    results.update(intent_result)

    return results


def get_intent_acc(preds, labels):
    acc = (preds == labels).mean()
    return {
        "intent_acc": acc
    }


def read_prediction_text(args):
    return [text.strip() for text in open(os.path.join(args.pred_dir, args.pred_input_file), 'r', encoding='utf-8')]
