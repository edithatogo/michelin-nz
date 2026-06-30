# Contributing to Michelin Per-Capita Dashboard

We are building a community-driven database of restaurant blog reviews. We welcome pull requests from bloggers, critics, and developers!

---

## ✍️ How to Add Your Blog Review

If you have reviewed one of the listed restaurants on your blog, Substack, or social media, you can add it directly to our dashboard cards:

1. **Find the restaurant ID:**
   Look inside `src/nz.md` for the restaurant array keys (e.g., `hiakai`, `the-grove`, `amisfield`).

2. **Create a review JSON file:**
   Add a JSON file inside `src/data/reviews/` named `{restaurant-id}.json` (or `{restaurant-id}-{your-blog-name}.json` if one already exists).

3. **Format your JSON review:**
   ```json
   {
     "restaurantId": "hiakai",
     "author": "My Food Substack Name",
     "rating": "4.8/5",
     "content": "A short, engaging snippet of your review (maximum 150 characters).",
     "link": "https://yourblog.substack.com/post-link"
   }
   ```

4. **Submit a Pull Request:**
   Commit the file and open a PR on GitHub. Our automated pipeline will compile the JSON files on the next build!

---

## 💻 Developer Contributions

1. Fork the repo and create a branch: `feat/my-awesome-improvement`.
2. Follow our coding guidelines inside [code_styleguides/](file:///Volumes/PortableSSD/GitHub/michelin-nz/conductor/code_styleguides/).
3. Make sure to run `npm run build` locally before committing to check for compile errors.
