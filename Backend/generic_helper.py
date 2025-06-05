# import re
#
# def get_str_from_food_dict(food_dict: dict):
#     result = ", ".join([f"{int(value)} {key}" for key, value in food_dict.items()])
#     return result
#
#
# def extract_session_id(session_str: str):
#     match = re.search(r"/sessions/(.*?)/contexts/", session_str)
#     if match:
#         extracted_string = match.group(1)
#         return extracted_string
#
#     return ""
#
# if __name__ == "__main__":
#     print(get_str_from_food_dict({"samosa":2,"mango lassi":1}))

import re


def get_str_from_food_dict(food_dict: dict) -> str:
    """
    Converts a dictionary of food items and their quantities into a readable string.
    Example: {"samosa": 2, "mango lassi": 1} -> "2 samosa, 1 mango lassi"
    """
    return ", ".join([f"{int(value)} {key}" for key, value in food_dict.items()])


def extract_session_id(session_str: str) -> str:
    """
    Extracts the session ID from a Dialogflow context session path.
    Example input: "projects/project-id/agent/sessions/abc123/contexts/ongoing-order"
    Returns: "abc123"
    """
    match = re.search(r"/sessions/(.*?)/contexts/", session_str)
    if match:
        return match.group(1)
    return ""


# For standalone test run
if __name__ == "__main__":
    # Test get_str_from_food_dict
    print(get_str_from_food_dict({"samosa": 2, "mango lassi": 1}))

    # Test extract_session_id
    test_session_path = "projects/myproject/agent/sessions/test123/contexts/ongoing-order"
    print(extract_session_id(test_session_path))  # Should print: test123
