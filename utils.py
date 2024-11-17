import unicodedata
import string

def remove_sign(word):
    BANG_XOA_DAU = str.maketrans(
        "ÁÀẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬĐÈÉẺẼẸÊẾỀỂỄỆÍÌỈĨỊÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÚÙỦŨỤƯỨỪỬỮỰÝỲỶỸỴáàảãạăắằẳẵặâấầẩẫậđèéẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵ",
        "A"*17 + "D" + "E"*11 + "I"*5 + "O"*17 + "U"*11 + "Y"*5 + "a"*17 + "d" + "e"*11 + "i"*5 + "o"*17 + "u"*11 + "y"*5
    )
    if not unicodedata.is_normalized("NFC", word):
        word = unicodedata.normalize("NFC", word)
    return word.translate(BANG_XOA_DAU)

def remove_space(word):
    return word.replace(" ", "")

def upper(word):
    return word.upper()

def reverse(word):
    return word[::-1]

def pre_process(word):
    word = remove_sign(word)
    word = remove_space(word)
    word = upper(word)
    word = reverse(word)

    return word

def search(word, trie):
    #word = pre_process(word)
    return trie.search(word)

def insert_char(word):
    all_ascii_characters = string.printable.upper()
    #char = random.choice(all_ascii_characters)
    #position = random.choice(list(range(len(word) + 1)))
    word_lst = []
    for char1 in all_ascii_characters:
        for position1 in range(len(word) + 1):
            new_word = word[:position1] + char1 + word[position1:]
            word_lst.append(new_word)
            # for char2 in all_ascii_characters:
            #     for position2 in range(len(new_word) + 1):
            #         new_word2 = new_word[:position2] + char2 + new_word[position2:]
            #         word_lst.append(new_word2)
    return list(set(word_lst))

def _remove_char(word):
    if len(word) == 0:
        return []
    word_lst = []
    for position in range(len(word)):
        if position == len(word) - 1:
            new_word = word[:-1]
        else:
            new_word = word[:position] + word[position + 1:]
        word_lst.append(new_word)

    return list(set(word_lst))

def remove_char(word):
    lst = [word]
    lst1 = []
    lst2 = []
    lst3 = []


    lst1 += _remove_char(word)
    for word1 in lst1:
        lst2 += _remove_char(word1)
    for word2 in lst2:
        lst3 += _remove_char(word2)

    return list(set(lst + lst1))
    return list(set(lst + lst1 + lst2 + lst3))

def _change_char(word):
    word_lst = []
    all_ascii_characters = string.printable.upper()
    for char in all_ascii_characters:
        for position in range(len(word) + 1):
            new_word = word[:position] + char + word[position + 1:]
            word_lst.append(new_word)
    return list(set(word_lst))


def change_char(word):
    lst = [word]
    lst1 = []
    lst2 = []
    lst1 += _change_char(word)
    for word1 in lst1:
        lst2 += _change_char(word1)

    return list(set(lst + lst1))
    return list(set(lst + lst1 + lst2))


def levenshtein_distance(str1, str2):
    # Tạo bảng động (Dynamic Programming table)
    m, n = len(str1), len(str2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Khởi tạo giá trị cho bảng
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    # Điền bảng động
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if str1[i - 1] == str2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]  # Nếu ký tự giống nhau
            else:
                dp[i][j] = min(dp[i - 1][j] + 1,  # Xóa
                               dp[i][j - 1] + 1,  # Chèn
                               dp[i - 1][j - 1] + 1)  # Thay thế

    return dp[m][n]