import os
import re

def extract_emails(text):
    # Pattern for valid email addresses
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return re.findall(email_pattern, text)

def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
            return extract_emails(content)
    except Exception as e:
        print(f"Error processing {filepath}: {str(e)}")
        return []

def filter_emails(emails, valid_emails = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'icloud.com', 'protonmail.com']):
    return [email for email in emails if any(domain in email for domain in valid_emails)]

def process_and_filter_emails():
    """Main function to process files and extract emails"""
    # Get current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Path to arquivos folder
    arquivos_dir = os.path.join(current_dir, 'arquivos')
    
    # Output file path
    output_file = os.path.join(current_dir, 'emails.txt')
    
    # Store all unique emails
    all_emails = set()

    valid_emails = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'icloud.com', 'protonmail.com']
    
    # Process each file in arquivos directory
    for filename in os.listdir(arquivos_dir):
        filepath = os.path.join(arquivos_dir, filename)
        if os.path.isfile(filepath):
            emails = process_file(filepath)
            emails = filter_emails(emails, valid_emails)
            all_emails.update(emails)
    
    # Write unique emails to output file
    with open(output_file, 'w', encoding='utf-8') as f:
        for email in sorted(all_emails):
            f.write(email + '\n')
    
    return len(all_emails)

def main():
    process_and_filter_emails()

if __name__ == "__main__":
    main()
