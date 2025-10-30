# Constants Directory

This directory contains all TypeScript interfaces, types, and constant values used throughout the application.

## Structure

### `types.ts`
Contains all TypeScript interfaces and types for the application:
- `Tree` - Interface for tree data objects
- `TreeDetectionResult` - Result structure for tree detection operations
- `ApiResponse<T>` - Generic API response wrapper
- `TreesApiResponse` - Specific API response for trees endpoint

### `config.ts`
Contains application configuration constants:
- `API_ENDPOINTS` - All backend API endpoints
- `API_CONFIG` - API client configuration (base URL, timeout)
- `APP_CONFIG` - Application-level settings (file size limits, allowed types, etc.)

### `index.ts`
Central export point for all constants and types. Import from this file:

```typescript
import { Tree, API_ENDPOINTS, APP_CONFIG } from '@/constants';
```

## Usage Examples

### Using Types
```typescript
import { Tree, TreesApiResponse } from '@/constants';

const tree: Tree = {
  name: "Oak Tree",
  count: 5,
  species: "Quercus robur",
  confidence: 0.95
};

const response: TreesApiResponse = {
  data: [tree],
  success: true
};
```

### Using Config Constants
```typescript
import { API_ENDPOINTS, APP_CONFIG } from '@/constants';

// Use API endpoints
const url = `${API_ENDPOINTS.TREES}`;

// Check file size
if (file.size > APP_CONFIG.MAX_FILE_SIZE) {
  console.error('File too large');
}
```

## Best Practices

1. **Always define types** - Never use `any` when you can define a proper interface
2. **Use const assertions** - Add `as const` to constant objects to make them readonly
3. **Group related constants** - Keep similar constants together
4. **Document complex types** - Add JSDoc comments for complex interfaces
5. **Export from index** - Always export through the index file for clean imports
