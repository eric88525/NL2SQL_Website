import numpy as np
import torch
import torch.nn as nn
from transformers import AutoConfig, AutoModel


class M1Model(nn.Module):
    """The model that can classify columns and SQL command operator.

    Attributes:
        cond_conn_op_decoder: the classification layer of condition connect operator.
            Ouput size is (batch_size, 3), represent  ['', 'AND', 'OR']

        agg_deocder: the classification layer of the function apply on column.
            Ouput size is (batch_size, column_counts, 7)
            SQL syntax: agg (column_name)
            agg is in ['', 'AVG', 'MAX', 'MIN', 'COUNT', 'SUM', 'not select this column']

        cond_op_decoder: the classification layer of the column operator.
            Output size is (batch_size, column_count, 5)
            SQL syntax: column_name operator value
            For example: weight > 50
            operator is in ['>', '<', '=', '!=', '']
    """

    def __init__(self, pretrained_model_name):
        super(M1Model, self).__init__()

        config = AutoConfig.from_pretrained(pretrained_model_name)

        self.bert_model = AutoModel.from_pretrained(
            pretrained_model_name, config=config)

        self.cond_conn_op_decoder = nn.Sequential(
            nn.Dropout(0.5),
            nn.Linear(config.hidden_size, config.hidden_size),
            nn.ReLU(),
            nn.Linear(config.hidden_size, 3)
        )
        self.agg_deocder = nn.Sequential(
            nn.Dropout(0.5),
            nn.Linear(config.hidden_size, config.hidden_size),
            nn.ReLU(),
            nn.Linear(config.hidden_size, 7)
        )
        self.cond_op_decoder = nn.Sequential(
            nn.Dropout(0.5),
            nn.Linear(config.hidden_size, config.hidden_size),
            nn.ReLU(),
            nn.Linear(config.hidden_size, 5)
        )

    def forward(self, input_ids, attention_mask, token_type_ids, header_idx, **kwargs):
        """Forward pass.

        Args:
            input_ids (torch.tensor): bert model input
            attention_mask (torch.tensor)):  bert model input
            token_type_ids (torch.tensor):  bert model input
            header_idx (torch.tensor)): the index of header in input_ids

        Returns:
            A tuple of 3 tensors, each tensor is the output of the corresponding decoder.
        """
        hiddens, cls = self.bert_model(
            input_ids=input_ids, attention_mask=attention_mask, token_type_ids=token_type_ids, return_dict=False)

        # shape = (batch_size, 3)
        cond_conn_op = self.cond_conn_op_decoder(cls)

        # header_hiddens shape = (batch_size, columns_count, hidden_dim)
        header_hiddens = hiddens[header_idx == 1]

        # agg shape = (batch_size, columns_count, 7)
        agg = self.agg_deocder(header_hiddens)

        # cond_op shape = (batch_size, columns_count, 5)
        cond_op = self.cond_op_decoder(header_hiddens)

        return cond_conn_op, cond_op, agg
