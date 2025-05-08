# import matplotlib.pyplot as plt
# import pandas as pd
# import streamlit as st

# def generate_comparison_graphs(product_data):
#     # Clean column names and validate data
#     product_data.columns = product_data.columns.str.strip()
#     required_columns = {"Name", "Price", "Rating", "URL"}
    
#     if not required_columns.issubset(product_data.columns):
#         st.error("Dataset is missing required columns.")
#         return

#     # Clean data
#     product_data = product_data.dropna(subset=["Price", "Rating"]).copy()
#     product_data["Price"] = pd.to_numeric(product_data["Price"], errors="coerce")
#     product_data["Rating"] = pd.to_numeric(product_data["Rating"], errors="coerce")
#     product_data = product_data.dropna()
    
#     if product_data.empty:
#         st.warning("No valid data after cleaning.")
#         return

#     # --- Best Product Logic ---
#     product_data["Value Score"] = (product_data["Rating"] / product_data["Price"]) * 100
#     best_product = product_data.sort_values("Value Score", ascending=False).iloc[0]
    
#     st.subheader("🏆 Best Value Product")
#     st.markdown(f"**{best_product['Name']}**  \n"
#                 f"Price: ₹{best_product['Price']:.2f}  \n"
#                 f"Rating: {best_product['Rating']}/5  \n"
#                 f"[Product Link]({best_product['URL']})")

#     # --- Select Top 4 Products ---
#     # Sort by Value Score (or any other criteria) and select top 4
#     top_4_products = product_data.sort_values("Value Score", ascending=False).head(4)

#     # --- Visualizations ---
#     fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 12))  # Increased figure size
    
#     # Replace product names with generic labels
#     product_labels = [f"Product {i+1}" for i in range(len(top_4_products))]
    
#     # Price Comparison
#     bars1 = ax1.bar(product_labels, top_4_products["Price"], color='#66b3ff', width=0.6)  # Adjusted bar width
#     ax1.set_title("Price Comparison (Top 4 Products)", fontweight='bold')
#     ax1.set_xlabel("Price (₹)", fontweight='bold')
#     ax1.set_xticklabels(product_labels, rotation=0, ha="right")  # Rotate labels for better alignment
#     ax1.grid(axis='y', linestyle='--')
    
#     # Add price values on top of bars
#     for bar in bars1:
#         height = bar.get_height()
#         ax1.text(
#             bar.get_x() + bar.get_width() / 2,  # X position (center of the bar)
#             height + 0.02 * max(top_4_products["Price"]),  # Y position (slightly above the bar)
#             f'₹{height:.2f}',  # Text to display
#             ha='center',  # Horizontal alignment
#             va='bottom',  # Vertical alignment
#             fontsize=10
#         )
    
#     # Rating Comparison
#     bars2 = ax2.bar(product_labels, top_4_products["Rating"], color='#99ff99', width=0.6)  # Adjusted bar width
#     ax2.set_title("Rating Comparison (Top 4 Products)", fontweight='bold')
#     ax2.set_xlabel("Rating (out of 5)", fontweight='bold')
#     ax2.set_xticklabels(product_labels, rotation=0, ha="right")  # Rotate labels for better alignment
#     ax2.set_ylim(0, 5)  # Set y-axis limit for ratings
#     ax2.grid(axis='y', linestyle='--')
    
#     # Add rating values on top of bars
#     for bar in bars2:
#         height = bar.get_height()
#         ax2.text(
#             bar.get_x() + bar.get_width() / 2,  # X position (center of the bar)
#             height + 0.02 * 5,  # Y position (slightly above the bar)
#             f'{height:.1f}',  # Text to display
#             ha='center',  # Horizontal alignment
#             va='bottom',  # Vertical alignment
#             fontsize=10
#         )
    
#     plt.tight_layout()  # Adjust layout to prevent overlap
#     st.pyplot(fig)
#     plt.close(fig)  # Prevent memory leaks

#     # --- Data Table ---
#     st.subheader("Raw Data")
#     product_data_display = product_data[["Name", "Price", "Rating", "URL"]].copy()
#     product_data_display["URL"] = product_data_display["URL"].apply(
#         lambda x: f'<a href="{x}" target="_blank">🔗 Click Here To Buy</a>'
#     )
#     st.markdown(product_data_display.to_html(escape=False, index=False), unsafe_allow_html=True)