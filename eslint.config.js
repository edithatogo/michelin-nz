import js from "@eslint/js";

export default [
  js.configs.recommended,
  {
    rules: {
      "no-unused-vars": "warn",
      "no-undef": "error"
    },
    languageOptions: {
      ecmaVersion: "latest",
      sourceType: "module",
      globals: {
        window: "readonly",
        document: "readonly",
        console: "readonly",
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
