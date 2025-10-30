# Frontend Structure Documentation

## Overview
The frontend has been refactored with proper TypeScript interfaces and a clean separation of concerns.

## Directory Structure

```
frontend/src/
├── constants/          # Type definitions and configuration constants
│   ├── types.ts       # TypeScript interfaces (Tree, ApiResponse, etc.)
│   ├── config.ts      # App configuration (API endpoints, limits, etc.)
│   ├── index.ts       # Central export point
│   └── README.md      # Documentation
│
├── utils/             # Utility functions
│   ├── api.ts         # API client functions (fetchTrees, detectTreesInImage)
│   └── index.ts       # Export utilities
│
├── lib/               # Core libraries and setup
│   └── config.ts      # Axios instance with interceptors
│
├── api/               # Next.js API routes (optional)
│   └── trees/
│       └── route.ts   # Server-side API handler
│
└── app/               # Next.js app directory
    ├── trees/
    │   └── page.tsx   # Trees listing page (client component)
    ├── layout.tsx     # Root layout
    └── page.tsx       # Home page
```

## Key Improvements

### 1. **Proper Type Safety**
- All interfaces defined in `constants/types.ts`
- No more `any` types
- Full IntelliSense support

### 2. **Centralized Configuration**
- API endpoints in one place
- Easy to update URLs and settings
- Environment variable support

### 3. **Clean Import Paths**
```typescript
// Before (broken)
import { fetchTrees } from "@/api/trees/route";

// After (clean)
import { fetchTrees } from "@/utils/api";
import { Tree, API_ENDPOINTS } from "@/constants";
```

### 4. **Better Error Handling**
- Loading states
- Error states
- Try-catch blocks
- Axios interceptors for global error handling

### 5. **Reusable Components**
The `TreesPage` component now includes:
- Loading state
- Error handling
- Empty state
- Rich tree information display
- Type-safe data rendering

## Usage Examples

### Fetching Trees
```typescript
import { fetchTrees } from "@/utils/api";
import { Tree } from "@/constants";

const loadTrees = async () => {
  const response = await fetchTrees();
  const trees: Tree[] = response.data;
  // Use trees with full type safety
};
```

### Adding New Types
```typescript
// In constants/types.ts
export interface TreeStats {
  totalCount: number;
  averageConfidence: number;
  speciesDistribution: Record<string, number>;
}

// Use anywhere
import { TreeStats } from "@/constants";
```

### Using Configuration
```typescript
import { API_ENDPOINTS, APP_CONFIG } from "@/constants";

// Validate file upload
if (file.size > APP_CONFIG.MAX_FILE_SIZE) {
  throw new Error("File too large");
}

// Make API call
const url = API_ENDPOINTS.DETECT;
```

## TypeScript Configuration

Updated `tsconfig.json` paths:
```json
{
  "paths": {
    "@/*": ["./src/*"]  // Fixed from "./*"
  }
}
```

This allows clean imports like `@/constants`, `@/utils`, etc.

## API Client Setup

The Axios instance in `lib/config.ts` includes:
- Base URL from environment or default
- Timeout configuration
- Request interceptor (for auth tokens)
- Response interceptor (for error handling)

## Next Steps

1. **Add Environment Variables**
   Create `.env.local`:
   ```
   NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
   ```

2. **Add More API Functions**
   Extend `utils/api.ts` with more endpoints

3. **Create Custom Hooks**
   ```typescript
   // utils/hooks/useTrees.ts
   export const useTrees = () => {
     const [trees, setTrees] = useState<Tree[]>([]);
     // ... logic
     return { trees, loading, error };
   };
   ```

4. **Add Form Validation**
   Create validators in `utils/validators.ts`

## Benefits

✅ **Type Safety** - Catch errors at compile time  
✅ **Maintainability** - Clear structure and organization  
✅ **Scalability** - Easy to add new features  
✅ **Developer Experience** - Better IntelliSense and autocomplete  
✅ **Code Reusability** - Shared types and utilities  
✅ **Error Prevention** - TypeScript catches issues early  

## Testing

All TypeScript errors have been resolved:
- ✅ No implicit `any` types
- ✅ All imports resolve correctly
- ✅ Type safety throughout the application
- ✅ Proper async/await patterns
