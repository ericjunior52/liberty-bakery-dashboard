import base64
from pathlib import Path

import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="Liberty Bakery Dashboard",
    page_icon="LB",
    layout="wide"
)


def load_starting_products():
    return [
        {"Product": "Butter Bread", "Category": "Bread", "Price": 3.50, "Stock": 25},
        {"Product": "Sugar Bread", "Category": "Bread", "Price": 3.00, "Stock": 18},
        {"Product": "Tea Bread", "Category": "Bread", "Price": 2.75, "Stock": 12},
    ]


def image_to_base64(image_path):
    path = Path(image_path)

    if not path.exists():
        return ""

    return base64.b64encode(path.read_bytes()).decode()


if "products" not in st.session_state:
    st.session_state.products = load_starting_products()


hero_image = image_to_base64("assets/bakery_couple.png")
logo_image = image_to_base64("assets/liberty_logo.png")
owner_image = image_to_base64("assets/bakery_owner.png")


st.markdown(
    """
    <style>
    .stApp {
        background:
            radial-gradient(circle at top left, rgba(255, 255, 255, 0.90), transparent 28%),
            linear-gradient(135deg, #f5f0ff 0%, #eadcff 42%, #d8b4fe 100%);
        color: #2e1065;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }

    .hero {
        min-height: 320px;
        display: flex;
        align-items: center;
        background-size: cover;
        background-position: center;
        border: 1px solid rgba(109, 40, 217, 0.18);
        border-radius: 26px;
        padding: 32px;
        box-shadow: 0 24px 55px rgba(46, 16, 101, 0.24);
        margin-bottom: 28px;
        overflow: hidden;
    }

    .logo-row {
        display: flex;
        align-items: center;
        gap: 18px;
        flex-wrap: wrap;
    }

    .real-logo {
        width: 112px;
        height: 112px;
        object-fit: cover;
        border-radius: 50%;
        box-shadow: 0 18px 38px rgba(46, 16, 101, 0.45);
        border: 4px solid rgba(255, 255, 255, 0.85);
    }

    .logo-title {
        font-size: 3.3rem;
        font-weight: 900;
        color: #ffffff;
        margin: 0;
        line-height: 1.05;
        text-shadow: 0 8px 25px rgba(0, 0, 0, 0.45);
    }

    .logo-subtitle {
        color: #fdf4ff;
        font-size: 1.35rem;
        font-weight: 700;
        margin-top: 8px;
        margin-bottom: 0;
        text-shadow: 0 6px 18px rgba(0, 0, 0, 0.45);
    }

    .section-card {
        background: rgba(255, 255, 255, 0.82);
        border: 1px solid rgba(109, 40, 217, 0.16);
        border-radius: 20px;
        padding: 22px;
        box-shadow: 0 12px 30px rgba(109, 40, 217, 0.12);
        margin-bottom: 22px;
    }

    .owner-card {
        background: rgba(255, 255, 255, 0.86);
        border: 1px solid rgba(109, 40, 217, 0.18);
        border-radius: 22px;
        padding: 18px;
        box-shadow: 0 16px 38px rgba(109, 40, 217, 0.14);
        margin-bottom: 22px;
    }

    .owner-image {
        width: 100%;
        height: 420px;
        object-fit: cover;
        border-radius: 18px;
        box-shadow: 0 16px 35px rgba(46, 16, 101, 0.18);
    }

    .owner-title {
        color: #581c87;
        font-size: 1.5rem;
        font-weight: 900;
        margin-top: 16px;
        margin-bottom: 6px;
    }

    .owner-text {
        color: #4c1d95;
        font-size: 1rem;
        line-height: 1.5;
    }

    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.88);
        border: 1px solid rgba(109, 40, 217, 0.16);
        border-radius: 18px;
        padding: 18px;
        box-shadow: 0 10px 28px rgba(109, 40, 217, 0.12);
    }

    .stButton button,
    .stFormSubmitButton button {
        background: linear-gradient(135deg, #6d28d9, #9333ea);
        color: white;
        border: none;
        border-radius: 12px;
        font-weight: 700;
        padding: 0.6rem 1rem;
    }

    .stButton button:hover,
    .stFormSubmitButton button:hover {
        color: white;
        border: none;
        background: linear-gradient(135deg, #5b21b6, #7e22ce);
    }

    @media (max-width: 700px) {
        .hero {
            min-height: 260px;
            padding: 22px;
        }

        .logo-title {
            font-size: 2.2rem;
        }

        .real-logo {
            width: 78px;
            height: 78px;
        }

        .owner-image {
            height: 320px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)


df = pd.DataFrame(st.session_state.products)
df["Inventory Value"] = df["Price"] * df["Stock"]

low_stock_items = df[df["Stock"] <= 10]
total_products = len(df)
inventory_value = df["Inventory Value"].sum()


st.markdown(
    f"""
    <div class="hero" style="
        background-image:
            linear-gradient(90deg, rgba(46, 16, 101, 0.88), rgba(88, 28, 135, 0.54)),
            url('data:image/png;base64,{hero_image}');
    ">
        <div class="logo-row">
            <img class="real-logo" src="data:image/png;base64,{logo_image}" />
            <div>
                <h1 class="logo-title">Liberty Bakery</h1>
                <p class="logo-subtitle">Pure Flour-ishing.</p>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


metric_one, metric_two, metric_three = st.columns(3)

metric_one.metric("Bread Types", total_products)
metric_two.metric("Low Stock Items", len(low_stock_items))
metric_three.metric("Inventory Value", f"${inventory_value:,.2f}")


left_column, right_column = st.columns([1, 1.4])

with left_column:
    st.markdown(
        f"""
        <div class="owner-card">
            <img class="owner-image" src="data:image/png;base64,{owner_image}" />
            <div class="owner-title">Made Fresh With Care</div>
            <div class="owner-text">
                Liberty Bakery focuses on simple, fresh bread made with care:
                butter bread, sugar bread, and tea bread.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with right_column:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Add New Bread Product")

    with st.form("add_bread_form"):
        new_product = st.text_input("Bread Name")
        new_price = st.number_input("Price", min_value=0.0, step=0.50)
        new_stock = st.number_input("Stock Quantity", min_value=0, step=1)

        add_submitted = st.form_submit_button("Add Bread")

        if add_submitted:
            if new_product.strip() == "":
                st.error("Please enter a bread name.")
            else:
                bread = {
                    "Product": new_product.strip(),
                    "Category": "Bread",
                    "Price": new_price,
                    "Stock": new_stock,
                }

                st.session_state.products.append(bread)
                st.success(f"{new_product} has been added.")
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.subheader("Bread Catalog")
st.dataframe(df, width="stretch")
st.markdown("</div>", unsafe_allow_html=True)


st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.subheader("Quick Order Calculator")

with st.form("bread_order_form"):
    customer_name = st.text_input("Customer Name")
    selected_product = st.selectbox("Bread Type", df["Product"].tolist())
    quantity = st.number_input("Quantity", min_value=1, step=1)

    order_submitted = st.form_submit_button("Calculate Order")

    if order_submitted:
        product_row = df[df["Product"] == selected_product].iloc[0]
        price = product_row["Price"]
        total = price * quantity

        if customer_name.strip() == "":
            customer_name = "Customer"

        st.success(
            f"{customer_name} ordered {quantity} x {selected_product}. "
            f"Total: ${total:,.2f}"
        )

st.markdown("</div>", unsafe_allow_html=True)


st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.subheader("Low Stock Alert")

if low_stock_items.empty:
    st.success("All bread products have enough stock.")
else:
    st.warning("These bread products are running low:")
    st.dataframe(low_stock_items[["Product", "Category", "Stock"]], width="stretch")

st.markdown("</div>", unsafe_allow_html=True)