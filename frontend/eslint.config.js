import js from '@eslint/js'
import globals from 'globals'
import reactHooks from 'eslint-plugin-react-hooks'
import reactRefresh from 'eslint-plugin-react-refresh'
import tseslint from 'typescript-eslint'
import prettier from 'eslint-config-prettier'
import { defineConfig, globalIgnores } from 'eslint/config'

// Regras de qualidade do guia de código (AGENTS.md §2 e §4).
const regrasDeQualidade = {
  complexity: ['error', 8],
  'max-params': ['error', 4],
  'max-depth': ['error', 3],
  'max-lines-per-function': ['error', { max: 60, skipBlankLines: true, skipComments: true }],
  'max-lines': ['error', { max: 300, skipBlankLines: true, skipComments: true }],
  'no-console': ['error', { allow: ['warn', 'error'] }],
  eqeqeq: ['error', 'always'],
  '@typescript-eslint/no-explicit-any': 'error',
  '@typescript-eslint/naming-convention': [
    'error',
    { selector: 'typeLike', format: ['PascalCase'] },
    { selector: 'variable', format: ['camelCase', 'PascalCase', 'UPPER_CASE'] },
    { selector: 'function', format: ['camelCase', 'PascalCase'] },
  ],
}

// Só a camada de serviços conversa com a API (AGENTS.md §2, frontend).
const fetchSoNosServicos = {
  'no-restricted-globals': [
    'error',
    { name: 'fetch', message: 'Chame a API apenas por src/servicos/.' },
  ],
}

export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      js.configs.recommended,
      tseslint.configs.recommended,
      reactHooks.configs.flat.recommended,
      reactRefresh.configs.vite,
      prettier,
    ],
    languageOptions: {
      globals: globals.browser,
    },
    rules: regrasDeQualidade,
  },
  {
    files: ['src/**/*.{ts,tsx}'],
    ignores: ['src/servicos/**'],
    rules: fetchSoNosServicos,
  },
])
