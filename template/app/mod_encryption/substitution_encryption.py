import os
import random


class SubstitutionEncryption():
    """SubstitutionEncryption is a two way Encryption method that implements a
     dictionary as a lookup value per column/domain and then the unique value which will
     be used as the substitution value.
    If key-value not provided it will be dynamically generated at time of lookup value


    :param current_key: is the current Key for `substitution_lookup` you wish to look up against.
                        In use this will be the current column or domain you wish to lookup against.
    :param substitution_lookup: allows for different text encodings to be used.
    :param words_file_path: is the file path for the dictionary of words / words list to randomize against in
                            the `update_substitution_lookup` function.
    :param update_substitution_loopup_kwags: this allows you to specify a dictionary of keyword arguments
                                            to pass to the `update_substitution_lookup` function as called!
    """

    def __init__(
        self,
        current_key: str,
        substitution_lookup: dict,
        words_file_path: str = os.path.join(os.path.dirname(__file__), "words.txt"),
        update_substitution_loopup_kwags: dict = {
            "max_word_len": None,
            "min_word_len": None,
            "number_of_shuffles": 2,
        },
    ) -> None:
        super().__init__()
        self.current_key = current_key
        self.substitution_lookup = substitution_lookup
        self.words = self.read_words(words_file_path)
        self.update_substitution_loopup_kwags = update_substitution_loopup_kwags

    def encrypt(self, message: str) -> str:
        """Change provided message into a secret code (system of letters, numbers, and/or symbols) that people
           cannot understand

        Args:
            message (_type_): a string that we wish to encode/encrypt so that people cannot understand it

        Returns:
            str: An encoded secret code (system of letters, numbers, and/or symbols) that people cannot understand
        """

        encrypted_message = self.substitution_lookup[self.current_key].get(
            message,
        )
        if (
            encrypted_message
            is None  # Get with default ran the function even if value exists
        ):
            encrypted_message = self.update_substitution_lookup(
                message, **self.update_substitution_loopup_kwags
            )

        return encrypted_message

    def decrypt(self, encoded_message: str) -> str:
        """make (a coded or unclear message) intelligible.

        Args:
            message (str): an encoded string that we wish to decode/decrypt so that people can understand it

        Returns:
            str: An decoded message code (string) that people can understand again
        """

        reversed_substitution_lookup = dict(
            [
                (value, key)
                for key, value in self.substitution_lookup[self.current_key].items()
            ]
        )

        decoded_data = reversed_substitution_lookup[encoded_message]

        return decoded_data

    def update_substitution_lookup(
        self,
        message: str,
        min_word_len: int = None,
        max_word_len: int = None,
        number_of_shuffles: int = 1,
    ):
        """This function will update the `substitution_lookup` for the given message with a word from the self.words
            generated from `words.txt` by default. This will check if the value already exists for another key/message
            and will try generate another word if it already exists!

        Args:
            min_word_len (int, optional): What is the minimum length of a word you want to generate. Defaults to None.
            max_word_len (int, optional): What is the maximum length of a word you want to generate. Defaults to None.
            number_of_shuffles (int, optional): How many times do you want to shuffle the array before creating a
                                chosen variable. Defaults to 1.
        """
        if min_word_len > max_word_len:
            raise Exception("`min_word_len` cannot be greater than `max_word_len`")

        number_of_shuffles = abs(number_of_shuffles)
        if number_of_shuffles <= 0:
            number_of_shuffles = 1

        new_words_list = []
        final_words_list = []
        if min_word_len:
            for word in self.words:
                if (len(word)) >= min_word_len:
                    new_words_list.append(word)
        else:
            new_words_list = self.words

        if max_word_len:
            for word in new_words_list:
                if (len(word)) <= max_word_len:
                    final_words_list.append(word)
        else:
            final_words_list = new_words_list

        unique_word_in_list = False
        chosen_word = None 
        while not unique_word_in_list and chosen_word is not None:
            if chosen_word in self.substitution_lookup[self.current_key].items():
                for i in range(0, number_of_shuffles):
                    random.shuffle(final_words_list)
                chosen_word = final_words_list[0].strip()
            else:
                unique_word_in_list = True

        self.substitution_lookup[self.current_key][message] = chosen_word

        return chosen_word

    def read_words(file_name: str) -> list:
        words_list = []
        with open(file_name) as f:
            words_list = f.readlines()

        words_list = [word.strip().lower() for word in words_list]

        return words_list
