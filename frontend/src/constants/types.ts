// Tree related types and interfaces

export interface Tree {
  id?: string;
  name: string;
  count: number;
  species?: string;
  location?: {
    latitude: number;
    longitude: number;
  };
  detectedAt?: string;
  confidence?: number;
}

export interface Detection {
  id?: string;
  filename: string;
  tree_count: number;
  avg_confidence: number;
  confidences: number[];
  image_size: {
    width: number;
    height: number;
  };
  timestamp: string;
}

export interface TreeDetectionResult {
  totalTrees: number;
  trees: Tree[];
  imageUrl?: string;
  processedAt?: string;
}

export interface ApiResponse<T> {
  data: T;
  message?: string;
  success?: boolean;
}

export interface TreesApiResponse extends ApiResponse<Tree[]> {
  data: Tree[];
}

export interface DetectionResponse extends ApiResponse<Detection> {
  success: boolean;
  message: string;
  data: Detection;
}

export interface DetectionsListResponse extends ApiResponse<Detection[]> {
  success: boolean;
  count: number;
  data: Detection[];
}
