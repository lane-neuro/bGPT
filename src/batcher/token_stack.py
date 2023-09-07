import torch


class token_stack:
    # role: stacks tokens
    # takes a list of length N 1-D tensors with integers of length M
    # sticks them together into an NxM pytorch tensor
    # returns for training

    # [[],[],[]]: tokens = torch.tensor(tokens, new_token)

    # definitions
    tokens: torch.tensor = []

    def __init__(self, first_token):
        self.__add__(first_token)
        return

    def __add__(self, other):
        self.tokens = torch.as_tensor([self.tokens, other])
        return

