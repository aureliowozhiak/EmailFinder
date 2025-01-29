# Email Finder

A Python tool to find and extract email addresses from text files or strings.

## Features

- Extract email addresses from text files
- Validate email formats
- Support for multiple email patterns
- Easy to use and integrate

## Installation

```bash
git clone https://github.com/aureliowozhiak/emailfinder.git
cd emailfinder
```

## Usage

### Command Line Usage

```bash
# Basic usage with search queries
python app.py --queries "company name" "another search term"

# Specify search engine (google or duckduckgo)
python app.py --queries "company name" --engine duckduckgo
```

### Python API Usage

```python
from emailfinder import EmailFinder

# Create an instance
finder = EmailFinder()

# Find emails in a string
text = "Contact us at: support@example.com or sales@company.co.uk"
emails = finder.find_emails(text)
print(emails)  # ['support@example.com', 'sales@company.co.uk']

# Find emails in a file
emails_from_file = finder.find_emails_in_file("path/to/your/file.txt")
```

### Options

You can customize the email search by:
- Excluding specific domains
- Setting minimum/maximum length requirements
- Adding custom validation rules

```python
# Example with options
finder = EmailFinder(
    exclude_domains=['temp.com', 'spam.com'],
    min_length=5,
    max_length=50
)
```

## Examples

### Finding emails in text

```python
text = """
Multiple email examples:
john.doe@example.com
contact@company.co.uk
support-team@service.org
"""

finder = EmailFinder()
found_emails = finder.find_emails(text)
```

### Processing a file

```python
# Read emails from a file
finder = EmailFinder()
emails = finder.find_emails_in_file("contacts.txt")
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

If you have any questions or suggestions, please open an issue in the repository.
