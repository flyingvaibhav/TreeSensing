// API Endpoints
export const API_ENDPOINTS = {
  UPLOAD: "/upload",
  DETECTIONS: "/detections",
  DETECTION_BY_ID: (id: string) => `/detections/${id}`,
  HEALTH: "/health",
} as const;

// API Configuration
export const API_CONFIG = {
  BASE_URL: process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000",
  TIMEOUT: 30000, // 30 seconds
} as const;

// App Configuration
export const APP_CONFIG = {
  MAX_FILE_SIZE: 10 * 1024 * 1024, // 10MB
  ALLOWED_FILE_TYPES: ["image/jpeg", "image/jpg", "image/png"],
  CONFIDENCE_THRESHOLD: 0.25,
} as const;
