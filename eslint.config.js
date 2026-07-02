import js from "@eslint/js";

export default [
  {
    ignores: ["src/.observablehq/**", "dist/**"]
  },
  js.configs.recommended,
  {
    rules: {
      "no-unused-vars": "error",
      "no-undef": "error"
    },
    languageOptions: {
      ecmaVersion: "latest",
      sourceType: "module",
      globals: {
        window: "readonly",
        document: "readonly",
        console: "readonly",
        process: "readonly",
        URL: "readonly",
        FileAttachment: "readonly",
        html: "readonly",
        display: "readonly",
        invalidation: "readonly",
        Inputs: "readonly",
        Plot: "readonly"
      }
    }
  }
];
