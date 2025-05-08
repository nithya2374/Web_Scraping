# import matplotlib.pyplot as plt
# import pandas as pd
# import seaborn as sns
# import streamlit as st
# from src.product_scraper import run_scraper
# from utils.helpers import load_categories, load_urls_by_category

# # Load categories from sample_url.txt
# categories = load_categories("data/sample_url.txt")

# # Streamlit app setup
# st.set_page_config(page_title="Product Comparison Dashboard", layout="wide")

# # Sidebar for category selection
# if categories:
#     selected_category = st.sidebar.radio("Select a Category", categories)
# else:
#     st.sidebar.write("No categories available.")
#     selected_category = None

# # Main content
# if selected_category:
#     st.title(f"Product Comparison: {selected_category}")

#     # Load product URLs for the selected category
#     urls = load_urls_by_category("data/sample_url.txt", selected_category)
#     st.write(f"Scraping {len(urls)} product links...")

#     # Scrape product details using async scraper
#     product_data = run_scraper(urls)

#     # Debugging: Show raw data
#     if not product_data.empty:
#         st.write("### Debugging: Displaying Scraped Data")
#         st.write(product_data.to_html(index=False, escape=False), unsafe_allow_html=True)

#         # Select the best product based on the highest positive sentiment score
#         best_product = product_data.loc[product_data["Positive"].idxmax()]
#         best_product_df = pd.DataFrame([best_product])

#         st.write("## Sentiment Analysis Results (Top Product)")
#         st.write(best_product_df.to_html(index=False, escape=False), unsafe_allow_html=True)

#         # Convert Price & Rating to numeric
#         product_data["Price"] = pd.to_numeric(product_data["Price"], errors='coerce')
#         product_data["Rating"] = pd.to_numeric(product_data["Rating"], errors='coerce')
#         # Suggestion Table: Best product based on lowest price and highest rating
#         if not product_data.empty:
#             suggestion_data = product_data.copy()

#             # Convert Price & Rating to numeric for sorting
#             suggestion_data["Price"] = pd.to_numeric(suggestion_data["Price"], errors='coerce')
#             suggestion_data["Rating"] = pd.to_numeric(suggestion_data["Rating"], errors='coerce')

#             # Filter valid entries (drop NaN values)
#             suggestion_data = suggestion_data.dropna(subset=["Price", "Rating"])

#             # Select the single best product (lowest price & highest rating)
#             best_suggested_product = suggestion_data.sort_values(by=["Price", "Rating"], ascending=[True, False]).head(1)

#             st.write("## Suggested Product (Best Value)")
#             st.write(best_suggested_product.to_html(index=False, escape=False), unsafe_allow_html=True)

#         # Define chart filters
#         chart_filters = {
#             "Price": product_data.nsmallest(4, "Price"),
#             "Rating": product_data.nlargest(4, "Rating"),
#             "Positive": product_data.nlargest(4, "Positive")
#         }

#         # Show Charts
#         for metric, color in zip(["Price", "Rating", "Positive"], ["blue", "orange", "green"]):
#             filtered_data = chart_filters[metric]

#             if filtered_data[metric].notna().sum() > 0:
#                 st.write(f"### {metric} Comparison (Top 4)")
#                 plt.figure(figsize=(10, 5))

#                 ax = sns.barplot(x=[f"Product{i+1}" for i in range(len(filtered_data))], 
#                                 y=filtered_data[metric], color=color)

#                 # Add labels on top of bars
#                 for p in ax.patches:
#                     ax.annotate(f'{p.get_height():.2f}', 
#                                 (p.get_x() + p.get_width() / 2., p.get_height()), 
#                                 ha='center', va='bottom', fontsize=12, fontweight='bold', color='black')

#                 plt.xlabel("Products")
#                 plt.ylabel(metric)
#                 plt.xticks(rotation=00)
#                 if metric == "Rating":
#                     plt.ylim(0, 5)
#                 st.pyplot(plt)
#             else:
#                 st.write(f"{metric} data is missing or invalid.")

#     else:
#         st.write("No product data available. Please check if Amazon blocked requests.")



import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st
from src.product_scraper import run_scraper
from utils.helpers import load_categories, load_urls_by_category

# Load categories from sample_url.txt
categories = load_categories("data/sample_url.txt")

# Streamlit app setup
st.set_page_config(page_title="Product Comparison Dashboard", layout="wide")

# Sidebar for category selection
if categories:
    selected_category = st.sidebar.radio("Select a Category", categories)
else:
    st.sidebar.write("No categories available.")
    selected_category = None

# Main content
if selected_category:
    st.title(f"Product Comparison: {selected_category}")

    # Load product URLs for the selected category
    urls = load_urls_by_category("data/sample_url.txt", selected_category)
    st.write(f"Scraping {len(urls)} product links...")

    # Scrape product details using async scraper
    product_data = run_scraper(urls)

    # Debugging: Show raw data
    if not product_data.empty:
        st.write("### Debugging: Displaying Scraped Data")
        st.write(product_data.to_html(index=False, escape=False), unsafe_allow_html=True)

        # Convert Price & Rating to numeric
        product_data["Price"] = pd.to_numeric(product_data["Price"], errors='coerce')
        product_data["Rating"] = pd.to_numeric(product_data["Rating"], errors='coerce')

        # Select the best product based on the lowest price, highest rating, and highest positive sentiment
        best_product = product_data.sort_values(by=["Price", "Rating", "Positive"], ascending=[True, False, False]).iloc[0]
        best_product_df = pd.DataFrame([best_product])

        st.write("## Suggested Product (Best Value)")
        st.write(best_product_df.to_html(index=False, escape=False), unsafe_allow_html=True)

        # Select the best product based on the highest positive sentiment score
        best_product_sentiment = product_data.loc[product_data["Positive"].idxmax()]
        best_product_sentiment_df = pd.DataFrame([best_product_sentiment])

        st.write("## Sentiment Analysis Results (Top Product)")
        st.write(best_product_sentiment_df.to_html(index=False, escape=False), unsafe_allow_html=True)

        # Define chart filters
        chart_filters = {
            "Price": product_data.nsmallest(4, "Price"),
            "Rating": product_data.nlargest(4, "Rating"),
            "Positive": product_data.nlargest(4, "Positive")
        }

        # Show Charts
        for metric, color in zip(["Price", "Rating", "Positive"], ["blue", "orange", "green"]):
            filtered_data = chart_filters[metric]

            if filtered_data[metric].notna().sum() > 0:
                st.write(f"### {metric} Comparison (Top 4)")
                plt.figure(figsize=(10, 5))

                ax = sns.barplot(x=[f"Product{i+1}" for i in range(len(filtered_data))], 
                                y=filtered_data[metric], color=color)

                # Add labels on top of bars
                for p in ax.patches:
                    ax.annotate(f'{p.get_height():.2f}', 
                                (p.get_x() + p.get_width() / 2., p.get_height()), 
                                ha='center', va='bottom', fontsize=12, fontweight='bold', color='black')

                plt.xlabel("Products")
                plt.ylabel(metric)
                plt.xticks(rotation=00)
                if metric == "Rating":
                    plt.ylim(0, 5)
                st.pyplot(plt)
            else:
                st.write(f"{metric} data is missing or invalid.")
    else:
        st.write("No product data available. Please check if Amazon blocked requests.")
