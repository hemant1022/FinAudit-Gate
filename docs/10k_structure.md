# 10-K Structure Boundaries

When parsing an SEC 10-K filing (such as Apple's 2023 10-K), it's crucial to identify the narrative boundaries accurately for our vector database. 

## Observations from AAPL 2023 10-K

1. **Item 1A. Risk Factors**
   - **Start Marker**: Look for explicit headers matching `Item 1A. Risk Factors` or similar capitalization variants.
   - **Content**: Contains the bulk of qualitative risk narratives, extremely valuable for the `Risk Auditor Agent`.
   - **End Marker**: The start of `Item 1B. Unresolved Staff Comments` or `Item 2. Properties`.

2. **Item 7. Management's Discussion and Analysis of Financial Condition and Results of Operations (MD&A)**
   - **Start Marker**: `Item 7. Management's Discussion and Analysis of Financial Condition and Results of Operations`.
   - **Content**: Detailed analysis of financial results, liquidity, and capital resources. Key input for the `Analysis Agent`.
   - **End Marker**: The start of `Item 7A. Quantitative and Qualitative Disclosures About Market Risk`.

## Parsing Strategy

Using `unstructured` or `LlamaParse`, the HTML elements are categorized into `NarrativeText`, `Title`, and `Table`.
- **Narratives**: Text blocks under `Title` elements that match the start markers above should be chunked hierarchically.
- **Tables**: `Table` elements should be routed to a separate pipeline for structured data extraction (SQLite/CSV) to prevent polluting the narrative vector index.

We've confirmed this separation strategy by parsing `10k.htm` into `narratives/` and `tables/` directories.
