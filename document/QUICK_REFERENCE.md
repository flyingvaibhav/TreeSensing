# Quick Reference Guide

## Import Cheat Sheet

### Types & Interfaces
```typescript
import { Tree, TreesApiResponse, ApiResponse } from '@/constants';
```

### Configuration
```typescript
import { API_ENDPOINTS, API_CONFIG, APP_CONFIG } from '@/constants';
```

### API Functions
```typescript
import { fetchTrees, detectTreesInImage } from '@/utils/api';
// or
import { fetchTrees, detectTreesInImage } from '@/utils';
```

### Axios Instance
```typescript
import { API } from '@/lib/config';
```

## Common Patterns

### Fetching Data in Component
```typescript
"use client";

import { useEffect, useState } from "react";
import { fetchTrees } from "@/utils/api";
import { Tree } from "@/constants";

export default function MyComponent() {
  const [trees, setTrees] = useState<Tree[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadData = async () => {
      try {
        setLoading(true);
        const response = await fetchTrees();
        setTrees(response.data);
      } catch (err) {
        setError("Failed to load data");
      } finally {
        setLoading(false);
      }
    };
    loadData();
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return <div>{/* Render trees */}</div>;
}
```

### Adding New API Endpoint

1. **Add to constants/config.ts**
```typescript
export const API_ENDPOINTS = {
  // ... existing
  NEW_ENDPOINT: "/new-endpoint",
} as const;
```

2. **Add function to utils/api.ts**
```typescript
export const fetchNewData = async () => {
  try {
    const response = await API.get(API_ENDPOINTS.NEW_ENDPOINT);
    return response.data;
  } catch (error) {
    console.error("Error:", error);
    throw error;
  }
};
```

3. **Use in component**
```typescript
import { fetchNewData } from "@/utils/api";

const data = await fetchNewData();
```

### Creating New Types

Add to `constants/types.ts`:
```typescript
export interface NewType {
  id: string;
  name: string;
  // ... other fields
}
```

Then use anywhere:
```typescript
import { NewType } from '@/constants';

const myData: NewType = { ... };
```

## File Locations

| What | Where |
|------|-------|
| Types/Interfaces | `src/constants/types.ts` |
| Config Constants | `src/constants/config.ts` |
| API Functions | `src/utils/api.ts` |
| Axios Setup | `src/lib/config.ts` |
| Pages | `src/app/**/page.tsx` |
| API Routes | `src/api/**/route.ts` |

## Environment Variables

Create `.env.local` (not committed to git):
```bash
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

Use in code:
```typescript
const apiUrl = process.env.NEXT_PUBLIC_API_URL;
```

## TypeScript Tips

### Use proper types instead of any
❌ Bad:
```typescript
const data: any = await fetchTrees();
```

✅ Good:
```typescript
import { TreesApiResponse } from '@/constants';
const data: TreesApiResponse = await fetchTrees();
```

### Define function return types
❌ Bad:
```typescript
const getData = async () => {
  return await fetchTrees();
};
```

✅ Good:
```typescript
const getData = async (): Promise<TreesApiResponse> => {
  return await fetchTrees();
};
```

### Use optional chaining
```typescript
const confidence = tree?.confidence ?? 0;
const name = tree.location?.latitude ?? "Unknown";
```

## Debugging

### Check API calls
Open browser DevTools → Network tab

### Check TypeScript errors
```bash
npm run build
# or
npx tsc --noEmit
```

### Check ESLint
```bash
npm run lint
```
