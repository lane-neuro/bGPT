import math

class scanner:

    def __init__(self,
                 nscanner: int,
                 batch_size: int,
                 n_bodyparts: int,
                 nrows_tensor: int,
                 n_chars_per_bodypart: int,
                 block_size: int, ):

        self.nscanner = nscanner  # value of 0 -> batch_size-1
        self.batch_size = batch_size
        self.nrows_tensor = nrows_tensor

        self.row_position_call_start = math.floor((self.nscanner / (self.batch_size + 1)) * self.nrows_tensor)
        self.row_position_end = math.floor(((self.nscanner + 1) / (self.batch_size + 1)) * self.nrows_tensor)

        self.char_call_position = 0
        self.char_per_row = n_bodyparts * n_chars_per_bodypart  # padding +2 or 3?

        self.nrows_call = math.ceil(block_size / (2 * self.char_per_row))  # account for tokenization?
        self.nrows_call = math.ceil(self.nrows_call*(framerate/framerate_min_aug)*(n_bodyparts-n_bodyparts_min_aug+1))

        self.row_position_call_end = self.row_position_call_start + self.nrows_call

        self.in_epoch = True

        return

    def reset(self):
        return

    def get_indices(self):
        if not self.in_epoch:
            return None
        else:
            row_incides = (self.row_position_call_start, self.row_position_call_end)
            char_index = self.char_call_position

            self.char_call_position += 1
            if self.char_call_position > self.char_per_row:
                self.char_call_position = 0
                self.row_position_call_start += 1
                self.row_position_call_end += 1

            if self.row_position_call_end > self.row_position_end:
                self.in_epoch = False
                self.row_position_call_start = math.floor((self.nscanner / (self.batch_size + 1)) * self.nrows_tensor)
                self.row_position_end = math.floor(((self.nscanner + 1) / (self.batch_size + 1)) * self.nrows_tensor)
                self.char_call_position = 0

            return row_incides, char_index
