import streamlit as st
import pandas as pd
from detection_agent import DetectionAgent
from correction_agent import CorrectionAgent
from enrichment_agent import EnrichmentAgent


st.title("🧹 CSV Data Cleaner with Agentic Workflow")


# ✅ Reusable CSV converter for downloads
@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')


uploaded_file = st.file_uploader("Upload a messy CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("Original Data")
    st.dataframe(df)

    if st.button("Run Detection Agent"):
        agent = DetectionAgent(df)
        logs = agent.run()

        st.subheader("🔍 Detection Logs")
        for log in logs:
            st.write("- " + log)

        st.subheader("🛠 Problematic Records")
        st.write("📌 Missing Values:")
        st.dataframe(agent.detect_missing())

        st.write("📌 Malformed Emails:")
        st.dataframe(agent.detect_malformed_emails())

        st.write("📌 Duplicates:")
        st.dataframe(agent.detect_duplicates())


#coorection agent


if st.button("🛠 Fix & Download Cleaned Data"):
    corrector = CorrectionAgent(df)
    cleaned_df, clean_logs = corrector.run()

    st.session_state.cleaned_df = cleaned_df  # ✅ Save for reuse

    st.subheader("✅ Correction Logs")
    for log in clean_logs:
        st.write("•", log)

    st.subheader("🧼 Cleaned Data")
    st.dataframe(cleaned_df)

    # Download button
    #@st.cache_data
    #def convert_df(df):
        #return df.to_csv(index=False).encode('utf-8')

    csv = convert_df(cleaned_df)
    st.download_button(
        label="📥 Download Cleaned CSV",
        data=csv,
        file_name="cleaned_data.csv",
        mime="text/csv"
    )



#enrichment agent

if "cleaned_df" in st.session_state:
    if st.button("✨ Enrich Data with LLM"):
        enricher = EnrichmentAgent(st.session_state.cleaned_df)
        enriched_df, enrich_logs = enricher.run()

        st.subheader("🔮 Enrichment Logs")
        for log in enrich_logs:
            st.write("•", log)

        st.subheader("💡 Enriched Data")
        st.dataframe(enriched_df)

        enriched_csv = convert_df(enriched_df)
        st.download_button(
            label="📥 Download Enriched CSV",
            data=enriched_csv,
            file_name="enriched_data.csv",
            mime="text/csv"
        )
else:
    st.info("⚠️ Please run the Correction Agent first before enrichment.")
