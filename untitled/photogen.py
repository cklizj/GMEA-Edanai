import requests
import webbrowser
import pandas as pd
import itertools

def read_excel_file(file_path):
    """Read an Excel file and return the first sheet as a DataFrame."""
    return pd.read_excel(file_path, engine='openpyxl')

def get_all_elements(data_frame):
    """Flatten the DataFrame and return all values as a list."""
    return data_frame.values.flatten().tolist()
    # Read the Excel files
    
def download_and_save_image(url, file_name):
    """Download and save an image from a URL to a file."""
    response = requests.get(url)

    if response.status_code == 200:
        with open(file_name, 'wb') as file:
            file.write(response.content)
    else:
        print(f"Failed to download image: {url}. Status code: {response.status_code}")
def main():
    
    url = "https://api.edenai.run/v2/image/generation"
    file_path1 = "location.xlsx"
    file_path2 = "character.xlsx"
    df1 = read_excel_file(file_path1)
    df2 = read_excel_file(file_path2)

    # Get all elements from each file
    elements1 = get_all_elements(df1)
    elements2 = get_all_elements(df2)

    # Generate all combinations of the elements
    combinations = list(itertools.product(elements1, elements2))

    # Print the combinations
    for combination in combinations:
        prompt=''
        for i in combination:
            prompt += i
            
        payload = {
            "response_as_dict": True,
            "attributes_as_list": True,
            "show_original_response": True,
            "resolution": "1024x1024",
            "num_images": 1,
            "text": "123",
            "providers": "openai"
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMzYzNWMxMzktMWRhMi00YTAzLTgwZmYtNDQ4ZWJlOTY3ZWY4IiwidHlwZSI6ImZyb250X2FwaV90b2tlbiJ9.BJucGZtBzIqFEI4GeA9L6MDAQK8Q2dsFiWSunv18SQw"
        }

        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            response_json = response.json()
            openai_data = response_json.get("openai")
            
            if openai_data:
                image_resource_url_list = openai_data.get("image_resource_url")
                
                if image_resource_url_list:
                    image_url = image_resource_url_list[0]
                    print(f"Image URL: {image_url}")

                    # Download and save the image
                    file_name = prompt+"downloaded_image.png"
                    download_and_save_image(image_url, file_name)
                    print(f"Image saved as {file_name}")
                else:
                    print("The 'image_resource_url' key is missing in the 'openai' object.")
            else:
                print("The 'openai' key is missing in the response JSON.")
        else:
            print(f"Failed to fetch image URL. Status code: {response.status_code}")
if __name__ == "__main__":
    main()
