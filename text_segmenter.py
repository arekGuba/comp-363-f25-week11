import random

little_dictionary = [
    "a",
    "afternoon",
    "airport",
    "an",
    "and",
    "anywhere",
    "at",
    "because",
    "become",
    "before",
    "behind",
    "beside",
    "between",
    "breakfast",
    "broadcast",
    "but",
    "daylight",
    "deadline",
    "everywhere",
    "for",
    "forecast",
    "handbook",
    "hardware",
    "he",
    "headline",
    "her",
    "him",
    "homework",
    "i",
    "in",
    "income",
    "inside",
    "into",
    "it",
    "keyboard",
    "me",
    "midnight",
    "network",
    "notebook",
    "of",
    "offline",
    "on",
    "online",
    "or",
    "outcome",
    "outline",
    "outside",
    "overcome",
    "oversee",
    "password",
    "saturn",
    "she",
    "software",
    "somewhere",
    "suitcase",
    "sunlight",
    "takeover",
    "textbook",
    "the",
    "them",
    "therefore",
    "they",
    "to",
    "understand",
    "undertake",
    "upon",
    "us",
    "we",
    "whatever",
    "whenever",
    "wherever",
    "whoever",
    "within",
    "without",
    "you",
]


def can_segment(A:str) -> bool:
    n =len(A)
    if n == 0:
        return True
    for i in range(n):
        if is_word(A[:i]):
            if can_segment(A[i:]):
                return True
    return False

def binary_search(word_list: list[str], target: str) -> int:
    """Performs binary search on a sorted list of words.
    Returns the index of target if found, otherwise -1.
    To preserve memory, this implementation is iterative."""
    low: int = 0
    high: int = len(word_list) - 1

    while low <= high:
        mid: int = (low + high) // 2
        guess: str = word_list[mid]

        if guess == target:
            return mid  # Target found
        if guess > target:
            high = mid - 1  # Search in the lower half
        else:
            low = mid + 1  # Search in the upper half

    return -1  # Target not found


def is_word(word_list: list[str], word: str) -> bool:
    """Boolean helper for binary searchReturns True if word is in 
    word_list, False otherwise."""
    return binary_search(word_list, word) != -1

def generate_random_string(
        from_words: list[str],
        number_of_words: int,
        distortion_probability: float = 0.0) -> str:
    """Produce a string with randomly selected strings from a list of strings. Then,
    distort the string by removing characters from it with the given probability."""
    # Select words at random from the input list. The number of words to select
    # is specified by the int:number_of_words in the arguments.
    random_string: str = ""
    # Guard statement
    if (distortion_probability >= 0.0
        and number_of_words > 0
            and number_of_words <= len(from_words)):
        random_string = "".join(random.sample(from_words, 6))
        # Distort the string only if the distortion probability is not zero.
        if distortion_probability > 0.0:
            distorted_chars = [
                ch for ch in random_string
                if random.random() >= distortion_probability
            ]
            random_string = "".join(distorted_chars)
    return random_string

"""def can_segment(A: str) -> bool:
    Determine if a string can be segmented into valid tokens.
    The computation is done recursively
    n = len(A)  # shortcut
    if n == 0:
        # Base case: an empty string can be segmented into 0 words
        return True
    for i in range(n):
        # Check if the first i characters of the string are a valid token
        if is_word(little_dictionary, A[:i+1]):
            # Can the rest of the string be segmented
            if can_segment(A[i+1:]):
                return True
    return False
"""


def can_segment_dp(A: str):
    # Determine (using dynamic programming) if A can be segmented into
    # valid tokens from little_dictionary.
    # Shortcut
    n: int = len(A)
    # Initialize the dp array
    dp: list[bool] = [False] * (n + 1)
    # Base case
    dp[0] = True

    # Consider every prefix A[:i] for i in 1..n
    for i in range(1, n + 1):
        j = 0
        # we continue until we either find a valid split or exhaust j
        while j < i and not dp[i]:
            if dp[j] and is_word(little_dictionary, A[j:i]):
                dp[i] = True
            j += 1

    return dp[n], dp

def segment_string(A: str, dp):
    """
    Segment a given string starting from the back.

    If a string IS segmentable according to can_segment_dp, starting from the back, 
    loop backwards, finding words and adding spaces according to dp segment array.
    """

    words = []
    n = len(A)

    if not dp[n]:
        return "Not segmentable."
    
    # convert dp array to a string, to let us use rfind for fast traversal
    dp_str = "".join(["1" if x else "0" for x in dp])

    i = n

    while i > 0:
        # j is the next possible segmentable position
        j = dp_str.rfind("1", 0, i)
        if is_word(little_dictionary, A[j:i]):
            # if A[j:i] is a valid word itself, append to words and move i
            words.append(A[j:i])
            i = j
        else: 
            # if A[j:i] isn't valid by itself, mark this position as unsegmentable in
            # and move on
            dp_str = dp_str[:j] + '0' + dp_str[j+1:]

    words.reverse()
    return words
    
# test
number_of_trials = 3
current_trial = 0
distortion_probability = 0.01
while current_trial < number_of_trials:
    current_trial += 1
    A = generate_random_string(
        little_dictionary, number_of_trials, distortion_probability)
    result, dp = can_segment_dp(A)
    # report
    print(f"{str(result):>8}: {A}")
    print(f"          {segment_string(A, dp)}")

