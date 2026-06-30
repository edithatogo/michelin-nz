# NZ Culinary Guide & Map Directions

This guide lists premium New Zealand eateries. Select a restaurant to open deep links to your mapping application of choice for directions or reviews.

```js
// Load compiled community reviews
const reviews = await FileAttachment("data/community_reviews.json").json();
const allRestaurants = await FileAttachment("data/restaurants.json").json();

const restaurants = allRestaurants.filter(d => d.country === "NZL");

// Helper to filter reviews for a specific restaurant ID
function getReviewsForRestaurant(id) {
  return reviews.filter(r => r.restaurantId === id);
}
```

```js
display(html`<div class="dashboard-grid">
  ${restaurants.map((r) => {
    const restaurantReviews = getReviewsForRestaurant(r.id);
    return html`
      <div class="card">
        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
          <h3>${r.name}</h3>
          <span class="star-rating">${"★".repeat(r.stars)}</span>
        </div>
        <p><strong>Cuisine:</strong> ${r.type}</p>
        <p><strong>Location:</strong> ${r.location}</p>
        
        <div style="margin-top: 1rem; border-top: 1px solid #1e293b; padding-top: 0.8rem;">
          <strong>Get Directions:</strong>
          <div style="display: flex; gap: 0.5rem; margin-top: 0.5rem; flex-wrap: wrap;">
            <a class="direction-link" target="_blank" href="https://www.google.com/maps/search/?api=1&query=${r.lat},${r.lng}" style="color: #06b6d4; text-decoration: none;">Google Maps</a> |
            <a class="direction-link" target="_blank" href="maps://?q=${r.name}&ll=${r.lat},${r.lng}" style="color: #fbbf24; text-decoration: none;">Apple Maps</a> |
            <a class="direction-link" target="_blank" href="https://www.openstreetmap.org/?mlat=${r.lat}&mlon=${r.lng}#map=17/${r.lat}/${r.lng}" style="color: #f43f5e; text-decoration: none;">OpenStreetMap</a>
          </div>
        </div>

        <div style="margin-top: 0.8rem;">
          <strong>Read Reviews:</strong>
          <div style="display: flex; gap: 0.5rem; margin-top: 0.5rem; flex-wrap: wrap;">
            <a target="_blank" href="https://www.google.com/search?q=${encodeURIComponent(`${r.name} ${r.location} reviews`)}" style="color: #fbbf24; text-decoration: none;">Google Search</a>
          </div>
        </div>

        ${restaurantReviews.length > 0 ? html`
          <div style="margin-top: 1rem; border-top: 1px dashed #1e293b; padding-top: 0.8rem;">
            <strong>Community Blog Reviews:</strong>
            ${restaurantReviews.map(rev => html`
              <div style="font-size: 0.9rem; margin-top: 0.5rem; color: #cbd5e1; background: rgba(30, 41, 59, 0.4); padding: 0.6rem; border-radius: 6px;">
                <div style="display: flex; justify-content: space-between; font-weight: bold; margin-bottom: 0.2rem;">
                  <span>${rev.author}</span>
                  <span style="color: #fbbf24;">${rev.rating}</span>
                </div>
                <p style="margin: 0; font-style: italic;">"${rev.content}"</p>
                <a target="_blank" href="${rev.link}" style="display: inline-block; margin-top: 0.4rem; font-size: 0.8rem; color: #06b6d4;">Read Full Post &rarr;</a>
              </div>
            `)}
          </div>
        ` : ""}
      </div>
    `;
  })}
</div>`);
```
