# Required imports
from langchain.document_loaders import AsyncChromiumLoader
from langchain.document_transformers import BeautifulSoupTransformer
from langchain.chat_models import ChatOpenAI
from langchain.chains import create_extraction_chain
import csv

# Initialize components
loader = AsyncChromiumLoader(["https://silverstones.pk/product-category/925-silver-jewelry-for-womens/nose-pin-rings/page/2/"])
html = loader.load()
bs_transformer = BeautifulSoupTransformer()
docs_transformed = bs_transformer.transform_documents(html, tags_to_extract=["div"])

# Define schema for product extraction
schema = {
    "properties": {
        "ID": {"type": "string"},
        "Product Name": {"type": "string"},
        "Published": {"type": "string"},
        "Is featured?": {"type": "string"},
        "Visibility in catalog": {"type": "string"},
        "Short description": {"type": "string"},
        "Description": {"type": "string"},
        "Date sale price starts": {"type": "string"},
        "Date sale price ends": {"type": "string"},
        "Tax status": {"type": "string"},
        "Tax class": {"type": "string"},
        "In stock?": {"type": "string"},
        "Stock": {"type": "string"},
        "Low stock amount": {"type": "string"},
        "Backorders allowed?": {"type": "string"},
        "Sold individually?": {"type": "string"},
        "Weight (kg)": {"type": "string"},
        "Length (cm)": {"type": "string"},
        "Width (cm)": {"type": "string"},
        "Height (cm)": {"type": "string"},
        "Allow customer reviews?": {"type": "string"},
        "Purchase note": {"type": "string"},
        "Sale price": {"type": "string"},
        "Regular price": {"type": "string"},
        "Categories": {"type": "string"},
        "Tags": {"type": "string"},
        "Shipping class": {"type": "string"},
        "Images": {"type": "string"},
        "Download limit": {"type": "string"},
        "Download expiry days": {"type": "string"},
        "Parent": {"type": "string"},
        "Grouped products": {"type": "string"},
        "Upsells": {"type": "string"},
        "Cross-sells": {"type": "string"},
        "External URL": {"type": "string"},
        "Button text": {"type": "string"},
        "Position": {"type": "string"},
        "Attribute 1 name": {"type": "string"},
        "Attribute 1 value(s)": {"type": "string"},
        "Attribute 1 visible": {"type": "string"},
        "Attribute 1 global": {"type": "string"},
        "Name": {"type": "string"},
        "Price": {"type": "string"},
        "Inventory_Info": {"type": "string"},
        "Image_URL": {"type": "string"},
        "SKU": {"type": "string"},
        "Additional_Info": {"type": "string"},
        "Category": {"type": "string"},
        "Special_Detail": {"type": "string"},
        "URL": {"type": "string"},
    },
    "required": [
    "ID",
     "Product Name",
    "Published",
    "Is featured?",
    "Visibility in catalog",
    "Short description",
    "Description",
    "Date sale price starts",
    "Date sale price ends",
    "Tax status",
    "Tax class",
    "In stock?",
    "Stock",
    "Low stock amount",
    "Backorders allowed?",
    "Sold individually?",
    "Weight (kg)",
    "Length (cm)",
    "Width (cm)",
    "Height (cm)",
    "Allow customer reviews?",
    "Purchase note",
    "Sale price",
    "Regular price",
    "Categories",
    "Tags",
    "Shipping class",
    "Images",
    "Download limit",
    "Download expiry days",
    "Parent",
    "Grouped products",
    "Upsells",
    "Cross-sells",
    "External URL",
    "Button text",
    "Position",
    "Attribute 1 name",
    "Attribute 1 value(s)",
    "Attribute 1 visible",
    "Attribute 1 global",
    "Name",
    "Price",
    "Inventory_Info",
    "Image_URL",
    "SKU",
    "Additional_Info",
    "Category",
    "Special_Detail",
    "URL"
]
}

# Use LLM for extraction
# Use LLM for extraction
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-16k", openai_api_key="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")



def extract(content: str, schema: dict):
    return create_extraction_chain(schema=schema, llm=llm).run(content)

# Extract product details
extracted_products = extract(content=docs_transformed[0].page_content, schema=schema)

# Write to CSV
csv_file = "new.csv"
csv_columns = list(schema["properties"].keys())  # get keys from the schema

try:
    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in extracted_products:
            writer.writerow(data)
    print(f"Data saved to {csv_file}")
except IOError:
    print("I/O error")