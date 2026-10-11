
from parser import parse_resume

file_path = input("Enter the full path to a PDF or DOCX resume: ").strip().strip('"')

try:
    text = parse_resume(file_path)
    print("\n✅ Resume parsed successfully!")
    print("\nExtracted text preview:\n")
    print(text[:1000])
    print(f"\nTotal characters extracted: {len(text)}")

except Exception as error:
    print(f"\n❌ Error: {error}")