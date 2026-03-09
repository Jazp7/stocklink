# Decision 7 — Server-Side Pagination

**Decision:** Implement pagination at the database/API level rather than fetching all records and paginating in the frontend.

**Why:**
- **Scalability**: As the number of products and providers grows (e.g., thousands of items), fetching everything at once would slow down the app and consume excessive memory and bandwidth.
- **Performance**: SQL `LIMIT` and `OFFSET` are highly optimized for returning small chunks of data.
- **User Experience**: Allows the UI to stay responsive even with large datasets.

**Implications of changing to client-side pagination:**
- The API would return a simple list again.
- The frontend would need to store the entire dataset in state.
- Performance would degrade as the dataset grows.
