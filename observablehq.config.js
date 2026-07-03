// See https://observablehq.com/framework/config for documentation.
export default {
  // The project’s title; used in the sidebar and webpage titles.
  title: "Michelin Star Per-Capita Dashboard",

  // The pages and sections in the sidebar. If you’d like to customize first-page navigation
  // or structure your dashboard, list pages here.
  pages: [
    {
      name: "NZ Aggregate",
      path: "/nz"
    },
    {
      name: "GDP & Stars",
      path: "/gdp-stars"
    },
    {
      name: "Country Explorer",
      path: "/explorer"
    },
    {
      name: "Pivot Table",
      path: "/pivot"
    },
    {
      name: "Data & Sources",
      path: "/sources"
    }
  ],

  // Content to write to the head of the page, e.g. for analytics or styles.
  head: "",

  // The path to the source directory.
  root: "src",

  // Theme settings (sleek dark mode)
  theme: "dark",

  // Some additional configuration options
  style: "style.css"
};
