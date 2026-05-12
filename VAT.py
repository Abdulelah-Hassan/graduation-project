import re

def findVAT(text):

    pattern = r'\b\d{15}\b'
    serial_numbers = re.findall(pattern, text)
    return serial_numbers if serial_numbers else ["No"]

# Example usage:
if __name__ == "__main__":
    sample_text = "geagre aiouh 123567890312345"
    found_serials = findVAT(sample_text)
    print("Found serial numbers:", found_serials if found_serials else "Nothing")