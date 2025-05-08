def load_categories(file_path):
    """Load categories from the file."""
    categories = []
    try:
        with open(file_path, "r") as file:
            for line in file:
                line = line.strip()
                # Skip empty lines and URLs
                if line and not line.startswith(("http://", "https://")):
                    categories.append(line)
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
    except Exception as e:
        print(f"Error loading categories: {e}")
    return categories


def load_urls_by_category(file_path, selected_category):
    """Load product URLs for a selected category."""
    urls = []
    try:
        with open(file_path, "r") as file:
            recording = False
            for line in file:
                line = line.strip()
                if not line:
                    continue  # Skip empty lines
                
                # Start recording URLs when the selected category is found
                if line == selected_category:
                    recording = True
                    continue
                
                # Stop recording if a new category is encountered
                if recording and not line.startswith(("http://", "https://")):
                    break
                
                # Record URLs
                if recording and line.startswith(("http://", "https://")):
                    urls.append(line)
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
    except Exception as e:
        print(f"Error loading URLs for category {selected_category}: {e}")
    return urls