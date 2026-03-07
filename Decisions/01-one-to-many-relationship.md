# Decision 1 — One-to-Many Relationship (Products → Providers)

**Decision:** Each product belongs to exactly one provider. The `provider_id` foreign key lives in the `products` table.

**Why:**
- Simpler to implement and query for a project of this scope.
- Avoids the complexity of a junction table (`product_provider`) required by Many-to-Many.
- Covers the minimum requirements of the technical assessment.
- Prevents data duplication: provider contact info is stored once, referenced by ID.

**Implications of changing to Many-to-Many:**
- A new `product_provider` junction table would need to be created in Supabase.
- All backend queries fetching products with provider info would need to be rewritten with JOIN logic.
- API responses returning `provider_id` would need to return an array of IDs instead.
- Frontend components displaying provider info per product would need to handle multiple providers.
