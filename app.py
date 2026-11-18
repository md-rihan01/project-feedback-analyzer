"""Streamlit dashboard for analyzing customer reviews with the FastAPI backend."""

import requests
import streamlit as st


API_URL = "http://127.0.0.1:8000/analyze"

st.set_page_config(page_title="Customer Feedback Analyzer", page_icon="📊", layout="wide")

st.title("Customer Feedback Analyzer")
st.write("Analyze customer reviews to see their sentiment, score, and main theme.")

reviews_text = st.text_area(
    "Customer reviews",
    height=220,
    placeholder="Enter one customer review per line...",
    help="Each non-empty line is sent to the analyzer as a separate review.",
)

if st.button("Analyze Reviews", type="primary"):
    reviews = [line.strip() for line in reviews_text.splitlines() if line.strip()]

    if not reviews:
        st.error("Enter at least one customer review before analyzing.")
    else:
        results = []
        error_message = None

        with st.spinner(f"Analyzing {len(reviews)} review(s)..."):
            for review in reviews:
                try:
                    response = requests.post(
                        API_URL,
                        json={"text": review},
                        timeout=60,
                    )
                    response.raise_for_status()
                    analysis = response.json()

                    # Match the response fields defined by api.py's Analysis model.
                    results.append(
                        {
                            "Review": review,
                            "Label": analysis["label"],
                            "Score": analysis["score"],
                            "Theme": analysis["theme"],
                        }
                    )
                except requests.ConnectionError:
                    error_message = (
                        "Could not connect to the analysis API. Make sure the FastAPI "
                        "backend is running at http://127.0.0.1:8000."
                    )
                    break
                except requests.Timeout:
                    error_message = "The API took too long to respond. Please try again."
                    break
                except requests.HTTPError as exc:
                    try:
                        detail = response.json().get("detail", response.reason)
                    except (ValueError, AttributeError):
                        detail = response.reason
                    error_message = f"The API returned an error ({response.status_code}): {detail}"
                    break
                except (ValueError, KeyError, TypeError):
                    error_message = "The API returned an invalid response. Please try again."
                    break
                except requests.RequestException as exc:
                    error_message = f"Could not complete the API request: {exc}"
                    break

        if error_message:
            st.error(error_message)
        elif results:
            st.subheader("Summary")
            total_reviews = len(results)
            average_score = sum(result["Score"] for result in results) / total_reviews
            positive_count = sum(
                1 for result in results if str(result["Label"]).lower() == "positive"
            )
            positive_percentage = positive_count / total_reviews * 100

            metric_columns = st.columns(3)
            metric_columns[0].metric("Total Reviews", total_reviews)
            metric_columns[1].metric("Average Score", f"{average_score:.2f} / 5")
            metric_columns[2].metric("Positive Reviews", f"{positive_percentage:.1f}%")

            st.subheader("Review Analysis")
            st.dataframe(results, use_container_width=True, hide_index=True)
